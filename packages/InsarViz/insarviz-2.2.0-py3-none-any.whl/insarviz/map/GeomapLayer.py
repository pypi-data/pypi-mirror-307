# -*- coding: utf-8 -*-

from typing import Any, Optional, Union, TYPE_CHECKING

import logging

import warnings

from collections import OrderedDict

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QRunnable, QThreadPool

from PyQt5.QtGui import (
    QIcon, QPainter, QOpenGLContext, QOffscreenSurface, QOpenGLShader, QMatrix4x4, QOpenGLTexture,
    QOpenGLVertexArrayObject, QAbstractOpenGLFunctions
)

from OpenGL.GL import (
    GL_TEXTURE0, GL_TRIANGLES,
    GL_UNSIGNED_INT,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
)

import numpy as np

import rasterio

from rasterio.vrt import WarpedVRT

from owslib.wmts import WebMapTileService, TileMatrixSetLink, TileMatrixSet

from insarviz.map.Layer import OpenGLLayer

from insarviz.map.Shaders import VERT_SHADER, GEOMAP_SHADER, ALPHA_SHADER

from insarviz.linalg import matrix

if TYPE_CHECKING:
    from insarviz.map.MapModel import MapModel

logger = logging.getLogger(__name__)


def tilematrix_xy_to_tilematrix_crs(x: int, y: int, zoom: int, wmts: WebMapTileService, layer: str,
                                    tilematrixset: str) -> tuple[float, float, float, float]:
    if str(zoom) in wmts.tilematrixsets[tilematrixset].tilematrix:
        tilematrix = wmts.tilematrixsets[tilematrixset].tilematrix[str(zoom)]
        if x < 0 or x >= tilematrix.matrixwidth:
            raise ValueError(f"x {x} is < 0 or >= tilematrix.width")
        if y < 0 or y >= tilematrix.matrixheight:
            raise ValueError(f"y {y} is < 0 or >= tilematrix height")
        tilematrixlimits = wmts.contents[layer].tilematrixsetlinks[tilematrixset].tilematrixlimits
        if tilematrixlimits:
            tilematrixlimit = tilematrixlimits[str(zoom)]
            if x < tilematrixlimit.mintilecol or x > tilematrixlimit.maxtilecol:
                raise ValueError(f"x {x} is out of tilematrixlimit")
            if y < tilematrixlimit.mintilerow or y > tilematrixlimit.maxtilerow:
                raise ValueError(f"y {y} is out of tilematrixlimit")
        # compute the corner of the tile xy in its crs coordinates
        tilematrix_crs = rasterio.CRS.from_string(wmts.tilematrixsets[tilematrixset].crs)
        pixelspan = tilematrix.scaledenominator * 0.00028 * tilematrix_crs.units_factor[1]
        left, top = tilematrix.topleftcorner
        left = left + pixelspan * x * tilematrix.tilewidth
        top = top - pixelspan * y * tilematrix.tileheight
        right = left + pixelspan * tilematrix.tilewidth
        bottom = top - pixelspan * tilematrix.tileheight
        return left, bottom, right, top
    else:
        raise ValueError(f'zoom {zoom} is not in tilematrixset {tilematrixset}')


class GeomapLayer(OpenGLLayer):

    icon: QIcon = QIcon()
    kind: str = "WMS layer"

    def __init__(self, name: str, model: "MapModel"):
        self.model_matrix: matrix.Matrix = matrix.scale(model.tex_width, model.tex_height)
        super().__init__(name)
        if self.icon.isNull():
            # cannot be initialized in the class declaration because:
            # "QIcon needs a QGuiApplication instance before the icon is created." see QIcon doc
            GeomapLayer.icon = QIcon('icons:WMS.svg')
        self.main_transform = model.loader.dataset.transform
        self.main_crs = model.loader.dataset.crs
        self.tiles = OrderedDict()  # implements a max_sized FIFO cache, keys are (zoom, x, y)
        self.tiles_cache_size = 100
        self.zoom: int = 0
        self.left_tile: int = 0
        self.right_tile: int = 0
        self.top_tile: int = 0
        self.bottom_tile: int = 0
        self.wmts = WebMapTileService(r'https://data.geopf.fr/wmts?')
        self.layer: str = 'ORTHOIMAGERY.ORTHOPHOTOS'
        self.tilematrixset: str = 'PM_0_21'
        # self.wmts = WebMapTileService(r'http://tiles.maps.eox.at/wmts')
        # self.layer = 'osm_3857'
        # self.tilematrixset = 'GoogleMapsCompatible'
        assert self.tilematrixset in self.wmts.contents[self.layer].tilematrixsetlinks.keys(), (f" GeomapLayer {self.name}, tilematrixset {self.tilematrixset} does not"
                                                                                                f"match any of{self.layer}'s tilematrixsets")
        self.format: str
        if "image/jpeg" in self.wmts.contents[self.layer].formats:
            self.format = "image/jpeg"
        elif "image/png" in self.wmts.contents[self.layer].formats:
            self.format = "image/png"
        else:
            raise RuntimeError(
                f"wmts does not have jpeg or png formats: {self.wmts.contents[self.layer].formats}")
        self.crs = rasterio.CRS.from_string(self.wmts.tilematrixsets[self.tilematrixset].crs)
        for i, op in enumerate(self.wmts.operations):
            if (not hasattr(op, 'name')):
                self.wmts.operations[i].name = ""
        self.tile_to_texture_pixelratio: dict[str, float] = {}
        assert self.crs.units_factor[0] in ("metre", "meter")
        assert not (rasterio.crs.epsg_treats_as_latlong(self.crs))
        for key, tilematrix in self.wmts.tilematrixsets[self.tilematrixset].tilematrix.items():
            # compute the corners of the tilematrix in its crs coordinates
            # see https://www.ogc.org/standard/wmts/
            left, top = tilematrix.topleftcorner
            pixelspan = tilematrix.scaledenominator * 0.00028 * self.crs.units_factor[1]
            right = left + pixelspan * tilematrix.tilewidth * tilematrix.matrixwidth
            bottom = top - pixelspan * tilematrix.tileheight * tilematrix.matrixheight
            # transform into coordinates in the main dataset crs
            left, bottom, right, top = rasterio.warp.transform_bounds(
                self.crs, self.main_crs, left, bottom, right, top)
            if np.isclose(left, right):
                left, right = -np.abs(left), np.abs(right)
            # transform into coordinates in main dataset pixels
            left, top = ~self.main_transform * (left, top)
            right, bottom = ~self.main_transform * (right, bottom)
            tile_to_texture_pixelratioX = (right - left) / \
                (tilematrix.tilewidth * tilematrix.matrixwidth)
            tile_to_texture_pixelratioY = (bottom - top) / \
                (tilematrix.tileheight * tilematrix.matrixheight)
            self.tile_to_texture_pixelratio[key] = tile_to_texture_pixelratioX
            # np.mean([tile_to_texture_pixelratioX,tile_to_texture_pixelratioY])

    def main_crs_to_tilematrix_xy(self, left: float, bottom: float, right: float, top: float, zoom: int):
        if str(zoom) in self.wmts.tilematrixsets[self.tilematrixset].tilematrix:
            tilematrix = self.wmts.tilematrixsets[self.tilematrixset].tilematrix[str(zoom)]
            # transform into coordinates in the tilematrix crs
            left, bottom, right, top = rasterio.warp.transform_bounds(
                self.main_crs, self.crs, left, bottom, right, top)
            tilematrix_bounds = self.tilematrix_bounds(zoom)
            # if both rects do not intersect return None
            if left > tilematrix_bounds[2]:
                return None
            if bottom > tilematrix_bounds[3]:
                return None
            if right < tilematrix_bounds[0]:
                return None
            if top < tilematrix_bounds[1]:
                return None
            # take the intersection between both rects
            left = max(left, tilematrix_bounds[0])
            bottom = max(bottom, tilematrix_bounds[1])
            right = min(right, tilematrix_bounds[2])
            top = min(top, tilematrix_bounds[3])
            # compute the x and y values
            pixelspan = tilematrix.scaledenominator * 0.00028 * self.crs.units_factor[1]
            left = int((left - tilematrix.topleftcorner[0]) / (pixelspan * tilematrix.tilewidth))
            bottom = int(
                (tilematrix.topleftcorner[1] - bottom) / (pixelspan * tilematrix.tileheight))
            right = int((right - tilematrix.topleftcorner[0]) / (pixelspan * tilematrix.tilewidth))
            top = int((tilematrix.topleftcorner[1] - top) / (pixelspan * tilematrix.tileheight))
            return left, bottom, right, top
        else:
            raise ValueError(f'zoom {zoom} is not in tilematrixset {self.tilematrixset}')

    def tilematrix_bounds(self, zoom):
        if str(zoom) in self.wmts.tilematrixsets[self.tilematrixset].tilematrix:
            tilematrix = self.wmts.tilematrixsets[self.tilematrixset].tilematrix[str(zoom)]
            pixelspan = tilematrix.scaledenominator * 0.00028 * self.crs.units_factor[1]
            left, top = tilematrix.topleftcorner
            tilematrixlimits = self.wmts.contents[self.layer].tilematrixsetlinks[self.tilematrixset].tilematrixlimits
            if tilematrixlimits:
                tilematrixlimit = tilematrixlimits[str(zoom)]
                left = left + pixelspan * tilematrixlimit.mintilecol * tilematrix.tilewidth
                top = top + pixelspan * tilematrixlimit.mintilerow * tilematrix.tileheight
                right = left + pixelspan * tilematrixlimit.maxtilecol * tilematrix.tilewidth
                bottom = top - pixelspan * tilematrixlimit.maxtilerow * tilematrix.tileheight
            else:
                right = left + pixelspan * tilematrix.matrixwidth * tilematrix.tilewidth
                bottom = top - pixelspan * tilematrix.matrixheight * tilematrix.tileheight
            return left, bottom, right, top
        else:
            raise ValueError(f'zoom {zoom} is not in tilematrixset {self.tilematrixset}')

    def add_tile(self, zoom: int, x: int, y: int):
        if len(self.tiles) > self.tiles_cache_size:
            removed = self.tiles.popitem(last=False)
            if removed[1] is not None:
                if self.context.isValid() and self.offscreen_surface.isValid():
                    self.context.makeCurrent(self.offscreen_surface)
                    # delete the OpenGL textures
                    # removed[1][0].destroy()
                    print("destroy")
                    self.context.doneCurrent()
        self.tiles[(zoom, x, y)] = None

        class Signals(QObject):
            done = pyqtSignal(tuple, QOpenGLTexture, list)

        class Task(QRunnable):

            def __init__(self, wmts: WebMapTileService, layer: str, tilematrixset: str, format: str,
                         main_crs: rasterio.CRS, main_transform: rasterio.transform.Affine,
                         texture: QOpenGLTexture):
                super().__init__()
                self.signals = Signals()
                self.wmts = wmts
                self.layer = layer
                self.tilematrixset = tilematrixset
                self.format = format
                self.main_crs = main_crs
                self.main_transform = main_transform
                self.texture = texture

            def run(self):
                context: QOpenGLContext = QOpenGLContext()
                context.setShareContext(QOpenGLContext.globalShareContext())
                context.create()
                if not context.isValid():
                    raise RuntimeError("Global OpenGL shared context cannot be created")
                offscreen_surface = QOffscreenSurface()
                offscreen_surface.setFormat(context.format())
                offscreen_surface.create()
                tilematrix = self.wmts.tilematrixsets[self.tilematrixset].tilematrix[str(zoom)]
                tile = self.wmts.gettile(layer=self.layer, tilematrixset=self.tilematrixset,
                                         tilematrix=str(int(zoom)),
                                         row=int(y), column=int(x),
                                         format=self.format)
                with warnings.catch_warnings():
                    # ignore RuntimeWarning for not georeferenced file
                    warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning,
                                            message=("Dataset has no geotransform, gcps, or rpcs. "
                                                     "The identity matrix will be returned."))
                    with rasterio.MemoryFile(tile) as notgeo_tile:
                        with notgeo_tile.open() as src:
                            data = src.read()
                            profile = src.profile
                if data.shape[0] == 1:
                    return
                left, bottom, right, top = tilematrix_xy_to_tilematrix_crs(
                    x, y, zoom, self.wmts, self.layer, self.tilematrixset)
                transform = rasterio.transform.from_bounds(
                    left, bottom, right, top, tilematrix.tilewidth, tilematrix.tileheight)
                tilematrix_crs = rasterio.CRS.from_string(
                    self.wmts.tilematrixsets[self.tilematrixset].crs)
                # TODO which compression to use ?
                profile.update(transform=transform, driver='GTiff', crs=tilematrix_crs,
                               height=tilematrix.tileheight, width=tilematrix.tilewidth,
                               compress='lzw')
                if "photometric" in profile:
                    del profile["photometric"]
                with rasterio.MemoryFile() as geo_tile:
                    with geo_tile.open(**profile) as dataset:
                        dataset.write(data)
                    with geo_tile.open() as src:
                        with WarpedVRT(src, crs=self.main_crs) as vrt:
                            img = vrt.read()
                            if img.dtype == "uint8":
                                img = img.astype(np.float32)/255
                            # transpose to change shape from (bands, rows, columns) to (rows, columns, bands)
                            # copy to ensure numpy does not create a view (that opengl cannot read properly)
                            img = np.transpose(img, [1, 2, 0]).copy().astype(np.float32)
                            # model matrix transforms coordinates inside the square (0,1) to coordinates in
                            # pixels relatively to the dataset
                            tile_model_matrix = matrix.from_rasterio_Affine(
                                ~self.main_transform
                                * vrt.transform
                                * rasterio.Affine.scale(*vrt.shape[::-1]))
                            h, w, d = img.shape
                            context.makeCurrent(offscreen_surface)
                            self.texture.setMagnificationFilter(QOpenGLTexture.Linear)
                            self.texture.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
                            self.texture.setWrapMode(QOpenGLTexture.ClampToEdge)
                            self.texture.setSize(w, h)
                            self.texture.setFormat(QOpenGLTexture.RGB32F)
                            self.texture.allocateStorage(QOpenGLTexture.RGB, QOpenGLTexture.Float32)
                            self.texture.setData(QOpenGLTexture.RGB,
                                                 QOpenGLTexture.Float32, img.data)
                            self.texture.generateMipMaps()
                            context.doneCurrent()
                            assert texture.textureId() != 0, f"Geomap layer thread: cannot load image texture in OpenGl"
                            self.signals.done.emit((zoom, x, y), self.texture, tile_model_matrix)
                            print("signal sent")

        texture = QOpenGLTexture(QOpenGLTexture.Target2D)
        self.update_tile_texture((zoom, x, y), texture, None)
        task = Task(self.wmts, self.layer, self.tilematrixset,
                    self.format, self.main_crs, self.main_transform, texture)
        task.signals.done.connect(self.update_tile_texture)
        QThreadPool.globalInstance().start(task)

    @pyqtSlot(tuple, QOpenGLTexture, list)
    def update_tile_texture(self, key, texture: QOpenGLTexture, model_matrix):
        if key in self.tiles:
            self.tiles[key] = (texture, model_matrix)
            self.request_paint.emit()

    def update_tileset(self, top_left, bottom_right, shape):
        # compute zoom
        tilematrixset_zooms = np.asarray(
            [int(_) for _ in self.wmts.tilematrixsets[self.tilematrixset].tilematrix.keys()])
        screen_to_texture_pixelratio = (np.abs(bottom_right[0] - top_left[0])) / shape[0]
        # set zoom to the nearest zoom in the tilematrix
        self.zoom = tilematrixset_zooms[int(min(self.tile_to_texture_pixelratio, key=lambda i: np.abs(
            screen_to_texture_pixelratio - self.tile_to_texture_pixelratio.get(i))))]
        # transform into x,y tile coordinates
        [left, right], [top, bottom] = rasterio.transform.xy(self.main_transform,
                                                             [top_left[1], bottom_right[1]],
                                                             [top_left[0], bottom_right[0]])
        left, right = min(left, right), max(left, right)
        bottom, top = min(top, bottom), max(top, bottom)
        self.left_tile, self.bottom_tile, self.right_tile, self.top_tile = self.main_crs_to_tilematrix_xy(
            left, bottom, right, top, self.zoom)
        for i in range(self.left_tile, self.right_tile+1):
            for j in range(self.top_tile, self.bottom_tile+1):
                if (self.zoom, i, j) in self.tiles:
                    # put the tile at the beginning of the cache if already in here (so it is not
                    # removed when adding the missing tiles)
                    self.tiles.move_to_end((self.zoom, i, j), last=True)
        for i in range(self.left_tile, self.right_tile+1):
            for j in range(self.top_tile, self.bottom_tile+1):
                if (self.zoom, i, j) not in self.tiles:
                    # request the missing tiles
                    self.add_tile(self.zoom, i, j)

    def show(self, view_matrix: matrix.Matrix, projection_matrix: matrix.Matrix,
             painter: Optional[QPainter] = None, vao: Optional[QOpenGLVertexArrayObject] = None,
             glfunc: Optional[QAbstractOpenGLFunctions] = None, blend: bool = True) -> None:
        if painter is not None:
            painter.beginNativePainting()
            # a VAO is required because QPainter bound its own VAO so we need to bind back our own
            assert vao is not None, "OpenGLLayer: vao is required when using QPainter"
        if blend:
            glfunc.glEnable(GL_BLEND)
            glfunc.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if vao is not None:
            vao.bind()
        print("start paint")
        self.program.bind()
        for i in range(self.left_tile, self.right_tile+1):
            for j in range(self.top_tile, self.bottom_tile+1):
                if self.tiles.get((self.zoom, i, j), None) is not None:
                    texture, model_matrix = self.tiles[(self.zoom, i, j)]
                    # bind textures to texture units
                    glfunc.glActiveTexture(GL_TEXTURE0)
                    print(
                        f"bind {texture.isCreated()} {texture.textureId()} bound {texture.isBound()}")
                    print(f"{texture.isStorageAllocated()} {texture.width()} {texture.height()}")
                    texture.bind()
                    print("end bind")
                    # set model, view and projection matrixes
                    self.program.setUniformValue('model_matrix',
                                                 QMatrix4x4(matrix.flatten(model_matrix)))
                    self.program.setUniformValue('view_matrix',
                                                 QMatrix4x4(matrix.flatten(view_matrix)))
                    self.program.setUniformValue('projection_matrix',
                                                 QMatrix4x4(matrix.flatten(projection_matrix)))
                    # set alpha value
                    self    .program.setUniformValue('alpha', self.alpha)
                    # draw the two triangles of the VAO that form a square
                    print("draw")
                    glfunc.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
                    texture.release()
                elif self.tiles.get((self.zoom-1, i//2, j//2), None) is not None:
                    pass  # TODO
                else:
                    for k in range(2):
                        for l in range(2):
                            if self.tiles.get((self.zoom+1, 2*i+k, 2*j+l), None) is not None:
                                texture, model_matrix = self.tiles[(self.zoom+1, 2*i+k, 2*j+l)]
                                # bind textures to texture units
                                glfunc.glActiveTexture(GL_TEXTURE0)
                                texture.bind()
                                # set model, view and projection matrixes
                                self.program.setUniformValue('model_matrix',
                                                             QMatrix4x4(matrix.flatten(model_matrix)))
                                self.program.setUniformValue('view_matrix',
                                                             QMatrix4x4(matrix.flatten(view_matrix)))
                                self.program.setUniformValue('projection_matrix',
                                                             QMatrix4x4(matrix.flatten(projection_matrix)))
                                # set alpha value
                                self.program.setUniformValue('alpha', self.alpha)
                                # draw the two triangles of the VAO that form a square
                                glfunc.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
                                texture.release()
        print("end paint")
        self.program.release()
        if vao is not None:
            vao.release()
        if painter is not None:
            painter.endNativePainting()

    def build_program(self) -> None:
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, VERT_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, ALPHA_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, GEOMAP_SHADER)
        self.program.link()
        self.program.bind()
        self.program.setUniformValue('model_matrix', QMatrix4x4(matrix.flatten(self.model_matrix)))
        self.program.setUniformValue('geomap_texture', 0)
        self.program.release()

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "GeomapLayer":
        assert input_dict["kind"] == cls.kind
        name = input_dict.get("name", "geomap layer")
        layer = GeomapLayer(name, map_model)
        if "visible" in input_dict:
            layer.visible = input_dict["visible"]
        if "alpha" in input_dict:
            layer.alpha = input_dict["alpha"]
        return layer

    def __del__(self):
        """
        Free textures and shader program from the VRAM when the layer is destroyed to prevent
        memory leaks.
        """
        try:
            if self.context.isValid() and self.offscreen_surface.isValid():
                self.context.makeCurrent(self.offscreen_surface)
                # delete the OpenGL textures
                for tile in self.tiles.values():
                    if tile is not None:
                        tile[0].destroy()
                # delete the OpenGL shaders program
                del self.program
                self.context.doneCurrent()
        except RuntimeError:
            # the context has already been deleted
            pass
