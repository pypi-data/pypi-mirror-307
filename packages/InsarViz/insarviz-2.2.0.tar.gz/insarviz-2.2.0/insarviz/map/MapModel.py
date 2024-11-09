#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""MapModel

This module contains the MapModel class that manages data for the Map and
Minimap views (as in a Model/View architecture).
"""

# imports ###################################################################

from typing import Any, Optional

import logging

import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QModelIndex

from PyQt5.QtGui import QOpenGLContext, QOffscreenSurface, QOpenGLTexture

from OpenGL.GL import (
    GL_TEXTURE0
)

from OpenGL.constant import IntConstant

import numpy as np

from pyqtgraph.colormap import ColorMap

from insarviz.colormaps import create_colormap_texture

from insarviz.Loader import Loader

from insarviz.map.Shaders import DATA_UNIT, PALETTE_UNIT

from insarviz.map.LayerModel import LayerModel

from insarviz.map.Layer import Layer, MainLayer, Raster1BLayer, RasterRGBLayer, GeomapLayer  # TODO WIP
# from insarviz.map.GeomapLayer import GeomapLayer

from insarviz.map.Selection import SelectionLayer

import insarviz.version as version

logger = logging.getLogger(__name__)


# Map Model class ##################################################################################

class MapModel(QObject):
    """
    Model managing data for Map and Minimap
    """
    closed = pyqtSignal()
    opened = pyqtSignal()

    # connected to MainLayer.set_texture
    # (texture_unit, texture)
    texture_changed = pyqtSignal(IntConstant, QOpenGLTexture)

    # connected to MainLayer.set_v0_v1, Palette.setLevels
    v0_v1_changed = pyqtSignal(float, float)  # (v0, v1)

    #  connected to ColormapWidget.set_colormap
    request_colormap = pyqtSignal(str)

    # connected to ColormapWidget.set_XXX_histogram
    total_hist_changed = pyqtSignal(np.ndarray, np.ndarray)  # (values, bins)
    band_hist_changed = pyqtSignal(np.ndarray, np.ndarray)  # (values, bins)

    # connected to AbstractMapView.paint
    request_paint = pyqtSignal()

    # connected to AbstractMapView.set_view_center
    request_set_view_center = pyqtSignal(float, float)  # (cx, cy)

    def __init__(self, loader: Loader, context: QOpenGLContext,
                 offscreen_surface: QOffscreenSurface):
        """
        MapModel
        """
        super().__init__()
        self.loader = loader
        self.loader.data_loaded.connect(self.on_data_loaded)
        self.loader.histograms_computed.connect(self.on_histograms_computed)
        self.context = context  # QOpenGLContext shared with every other contexts
        self.offscreen_surface = offscreen_surface  # QOffscreenSurface to use OpenGL commands
        self.layer_model = LayerModel()
        self.layer_model.request_paint.connect(self.request_paint)
        self.textures: dict[int, int] = {}  # associate a band index to an openGL texture id
        self.histograms: dict[int, tuple[np.ndarray, np.ndarray]] = {}
        self.flip_h: bool = False  # image vertical flip state
        self.flip_v: bool = False  # image vertical flip state
        self.i: Optional[int] = None  # current band index (starting from 1 like in gdal)
        self.colormap: Optional[ColorMap] = None
        # OpenGL texture for colormap
        self.colormap_texture = QOpenGLTexture(QOpenGLTexture.Target1D)
        self.tex_width: int = 0  # data width (in pixels)
        self.tex_height: int = 0  # data height (in pixels)
        self.colormap_v0: float = 0.  # minimum value for colorbar range (default 5 percentile)
        self.colormap_v1: float = 1.  # maximum value for colorbar range (default 95 percentile)

    @pyqtSlot(int)
    def on_data_loaded(self, band_index: int) -> None:
        """
        TODO
        """
        assert self.loader.dataset is not None
        self.tex_width, self.tex_height = self.loader.dataset.width, self.loader.dataset.height
        assert band_index in self.loader.dataset.indexes
        self.i = band_index
        self.request_set_view_center.emit(self.tex_width/2, self.tex_height/2)

    @pyqtSlot()
    def on_histograms_computed(self) -> None:
        assert self.loader.total_histogram is not None
        self.total_hist_changed.emit(*self.loader.total_histogram)
        if self.i is not None:
            self.band_hist_changed.emit(*self.loader.band_histograms[self.i-1])

    def close(self) -> None:
        self.loader.close()
        # delete the OpenGL textures
        self.context.makeCurrent(self.offscreen_surface)
        for texture in self.textures.values():
            texture.destroy()
        self.colormap_texture.destroy()
        self.context.doneCurrent()
        self.textures = {}
        self.histograms = {}
        self.flip_h = False
        self.flip_v = False
        self.i = None
        self.tex_width = 0
        self.tex_height = 0
        self.colormap = None
        self.colormap_v0 = 0.
        self.colormap_v1 = 1.
        self.closed.emit()
        self.layer_model.clear()
        self.total_hist_changed.emit(np.array([]), np.array([]))
        self.band_hist_changed.emit(np.array([]), np.array([]))
        self.request_paint.emit()

    def create_base_layers(self) -> None:
        self.loader.compute_histograms()
        # initialize main_layer
        main_layer = MainLayer(self)
        self.layer_model.add_layer(main_layer)
        # initialize selection and selection_layer
        selection = SelectionLayer()
        self.layer_model.add_layer(selection, i=0)
        self.layer_model.set_selection(selection)
        self.request_colormap.emit("greyscale")
        self.v0_v1_changed.emit(self.colormap_v0, self.colormap_v1)
        self.show_band(self.i)

    def show_band(self, i: int) -> None:
        """
        Load, generate (if not existing) and show the texture of the ith band.

        Parameters
        ----------
        i : int
            Band/date number to be loaded and shown.

        Returns
        -------
        None.

        """
        assert self.loader.dataset is not None
        assert i in self.loader.dataset.indexes
        self.i = i
        # band data
        try:  # looking up cache
            self.textures[i]
        except KeyError:
            band, nd, dtype = self.loader.load_band(i)
            band = band.astype(np.float32)
            # band data
            bg = (band == nd)
            h, w = band.shape
            z = np.ones((h, w, 2), dtype='float32')
            z[:, :, 0] = band
            z[:, :, 0][bg] = 0.
            z[:, :, 1][bg] = 0.
            # band texture
            self.context.makeCurrent(self.offscreen_surface)
            texture = QOpenGLTexture(QOpenGLTexture.Target2D)
            texture.setMagnificationFilter(QOpenGLTexture.Nearest)
            texture.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
            texture.setWrapMode(QOpenGLTexture.ClampToEdge)
            texture.setSize(w, h)
            texture.setFormat(QOpenGLTexture.RG32F)
            texture.allocateStorage(QOpenGLTexture.RG, QOpenGLTexture.Float32)
            texture.setData(QOpenGLTexture.RG, QOpenGLTexture.Float32, z)
            texture.generateMipMaps()
            self.context.doneCurrent()
            assert texture.textureId(
            ), f"Map Model : cannot load image texture for band {i} in OpenGl"
            # store band texture param
            self.textures[i] = texture
        # send the arrays of the histogram (values and bins)
        self.band_hist_changed.emit(*self.loader.band_histograms[self.i - 1])
        self.texture_changed.emit(IntConstant("GL_TEXTURE0+DATA_UNIT", GL_TEXTURE0+DATA_UNIT),
                                  self.textures[i])
        self.request_paint.emit()

    # connected to PaletteView.palette_changed, called when user change color gradient
    @pyqtSlot(ColorMap)
    def set_colormap(self, colormap: ColorMap) -> None:
        self.colormap = colormap
        self.context.makeCurrent(self.offscreen_surface)
        self.colormap_texture.destroy()
        self.colormap_texture = create_colormap_texture(colormap)
        self.context.doneCurrent()
        self.texture_changed.emit(IntConstant("GL_TEXTURE0+PALETTE_UNIT", GL_TEXTURE0+PALETTE_UNIT),
                                  self.colormap_texture)
        self.request_paint.emit()

    # connected to PaletteView.v0_v1_changed
    @pyqtSlot(float, float)
    def set_v0_v1(self, v0: float, v1: float) -> None:
        # prevents infinite looping between MapModel and PaletteView
        if self.colormap_v0 != v0 or self.colormap_v1 != v1:
            self.colormap_v0 = v0
            self.colormap_v1 = v1
            self.v0_v1_changed.emit(v0, v1)
            self.request_paint.emit()

    # connected to MainWindow.flip_h_action
    @pyqtSlot(bool)
    def set_flip_h(self, checked: bool) -> None:
        self.flip_h = checked
        self.request_paint.emit()

    # connected to MainWindow.flip_v_action
    @pyqtSlot(bool)
    def set_flip_v(self, checked: bool) -> None:
        self.flip_v = checked
        self.request_paint.emit()

    def to_dict(self, filepath: str) -> dict[str, Any]:
        output: dict[str, Any] = {}
        output["insarviz"] = version.__version__
        filedir = os.path.dirname(filepath)  #  the directory where the json is saved
        assert isinstance(self.loader.filepath, str)
        output["dataset_path"] = os.path.relpath(self.loader.filepath, start=filedir)
        output["layers"] = [layer.to_dict(filedir) for layer in self.layer_model.layers]
        output["flip_h"] = self.flip_h
        output["flip_v"] = self.flip_v
        output["current_band"] = self.i
        assert isinstance(self.colormap, ColorMap)
        output["colormap"] = self.colormap.name
        output["colormap_v0"] = self.colormap_v0
        output["colormap_v1"] = self.colormap_v1
        # numpy arrays need to be transformed into list in order to be serialized in json
        assert self.loader.total_histogram is not None
        output["total_histogram"] = tuple([a.tolist() for a in self.loader.total_histogram])
        assert self.loader.band_histograms is not None
        output["band_histograms"] = [tuple([a.tolist() for a in b])
                                     for b in self.loader.band_histograms]
        return output

    def from_dict(self, input_dict: dict[str, Any], filepath: str) -> bool:
        assert self.loader.dataset is not None
        selection_layer: Optional[SelectionLayer] = None
        main_layer: Optional[MainLayer] = None
        for layer_dict in input_dict["layers"]:
            layer: Layer
            if layer_dict["kind"] == SelectionLayer.kind:
                if selection_layer is not None:
                    logger.warning("More than one selection layer")
                    self.close()
                    return False
                selection_layer = SelectionLayer.from_dict(layer_dict)
                layer = selection_layer
            elif layer_dict["kind"] == MainLayer.kind:
                if main_layer is not None:
                    logger.warning("More than one main data layer")
                    self.close()
                    return False
                main_layer = MainLayer.from_dict(layer_dict, self)
                layer = main_layer
            elif layer_dict["kind"] == Raster1BLayer.kind:
                if "filepath" not in layer_dict:
                    logger.warning(f'Layer {layer_dict["kind"]} "{layer_dict["name"]}"'
                                   ' miss the filepath field, skipping that layer')
                    continue
                layer_dict["filepath"] = os.path.join(
                    os.path.dirname(filepath), layer_dict.get("filepath"))
                layer = Raster1BLayer.from_dict(layer_dict, self)
            elif layer_dict["kind"] == RasterRGBLayer.kind:
                if "filepath" not in layer_dict:
                    logger.warning(f'Layer {layer_dict["kind"]} "{layer_dict["name"]}"'
                                   ' miss the filepath field, skipping that layer')
                    continue
                layer_dict["filepath"] = os.path.join(
                    os.path.dirname(filepath), layer_dict.get("filepath"))
                layer = RasterRGBLayer.from_dict(layer_dict, self)
            elif layer_dict["kind"] == GeomapLayer.kind:
                layer = GeomapLayer.from_dict(layer_dict, self)
            else:
                logger.warning(f'Unrecognized layer type {layer_dict["kind"]} '
                               f'for layer "{layer_dict["name"]}", skipping that layer')
                continue
            self.layer_model.add_layer(layer)
        if main_layer is None:
            logger.warning("Missing main data layer")
            self.close()
            return False
        if selection_layer is None:
            logger.warning("Missing selection layer")
            self.close()
            return False
        self.layer_model.set_selection(selection_layer)
        # send signals to fake the addition of the SelectionItems of the input_dict
        selection_index = self.layer_model.index(selection_layer.child_number(), 0, QModelIndex())
        points_folder_index = self.layer_model.index(selection_layer.points_folder.child_number(),
                                                     0, selection_index)
        if self.layer_model.rowCount(points_folder_index) > 0:
            self.layer_model.request_expand.emit(selection_index)
            self.layer_model.request_expand.emit(points_folder_index)
        profiles_folder_index = self.layer_model.index(
            selection_layer.profiles_folder.child_number(), 0, selection_index)
        if self.layer_model.rowCount(profiles_folder_index) > 0:
            self.layer_model.request_expand.emit(selection_index)
            self.layer_model.request_expand.emit(profiles_folder_index)
        references_folder_index = self.layer_model.index(
            selection_layer.references_folder.child_number(), 0, selection_index)
        if self.layer_model.rowCount(references_folder_index) > 0:
            self.layer_model.request_expand.emit(selection_index)
            self.layer_model.request_expand.emit(references_folder_index)
        self.flip_h = input_dict.get("flip_h", False)
        self.flip_v = input_dict.get("flip_v", False)
        self.i = input_dict.get("current_band", self.i)
        self.request_colormap.emit(input_dict.get("colormap", "greyscale"))
        if "total_histogram" in input_dict and "band_histograms" in input_dict:
            if not self.loader.set_histograms(input_dict["total_histogram"],
                                              input_dict["band_histograms"]):
                logger.warning("Histograms exist but are invalid")
                self.loader.compute_histograms()
        else:
            logger.info("Histograms are missing, computing them")
            self.loader.compute_histograms()
        self.colormap_v0 = input_dict.get("colormap_v0", self.colormap_v0)
        self.colormap_v1 = input_dict.get("colormap_v1", self.colormap_v1)
        self.v0_v1_changed.emit(self.colormap_v0, self.colormap_v1)
        if self.i not in self.loader.dataset.indexes:
            logger.warning(f"current_band {self.i} does not match any existing band, change to 1")
            self.i = 1
        return True
