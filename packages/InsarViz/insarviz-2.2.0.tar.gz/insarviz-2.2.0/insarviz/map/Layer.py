# -*- coding: utf-8 -*-

from typing import Any, Optional, TYPE_CHECKING

import logging

import warnings

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from PyQt5.QtGui import (
    QIcon, QPainter, QOpenGLContext, QOffscreenSurface, QMatrix4x4, QOpenGLShaderProgram,
    QOpenGLShader, QOpenGLTexture, QAbstractOpenGLFunctions, QOpenGLVertexArrayObject
)

from OpenGL.GL import (
    GL_TEXTURE0,  GL_TRIANGLES,
    GL_UNSIGNED_INT,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
)

from pyqtgraph.colormap import ColorMap

from OpenGL.constant import IntConstant

import numpy as np

import os

import rasterio

from rasterio.vrt import WarpedVRT

from owslib.wms import WebMapService  # TODO WIP

from insarviz.map.TreeModel import TreeItem, TreeModel

from insarviz.map.TreeItemAttribute import (
    TreeItemAttribute, TreeItemColormapAttribute, TreeItemFloatAttribute
)

from insarviz.map.Shaders import (
    DATA_UNIT, PALETTE_UNIT, VERT_SHADER, PALETTE_SHADER, MAP_SHADER, GEOMAP_SHADER, ALPHA_SHADER
)

from insarviz.linalg import matrix

from insarviz.colormaps import my_colormaps, create_colormap_texture

from insarviz.Loader import Loader

from insarviz.ColormapWidget import ColormapWidget

if TYPE_CHECKING:
    from insarviz.map.MapModel import MapModel


logger = logging.getLogger(__name__)


class Layer(TreeItem):

    kind: str = "layer"  # description of the class, used in RemoveTreeItemCommand
    removable: bool = True
    renamable: bool = True
    icon: QIcon = QIcon()  # look https://github.com/qgis/QGIS/tree/master/images/themes/default

    request_paint = pyqtSignal()

    def __init__(self, name: str):
        super().__init__()
        # whether the layer is visible in MapView or not, also checkbox state in LayerView
        self.visible: bool = True
        self.name: str = name

    def show(self, view_matrix: matrix.Matrix, projection_matrix: matrix.Matrix,
             painter: Optional[QPainter] = None, vao: Optional[QOpenGLVertexArrayObject] = None,
             glfunc: Optional[QAbstractOpenGLFunctions] = None, blend: bool = True) -> None:
        """
        Shall be implemented by subclasses.
        Display the layer using either OpenGL commands or painter.

        Parameters
        ----------
        view_matrix : matrix.Matrix
            Transform world coordinates into view coordinates.
        projection_matrix : matrix.Matrix
            Transform view coordinates into clip coordinates (OpenGL only)
        painter : QPainter, optional
            QPainter provided by the view. If painter is given then vao_id must be given aswell.
        vao_id : QOpenGLVertexArrayObject, optional
            OpenGL Vertex Array Object, the VAO is a square mapped with a texture.
        glfunc : QAbstractOpenGLFunctions, optional
            OpenGL functions
        blend : bool, optional
        """
        raise NotImplementedError

    def data(self, column: int, role: int) -> Any:
        if column == TreeModel.remove_column:
            return None
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self.name
        if role == Qt.CheckStateRole:
            return Qt.Checked if self.visible else Qt.Unchecked
        if role == Qt.DecorationRole:
            return self.icon
        return None

    def flags(self, flags: Qt.ItemFlags, column: int) -> Qt.ItemFlags:
        if column == 0:
            # enable visibility checkbox and drag&drop
            flags = flags | Qt.ItemIsUserCheckable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
            if self.renamable:
                # enable name edition
                flags = flags | Qt.ItemIsEditable
        elif column == TreeModel.remove_column:
            if self.removable:
                # enable the remove button
                flags = flags | Qt.ItemIsEditable
        return flags

    def set_data(self, value: Any, column: int, role: int) -> bool:
        if column != 0:
            return False
        if role == Qt.CheckStateRole:
            self.visible = True if value == Qt.Checked else False
            return True
        if role == Qt.EditRole and self.renamable:
            self.name = value
            return True
        return False

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = {}
        output["kind"] = self.kind
        output["name"] = self.name
        output["visible"] = self.visible
        return output


class OpenGLLayer(Layer):

    # QOpenGLContext shared with every other contexts, set by ts_viz.MainWindow.initUI
    context: Optional[QOpenGLContext] = None
    # QOffscreenSurface to use OpenGL commands, set by ts_viz.MainWindow.initUI
    offscreen_surface: Optional[QOffscreenSurface] = None

    def __init__(self, name: str):
        super().__init__(name)
        # dict of texture_unit:texture
        self.textures: dict[int, QOpenGLTexture] = {}
        self.alpha: float = 1.
        self.add_child(TreeItemFloatAttribute(self, "alpha", name="alpha", vmin=0., vmax=1.,
                                              tooltip="transparency (between 0 and 1)"))
        assert self.context is not None, "OpengGLLayer.init: no OpenGL shared context"
        assert self.context.isValid(), "OpenGLLayer.init: OpenGL shared context not valid"
        assert self.offscreen_surface is not None, "OpengGLLayer.init: no QOffscreenSurface"
        assert self.offscreen_surface.isValid(), "OpenGLLayer.init: QOffscreenSurface not valid"
        self.context.makeCurrent(self.offscreen_surface)
        self.program = QOpenGLShaderProgram()
        self.build_program()
        self.context.doneCurrent()

    def build_program(self) -> None:
        """
        Shall be implemented by subclasses.
        Computes the OpenGL shader program used by the layer, possibly sets some constant uniforms
        to the program (such as texture unit for example) and then returns its id.
        A valid shared OpenGL context is supposed to already be current when this method is called.

        Note that texture unit shall be given as integer (without GL_TEXTURE0) with set_uniform.

        Returns
        -------
        program : int
            the OpenGL shader program id
        """
        # shall be implented by subclasses
        raise NotImplementedError

    @pyqtSlot(IntConstant, QOpenGLTexture)
    def set_texture(self, texture_unit: IntConstant, texture: QOpenGLTexture) -> None:
        """
        Set texture as value for key texture_unit in self.textures dictionnary.
        That information is used by self.show to bind the correct texture to the texture unit when
        displaying the layer.

        Parameters
        ----------
        texture_unit : int
            texture unit for glActiveTexture, shall be on the form GL_TEXTURE0 + ...
        texture : QOpenGLTexture
            texture to bind
        """
        self.textures[texture_unit] = texture

    def show(self, view_matrix: matrix.Matrix, projection_matrix: matrix.Matrix,
             painter: Optional[QPainter] = None, vao: Optional[QOpenGLVertexArrayObject] = None,
             glfunc: Optional[QAbstractOpenGLFunctions] = None, blend: bool = True) -> None:
        assert glfunc is not None
        if painter is not None:
            painter.beginNativePainting()
            # a VAO is required because QPainter bound its own VAO so we need to bind back our own
            assert vao is not None, "OpenGLLayer: vao is required when using QPainter"
        if blend:
            glfunc.glEnable(GL_BLEND)
            glfunc.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if vao is not None:
            vao.bind()
        # bind textures to texture units
        for texture_unit, texture in self.textures.items():
            glfunc.glActiveTexture(texture_unit)
            texture.bind()
        self.program.bind()
        # set view and projection matrixes
        self.program.setUniformValue('view_matrix', QMatrix4x4(matrix.flatten(view_matrix)))
        self.program.setUniformValue('projection_matrix',
                                     QMatrix4x4(matrix.flatten(projection_matrix)))
        # set alpha value
        self.program.setUniformValue('alpha', self.alpha)
        # draw the two triangles of the VAO that form a square
        glfunc.glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        self.program.release()
        for _, texture in self.textures.items():
            texture.release()
        if vao is not None:
            vao.release()
        if painter is not None:
            painter.endNativePainting()

    def __del__(self):
        """
        Free textures and shader program from the VRAM when the layer is destroyed to prevent
        memory leaks.
        """
        try:
            if self.context.isValid() and self.offscreen_surface.isValid():
                self.context.makeCurrent(self.offscreen_surface)
                # delete the OpenGL textures
                for _, texture in self.textures.items():
                    texture.destroy()
                # delete the OpenGL shaders program
                del self.program
                self.context.doneCurrent()
        except RuntimeError:
            # the context has already been deleted
            pass

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = super().to_dict(filedir)
        output["alpha"] = self.alpha
        return output


class MainLayer(OpenGLLayer):

    removable: bool = False
    renamable: bool = False
    kind: str = "main layer"

    def __init__(self, map_model: "MapModel"):
        self.width: int = map_model.tex_width
        self.height: int = map_model.tex_height
        super().__init__("Main Layer")
        map_model.texture_changed.connect(self.set_texture)
        map_model.v0_v1_changed.connect(self.set_v0_v1)

    def build_program(self) -> None:
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, VERT_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, PALETTE_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, ALPHA_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, MAP_SHADER)
        self.program.link()
        self.program.bind()
        model_matrix: matrix.Matrix = matrix.scale(self.width, self.height)
        self.program.setUniformValue('model_matrix', QMatrix4x4(matrix.flatten(model_matrix)))
        self.program.setUniformValue('values', DATA_UNIT)
        self.program.setUniformValue('palette', PALETTE_UNIT)
        self.program.setUniformValue('v0', 0.)
        self.program.setUniformValue('v1', 1.)
        self.program.release()

    def data(self, column: int, role: int) -> Any:
        if column == 0 and role == Qt.ToolTipRole:
            return "Main data layer, insar data cube"
        return super().data(column, role)

    # connected to MapModel.v0_v1_changed
    @pyqtSlot(float, float)
    def set_v0_v1(self, v0: float, v1: float) -> None:
        """Update v0 and v1."""
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        self.context.makeCurrent(self.offscreen_surface)
        self.program.bind()
        self.program.setUniformValue('v0', float(v0))
        self.program.setUniformValue('v1', float(v1))
        self.program.release()
        self.context.doneCurrent()

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "MainLayer":
        assert input_dict["kind"] == cls.kind
        layer = MainLayer(map_model)
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
                # textures are deleted by MapModel
                # delete the OpenGL shaders program
                del self.program
                self.context.doneCurrent()
        except RuntimeError:
            # the context has already been deleted
            pass


class RasterLayer(OpenGLLayer):

    nb_band: int = 0

    def __init__(self, name: str, model: "MapModel", filepath: str, bands: list[int],
                 mask: Optional[int]):
        self.model_matrix: matrix.Matrix = matrix.scale(model.tex_width, model.tex_height)
        super().__init__(name)
        with warnings.catch_warnings():
            # ignore RuntimeWarning for not georeferenced file
            warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning,
                                    message="Dataset has no geotransform, gcps, or rpcs. The identity matrix will be returned.")
            with rasterio.open(filepath) as file:
                assert model.loader.dataset is not None
                assert len(bands) == self.nb_band, (f"{self.__class__} requires {self.nb_band} "
                                                    f"bands but received {len(bands)}")
                assert ((file.crs is not None and model.loader.dataset.crs is not None) or
                        (file.shape == model.loader.dataset.shape)), (f"{self.__class__} requires a ",
                                                                      "geolocalized image or an image "
                                                                      "of same shape than the dataset")
                assert self.context is not None
                assert self.context.isValid()
                assert self.offscreen_surface is not None
                assert self.offscreen_surface.isValid()
                self.filepath = filepath
                self.add_child(TreeItemAttribute(self, "filepath",
                               tooltip=filepath, editable=False))
                self._bands = bands
                self._mask = mask
                if mask is not None:
                    bands += [mask]
                # warp the image if geolocated
                if (file.crs is not None and model.loader.dataset.crs is not None):
                    with WarpedVRT(file, crs=model.loader.dataset.crs) as vrt:
                        img = np.empty((*vrt.shape, self.nb_band+1), dtype=np.float32)
                        data = vrt.read(bands, out_dtype=np.float32)
                        # transpose to change shape from (bands, rows, columns) to (rows, columns, bands)
                        img[:, :, :len(bands)] = np.transpose(data, [1, 2, 0])
                        # model matrix transforms coordinates inside the square (0,1) to coordinates in
                        # pixels relatively to the dataset
                        self.model_matrix = matrix.from_rasterio_Affine(
                            ~model.loader.dataset.transform
                            * vrt.transform
                            * rasterio.Affine.scale(*vrt.shape[::-1]))
                        self.context.makeCurrent(self.offscreen_surface)
                        self.program.bind()
                        self.program.setUniformValue('model_matrix',
                                                     QMatrix4x4(matrix.flatten(self.model_matrix)))
                        self.program.release()
                        self.context.doneCurrent()
                else:
                    img = np.empty((*file.shape, self.nb_band+1), dtype=np.float32)
                    data = file.read(bands, out_dtype=np.float32)
                    # transpose to change shape from (bands, rows, columns) to (rows, columns, bands)
                    img[:, :, :len(bands)] = np.transpose(data, [1, 2, 0])
                # if mask is missing
                if mask is None:
                    img[:, :, self.nb_band] = 1.
                # mask nodata values
                if all(x is not None for x in file.nodatavals):
                    img[:, :, self.nb_band][np.logical_or.reduce(
                        [img[:, :, i] == file.nodatavals[i] for i in range(self.nb_band)])] = 0.
                elif file.nodata is not None:
                    img[:, :, self.nb_band][np.logical_or.reduce(
                        [img[:, :, i] == file.nodata for i in range(self.nb_band)])] = 0.
                # transform from integer to float if needed
                for i, band in enumerate(bands):
                    if np.dtype(file.dtypes[file.indexes.index(band)]) == np.uint8:
                        img[:, :, i] = img[:, :, i] / 255
                # set the value of others band to 0 when mask is 0
                img[:, :, :self.nb_band][img[:, :, self.nb_band] == 0] = 0.
                # set the value of mask band to 1 when > 0
                img[:, :, self.nb_band][img[:, :, self.nb_band] > 0] = 1.
                # create the texture
                self.load_image(img)

    def load_image(self, img: np.ndarray):
        # shall be implented by subclasses
        raise NotImplementedError

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = super().to_dict(filedir)
        output["filepath"] = os.path.relpath(self.filepath, start=filedir)
        output["bands"] = self._bands
        output["mask"] = self._mask
        return output


class Raster1BLayer(RasterLayer):

    icon: QIcon = QIcon()
    kind: str = "raster 1B layer"
    nb_band: int = 1
    outlier_threshold = Loader.outlier_threshold
    autorange_threshold = ColormapWidget.autorange_threshold

    def __init__(self, name: str, model: "MapModel", filepath: str, band: int = 1,
                 mask: Optional[int] = None):
        if self.icon.isNull():
            # cannot be initialized in the class declaration because:
            # "QIcon needs a QGuiApplication instance before the icon is created." see QIcon doc
            Raster1BLayer.icon = QIcon('icons:raster1B.svg')
        self.colormap: ColorMap = my_colormaps[[c.name for c in my_colormaps].index('greyscale')]
        self.colormap_v0: float = 0.  # minimum value for colorbar range (default 5 percentile)
        self.colormap_v1: float = 1.  # maximum value for colorbar range (default 95 percentile)
        super().__init__(name, model, filepath, [band], mask)
        with warnings.catch_warnings():
            # ignore RuntimeWarning for slices that contain only nans
            warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning,
                                    message="Dataset has no geotransform, gcps, or rpcs. The identity matrix will be returned.")
            with rasterio.open(filepath) as file:
                band_description = file.descriptions[file.indexes.index(band)]
                self.band: str = (f"{band} ({band_description})"
                                  if band_description is not None else
                                  f"{band}")
                self.mask: str
                if mask is None:
                    self.mask = "None"
                else:
                    mask_description = file.descriptions[file.indexes.index(mask)]
                    self.mask = (f"{mask} ({mask_description})"
                                 if mask_description is not None else
                                 f"{mask}")
        self.add_child(TreeItemAttribute(self, "band", tooltip=self.band, editable=False))
        self.add_child(TreeItemAttribute(self, "mask", tooltip=self.mask, editable=False))
        self.set_colormap(self.colormap)
        self.add_child(TreeItemColormapAttribute(self, "colormap", tooltip="colormap"))

    def load_image(self, img: np.ndarray):
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        h, w, d = img.shape
        self.context.makeCurrent(self.offscreen_surface)
        texture = QOpenGLTexture(QOpenGLTexture.Target2D)
        texture.setMagnificationFilter(QOpenGLTexture.Nearest)
        texture.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        texture.setWrapMode(QOpenGLTexture.ClampToEdge)
        texture.setSize(w, h)
        texture.setFormat(QOpenGLTexture.RG32F)
        texture.allocateStorage(QOpenGLTexture.RG, QOpenGLTexture.Float32)
        texture.setData(QOpenGLTexture.RG, QOpenGLTexture.Float32, img)
        texture.generateMipMaps()
        self.context.doneCurrent()
        assert texture.textureId() != 0, f"{self.name} layer: cannot load image texture in OpenGl"
        self.set_texture(GL_TEXTURE0+DATA_UNIT, texture)
        # compute histogram
        self.histogram = self.compute_histogram(img)
        # compute v0 v1
        self.set_v0_v1(*self.autorange_from_hist(*self.histogram))

    def compute_histogram(self, img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        data = img[:, :, 0][img[:, :, 1] > 0]
        # build bins excluding the most extreme percentiles
        bins = np.histogram_bin_edges(data, bins="fd", range=np.percentile(data, [1, 99]))
        # add bins at the start and end for outliers
        bins = np.array([np.min(data), *bins, np.max(data)])
        return np.histogram(data, bins=bins)

    autorange_from_hist = ColormapWidget.autorange_from_hist

    def build_program(self) -> None:
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, VERT_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, PALETTE_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, ALPHA_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, MAP_SHADER)
        self.program.link()
        self.program.bind()
        self.program.setUniformValue('model_matrix', QMatrix4x4(matrix.flatten(self.model_matrix)))
        self.program.setUniformValue('values', DATA_UNIT)
        self.program.setUniformValue('palette', PALETTE_UNIT)
        self.program.setUniformValue('v0', self.colormap_v0)
        self.program.setUniformValue('v1', self.colormap_v1)
        self.program.release()

    @pyqtSlot(ColorMap)
    def set_colormap(self, colormap: ColorMap) -> None:
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        self.colormap = colormap
        self.context.makeCurrent(self.offscreen_surface)
        old_texture = self.textures.get(GL_TEXTURE0+PALETTE_UNIT, None)
        if old_texture is not None:
            old_texture.destroy()
        colormap_texture = create_colormap_texture(colormap)
        self.context.doneCurrent()
        self.set_texture(GL_TEXTURE0+PALETTE_UNIT, colormap_texture)

    @pyqtSlot(float, float)
    def set_v0_v1(self, v0: float, v1: float) -> None:
        self.colormap_v0 = v0
        self.colormap_v1 = v1
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        self.context.makeCurrent(self.offscreen_surface)
        self.program.bind()
        self.program.setUniformValue('v0', self.colormap_v0)
        self.program.setUniformValue('v1', self.colormap_v1)
        self.program.release()
        self.context.doneCurrent()

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = super().to_dict(filedir)
        output["colormap"] = self.colormap.name
        output["colormap_v0"] = self.colormap_v0
        output["colormap_v1"] = self.colormap_v1
        return output

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "Raster1BLayer":
        assert input_dict["kind"] == cls.kind
        assert "filepath" in input_dict
        name = input_dict.get("name", "raster1B layer")
        bands = input_dict.get("bands", [1])
        mask = input_dict.get("mask", None)
        layer = Raster1BLayer(name, map_model, input_dict["filepath"], bands[0], mask)
        if "visible" in input_dict:
            layer.visible = input_dict["visible"]
        if "alpha" in input_dict:
            layer.alpha = input_dict["alpha"]
        if "colormap" in input_dict:
            try:
                colormap = my_colormaps[[c.name for c in my_colormaps].index(
                    input_dict["colormap"])]
                layer.set_colormap(colormap)
            except ValueError:
                pass
        if "colormap_v0" in input_dict and "colormap_v1" in input_dict:
            v0, v1 = input_dict["colormap_v0"], input_dict["colormap_v1"]
            if isinstance(v0, float) and isinstance(v1, float):
                layer.set_v0_v1(v0, v1)
            else:
                logger.warning(f"layer {name}: colormap_v0 and/or colormap_v1 are not float, thus"
                               " they are ignored")
        return layer


class RasterRGBLayer(RasterLayer):

    icon: QIcon = QIcon()
    kind: str = "raster RGB layer"
    nb_band: int = 3

    def __init__(self, name: str, model: "MapModel", filepath: str, R: int = 1, G: int = 2,
                 B: int = 3, mask: Optional[int] = None):
        if self.icon.isNull():
            # cannot be initialized in the class declaration because:
            # "QIcon needs a QGuiApplication instance before the icon is created." see QIcon doc
            RasterRGBLayer.icon = QIcon('icons:rasterRGB.svg')
        super().__init__(name, model, filepath, [R, G, B], mask)
        with warnings.catch_warnings():
            # ignore RuntimeWarning for slices that contain only nans
            warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning,
                                    message="Dataset has no geotransform, gcps, or rpcs. The identity matrix will be returned.")
            with rasterio.open(filepath) as file:
                R_description = file.descriptions[file.indexes.index(R)]
                self.R: str = (f"{R} ({R_description})"
                               if R_description is not None else
                               f"{R}")
                G_description = file.descriptions[file.indexes.index(G)]
                self.G: str = (f"{R} ({G_description})"
                               if G_description is not None else
                               f"{G}")
                B_description = file.descriptions[file.indexes.index(B)]
                self.B: str = (f"{B} ({B_description})"
                               if B_description is not None else
                               f"{B}")
                self.mask: str
                if mask is None:
                    self.mask = "None"
                else:
                    mask_description = file.descriptions[file.indexes.index(mask)]
                    self.mask = (f"{mask} ({mask_description})"
                                 if mask_description is not None else
                                 f"{mask}")
        self.add_child(TreeItemAttribute(self, "R", tooltip=self.R, editable=False))
        self.add_child(TreeItemAttribute(self, "G", tooltip=self.G, editable=False))
        self.add_child(TreeItemAttribute(self, "B", tooltip=self.B, editable=False))
        self.add_child(TreeItemAttribute(self, "mask", tooltip=self.mask, editable=False))

    def load_image(self, img: np.ndarray):
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        h, w, d = img.shape
        self.context.makeCurrent(self.offscreen_surface)
        texture = QOpenGLTexture(QOpenGLTexture.Target2D)
        texture.setMagnificationFilter(QOpenGLTexture.Linear)
        texture.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        texture.setWrapMode(QOpenGLTexture.ClampToEdge)
        texture.setSize(w, h)
        texture.setFormat(QOpenGLTexture.RGBA32F)
        texture.allocateStorage(QOpenGLTexture.RGBA, QOpenGLTexture.Float32)
        texture.setData(QOpenGLTexture.RGBA, QOpenGLTexture.Float32, img)
        texture.generateMipMaps()
        self.context.doneCurrent()
        assert texture.textureId() != 0, f"{self.name} layer: cannot load image texture in OpenGl"
        self.set_texture(GL_TEXTURE0, texture)

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
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "RasterRGBLayer":
        assert input_dict["kind"] == cls.kind
        assert "filepath" in input_dict
        name = input_dict.get("name", "rasterRGB layer")
        bands = input_dict.get("bands", [1, 2, 3])
        mask = input_dict.get("mask", None)
        layer = RasterRGBLayer(name, map_model, input_dict["filepath"], bands[0], bands[1],
                               bands[2], mask)
        if "visible" in input_dict:
            layer.visible = input_dict["visible"]
        if "alpha" in input_dict:
            layer.alpha = input_dict["alpha"]
        return layer

############ WIIIIIIPPPPPPPP #####################


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
        img = self.load_geomap(model.loader)
        self.load_image(img)

    build_program = RasterRGBLayer.build_program

    def load_geomap(self, loader: Loader):
        """
        Download a tiled map

        Returns
        -------
        ndarray
            Image as a 4D array of RGBA values
        """
        assert loader.dataset is not None, "Loader.load_geomap: no dataset opened"
        wms = WebMapService('https://ows.terrestris.de/osm/service?')
        request = wms.getmap(layers=['OSM-WMS'],
                             bbox=loader.dataset.bounds,
                             srs=str(loader.dataset.crs),
                             size=loader.dataset.shape,
                             format='image/jpeg')
        with rasterio.MemoryFile(request) as memfile:
            with memfile.open() as img:
                img = img.read()
                if img.dtype == "uint8":
                    img = img.astype(np.float32)/255
                # change img.shape from (bands, rows, columns) to (rows, columns, bands)
                img = np.transpose(img, [1, 2, 0]).copy().astype(np.float32)
                return img

    def load_image(self, img: np.ndarray):
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        h, w, d = img.shape
        self.context.makeCurrent(self.offscreen_surface)
        texture = QOpenGLTexture(QOpenGLTexture.Target2D)
        texture.setMagnificationFilter(QOpenGLTexture.Linear)
        texture.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        texture.setWrapMode(QOpenGLTexture.ClampToEdge)
        texture.setSize(w, h)
        texture.setFormat(QOpenGLTexture.RGB32F)
        texture.allocateStorage(QOpenGLTexture.RGB, QOpenGLTexture.Float32)
        texture.setData(QOpenGLTexture.RGB, QOpenGLTexture.Float32, img)
        texture.generateMipMaps()
        self.context.doneCurrent()
        assert texture.textureId() != 0, f"{self.name} layer: cannot load image texture in OpenGl"
        self.set_texture(GL_TEXTURE0, texture)

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
