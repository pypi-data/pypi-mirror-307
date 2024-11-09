# -*- coding: utf-8 -*-

""" PaletteView

This module handles the creation of the Palette view: an interactive plot
of the distribution of data values and its corresponding color scheme
Also handles user interactions with it (change color gradient and its
correspondance with data values)

Contains class:
    * Palette
"""

# imports ##########################################################################################

from typing import Optional

import logging

import numpy as np

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QPushButton

from pyqtgraph import HistogramLUTWidget, BarGraphItem, LegendItem, GraphicsView
from pyqtgraph.widgets.ColorMapMenu import ColorMapMenu

from pyqtgraph.colormap import ColorMap

from insarviz.colormaps import my_colormaps


logger = logging.getLogger(__name__)


# ColormapWidget class #############################################################################

class ColormapWidget(QWidget):

    autorange_threshold = 0.02
    default_padding = 0.15
    max_padding = 0.4

    # connected to MapModel.set_v0_v1
    v0_v1_changed = pyqtSignal(float, float)
    # connected to MapModel.set_colormap
    colormap_changed = pyqtSignal(ColorMap)
    #
    compute_histograms = pyqtSignal(tuple)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.histogram_widget = HistogramWidget()
        # add a curve for total histogram
        self.total_hist_plot = BarGraphItem(x0=[], x1=[], y0=[], y1=[],
                                            pen=None, brush=(20, 20, 220, 100))
        self.total_hist_plot.setZValue(10)
        self.total_hist_plot.setRotation(90)
        self.histogram_widget.vb.addItem(self.total_hist_plot)
        # add a curve for band histogram
        # (total data histogram use the base HistogramLUTWidget mono curve: self.plot)
        self.band_hist_plot = BarGraphItem(x0=[], x1=[], y0=[], y1=[],
                                           pen=None, brush=(220, 20, 20, 100))
        self.band_hist_plot.setZValue(10)
        self.band_hist_plot.setRotation(90)
        self.histogram_widget.vb.addItem(self.band_hist_plot)
        # legend
        self.legend = LegendItem()
        self.legend.addItem(self.total_hist_plot, "all bands")
        self.legend.addItem(self.band_hist_plot, "current band")
        self.legend_widget = GraphicsView(parent=parent)
        self.legend_widget.setCentralWidget(self.legend)
        # toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setOrientation(Qt.Vertical)
        self.autorange_total_button: QPushButton = QPushButton("Autorange all bands", self)
        self.autorange_total_button.setToolTip("Automatically adjust the colormap mapping using the"
                                               " all band histogram")
        self.autorange_total_button.clicked.connect(self.autorange_total)
        self.toolbar.addWidget(self.autorange_total_button)
        self.autorange_band_button: QPushButton = QPushButton("Autorange current band", self)
        self.autorange_band_button.setToolTip("Automatically adjust the colormap mapping using the"
                                              " current band histogram")
        self.autorange_band_button.clicked.connect(self.autorange_band)
        self.toolbar.addWidget(self.autorange_band_button)
        self.compute_histogram_button: QPushButton = QPushButton("Recompute histograms", self)
        self.compute_histogram_button.setToolTip(
            "Recompute the histograms using the area to define outliers")
        self.compute_histogram_button.clicked.connect(
            lambda: self.compute_histograms.emit(self.histogram_widget.getLevels()))
        self.toolbar.addWidget(self.compute_histogram_button)
        # layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.histogram_widget, stretch=1)
        self.main_layout.addWidget(self.legend_widget)
        self.setLayout(self.main_layout)
        # internal signal and slots
        self.histogram_widget.sigLevelsChanged.connect(
            lambda _: self.v0_v1_changed.emit(*self.histogram_widget.getLevels()))
        self.histogram_widget.gradient.menu.sigColorMapTriggered.connect(
            self.colormap_changed.emit)
        # set disabled
        self.setDisabled(True)

    def sizeHint(self) -> QSize:
        return QSize(self.minimumWidth(), self.minimumHeight())

    @pyqtSlot(np.ndarray, np.ndarray)
    def set_total_histogram(self, hist: np.ndarray, bins: np.ndarray) -> None:
        self.total_hist_plot.setOpts(x0=bins[:-1], x1=bins[1:], y0=np.zeros(len(hist)), y1=hist)
        if len(hist) == 0:
            return
        self.autorange_total()
        self.histogram_widget.vb.setYRange(bins[1], bins[-2], padding=self.default_padding)
        ymin = float(bins[0] - (bins[-1] - bins[0]) * self.max_padding)
        ymax = float(bins[-1] + (bins[-1] - bins[0]) * self.max_padding)
        self.histogram_widget.vb.setLimits(yMin=ymin, yMax=ymax)

    @pyqtSlot(np.ndarray, np.ndarray)
    def set_band_histogram(self, hist: np.ndarray, bins: np.ndarray) -> None:
        self.band_hist_plot.setOpts(x0=bins[:-1], x1=bins[1:], y0=np.zeros(len(hist)), y1=hist)

    def autorange_from_hist(self, hist: np.ndarray, bins: np.ndarray) -> tuple[float, float]:
        assert len(hist) > 2 and len(hist)+1 == len(bins)
        # get the first index where the histogram cumulative sum is greater than threshold
        idx_v0 = np.where(np.cumsum(hist) > self.autorange_threshold)[0][0]
        # take the maximum between this index and 1 to skip the left outlier bin
        idx_v0 = np.max((1, idx_v0))
        # get the left boundary of this bin (hence the [:-1] to get the left boundaries)
        v0 = bins[:-1][idx_v0]
        # get the last index where the histogram backward cumulative sum is greater than threshold
        # (backward hence hist[::-1], and to get the correct index in the backward cumulative sum
        # has to be inversed again hence the second [::-1])
        idx_v1 = np.where(np.cumsum(hist[::-1])[::-1] > self.autorange_threshold)[0][-1]
        # take the minimum between this index and the len -2 to skip the right outlier bin
        idx_v1 = np.min((len(hist) - 2, idx_v1))
        # get the right boundary of this bin (hence the [1:] to get the right boundaries)
        v1 = bins[1:][idx_v1]
        return (v0, v1)

    @pyqtSlot()
    def autorange_total(self) -> None:
        hist = self.total_hist_plot.opts.get('y1')
        if len(hist) == 0:
            return
        bins = np.empty(len(hist)+1)
        bins[:-1] = self.total_hist_plot.opts.get('x0')
        bins[-1] = self.total_hist_plot.opts.get('x1')[-1]
        v0, v1 = self.autorange_from_hist(hist, bins)
        self.histogram_widget.setLevels(v0, v1)

    @pyqtSlot()
    def autorange_band(self) -> None:
        hist = self.band_hist_plot.opts.get('y1')
        if len(hist) == 0:
            return
        bins = np.empty(len(hist)+1)
        bins[:-1] = self.band_hist_plot.opts.get('x0')
        bins[-1] = self.band_hist_plot.opts.get('x1')[-1]
        v0, v1 = self.autorange_from_hist(hist, bins)
        self.histogram_widget.setLevels(v0, v1)

    # connected to Loader.data_units_loaded
    @pyqtSlot(str)
    def set_data_units(self, units: str) -> None:
        self.histogram_widget.axis.setLabel("LOS Displacement", units=units)

    @pyqtSlot(float, float)
    def set_v0_v1(self, v0: float, v1: float) -> None:
        self.histogram_widget.setLevels(v0, v1)

    def set_default_colormap(self) -> None:
        # greyscale is the first colormap action (see colormaps.py)
        self.histogram_widget.gradient.menu.actions()[0].trigger()

    @pyqtSlot(str)
    def set_colormap(self, name: str) -> None:
        for action in self.histogram_widget.gradient.menu.actions():
            if self.histogram_widget.gradient.menu.actionDataToColorMap(action.data()).name == name:
                action.trigger()
                return
        logger.warning(f"colormap {name} not found, switch to greyscale")
        self.set_default_colormap()


class HistogramWidget(HistogramLUTWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent, levelMode='mono', gradientPosition='right',
                         orientation='vertical')
        # remove the default gradient menu of pyqtgraph.GradientEditorItem
        del self.gradient.menu
        # create custom gradient menu with chosen default colormaps + our owns
        self.gradient.menu = ColorMapMenu(userList=my_colormaps)
        # remove the None action (that selects a greyscale colormap)
        self.gradient.menu.removeAction(self.gradient.menu.actions()[0])
        # connect gradient menu action as in pyqtgraph.GradientEditorItem
        self.gradient.menu.sigColorMapTriggered.connect(self.gradient.colorMapMenuClicked)
        # remove the ticks of gradient
        self.gradient.showTicks(False)
        # set minimum width so that colorbar is not hidden when minimized
        self.setMinimumWidth(115)
        self.setMaximumWidth(250)
        # move the region indicator to background
        self.region.setZValue(-1)
        # remove the default histogram curve
        self.vb.removeItem(self.plot)
