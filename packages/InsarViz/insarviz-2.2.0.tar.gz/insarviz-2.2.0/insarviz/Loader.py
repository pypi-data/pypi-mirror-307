#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Loader

This module manages data loading from a file.
Contains the class:
    * Loader
and its methods:
    * open - open data file and store dataset
    * __len__ - length of dataset (# of bands or dates)
    * _dates - list of dates or list of band #
    * load_band - load one band data (all points) from file
    * load_profile - load one point data (all dates) from file
    * get_metadata - get metadata from file if exists
"""

from typing import Optional, Union

import logging

import time

import threading

import datetime

import warnings

import numpy as np

import rasterio
import rasterio.warp

from owslib.wms import WebMapService

from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool


logger = logging.getLogger(__name__)


# data ######################################################################

class Loader(QObject):

    # used to find the outliers: values outside
    # [q25 - outlier_threshold*IQR, q75 + outlier_threshold*IQR]
    outlier_threshold = 4  # classicaly 1.5, but a higher value seems nicer

    # emited when a dataset is opened, pass the starting band index
    data_loaded = pyqtSignal(int)
    data_units_loaded = pyqtSignal(str)
    histograms_computed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.filepath: Optional[str] = None
        self.dataset: Optional[rasterio.DatasetReader] = None
        self.read_lock = threading.Lock()
        self.metadata: dict[str, str] = {}
        self.dates: Union[list[datetime.datetime], list[int]] = []
        self.timestamps: Optional[np.ndarray] = None  # array of floats representing self.dates
        self.units: str = ""
        self.total_histogram: Optional[tuple[np.ndarray, np.ndarray]] = None
        self.band_histograms: list[tuple[np.ndarray, np.ndarray]] = []

    def open(self, filepath: str) -> None:
        """
        Open data file and store dataset.
        Print dataset attributes.

        Parameters
        ----------
        filepath : str, path
            Name of the file to load (with path).
        """
        filepath = str(filepath)
        with warnings.catch_warnings():
            # ignore RuntimeWarning for slices that contain only nans
            warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning,
                                    message="Dataset has no geotransform, gcps, or rpcs. The identity matrix will be returned.")
            self.dataset = rasterio.open(filepath)
        print("opened", filepath)
        self.filepath = filepath
        profile = self.dataset.profile
        for attr in profile:
            print(attr, profile[attr])
        self.get_metadata(filepath)
        # value units
        try:
            self.units = self.dataset.tags()['VALUE_UNIT']
            logger.info(f'Value unit "{self.units}" found in dataset VALUE_UNIT tag')
        except KeyError:
            logger.info(f"{self.filepath} missing VALUE_UNIT dataset tag")
            try:
                #  TODO ugly fix because flatsim has problems in its metadata
                self.units = self.metadata['Value_unit'].split(",")[0]
                logger.info(f'value unit "{self.units}" found in .meta file')
            except KeyError:
                self.units = 'Undefined units'
                logger.info(f'no value unit found, taking "{self.units}" instead')
        self.data_units_loaded.emit(self.units)
        # dates and timestamps
        try:
            self.dates = [datetime.datetime.strptime(str(self.dataset.tags(i)["DATE"]), "%Y%m%d")
                          for i in self.dataset.indexes]
            self.timestamps = np.array([d.timestamp() for d in self.dates], dtype=float)
            logger.info("dates found in DATE band tags")
        except (KeyError, ValueError) as error:
            if isinstance(error, KeyError):
                logger.info(f"{self.filepath} missing DATE band tags")
            if isinstance(error, ValueError):
                logger.info(f"{self.filepath} DATE band tags are not well formated (%Y%m%d expected"
                            ' as for example "20240827", see '
                            'https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)')
            try:
                self.dates = [datetime.datetime.strptime(x[-8:], "%Y%m%d")
                              for x in self.dataset.descriptions]
                self.timestamps = np.array([d.timestamp() for d in self.dates], dtype=float)
                logger.info("dates found in band descriptions (last 8 characters)")
            except (ValueError, TypeError):
                logger.info("no date found, taking band numbers as indexes instead")
                self.dates = self.dataset.indexes
                self.timestamps = np.array(self.dates, dtype=float)
        self.total_histogram = (np.array([]), np.array([]))
        self.band_histograms = [(np.array([]), np.array([])) for i in range(len(self))]
        print('number of bands = ', len(self))
        self.data_loaded.emit(self.dataset.indexes[len(self)//2])

    def close(self) -> None:
        if self.dataset is not None:
            logger.info(f"closing {self.filepath}")
            self.dataset.close()
        self.filepath = None
        self.metadata = {}
        self.dates = []
        self.timestamps = None
        self.units = ""

    def __len__(self) -> int:
        """
        Length of dataset = number of bands/dates.

        Returns
        -------
        int
            number of band/dates.
        """
        assert self.dataset is not None, "Loader.len: no dataset opened"
        return len(self.dataset.indexes)

    def compute_histograms(self, binrange: Optional[tuple[float, float]] = None) -> QRunnable:
        """
        _summary_

        Parameters
        ----------
        bands : Optional[Union[int], list[int]], optional
            Indexes of dataset bands to sample, by default None meaning all bands.
        """
        assert self.dataset is not None, "Loader.compute_histogram: no dataset opened"
        assert self.filepath is not None

        class Signals(QObject):
            progress = pyqtSignal(int)
            done = pyqtSignal(tuple, list)

        class Task(QRunnable):

            def __init__(self, dataset: rasterio.io.DatasetReader, read_lock: threading.Lock,
                         binrange: Optional[tuple[float, float]] = None):
                super().__init__()
                self.dataset = dataset
                self.read_lock = read_lock
                self.binrange = binrange
                self.signals = Signals()

            def run(self):
                # intialize progress dialog
                t0 = time.time()
                # xy is an array of (row, col, band) positions to randomly sample the dataset
                sample_size = 20000
                xy = np.random.randint([self.dataset.height, self.dataset.width,
                                        len(self.dataset.indexes)], size=(sample_size, 3))
                self.signals.progress.emit(5)
                # sort xy to optimize dataset sampling (split between interleaving cases)
                if len(set(self.dataset.block_shapes)) == 1:
                    # block shape is the same across bands
                    block_height, block_width = self.dataset.block_shapes[0]
                    if self.dataset.interleaving == rasterio.enums.Interleaving.pixel:
                        # sort xy first by block row, second by block column
                        xy = xy[np.lexsort((xy[:, 1] // block_width, xy[:, 0] // block_height))]
                    elif (self.dataset.interleaving == rasterio.enums.Interleaving.band
                          or (self.dataset.driver == 'VRT' and self.dataset.interleaving is None)):
                        # sort xy first by band, second by block row, third by block column
                        xy = xy[np.lexsort(
                            (xy[:, 1] // block_width, xy[:, 0] // block_height, xy[:, 2]))]
                    else:
                        raise NotImplementedError(
                            f"interleaving:{self.dataset.interleaving} not implemented")
                else:
                    # block shape is not the same across bands so interleaving must be band
                    assert self.dataset.interleaving == rasterio.enums.Interleaving.band
                    # sort xy by band
                    xy = xy[np.lexsort((xy[:, 2]))]
                self.signals.progress.emit(10)
                # sample the dataset
                sample = np.empty(sample_size)
                for i in range(4):
                    # split in 4 steps to update the progress dialog
                    start = (i * sample_size) // 4
                    stop = ((i+1) * sample_size) // 4
                    with self.read_lock:
                        sample[start:stop] = np.array([self.dataset.read(
                            self.dataset.indexes[k[2]],
                            window=rasterio.windows.Window(k[1], k[0], 1, 1))[0][0]
                            for k in xy[start:stop]])
                    self.signals.progress.emit(10 + (i+1)*2)
                if self.dataset.nodata is not None:
                    sample = sample[sample != self.dataset.nodata]
                # compute the histogram bins on the sample
                # get the first and third quartiles (inverted_cdf means exact observation)
                q25, q75 = np.percentile(sample, [25, 75], method="inverted_cdf")
                # interquartile range
                IQR = q75 - q25
                # Freedman Diaconis Estimator of the binwidth
                binwidth = 2 * IQR / (np.cbrt(len(sample)))
                if self.binrange is None:
                    # range exclude outliers, ie observations outside of
                    # [q25 - outlier_threshold*IQR, q75 + outlier_threshold*IQR]
                    self.binrange = (q25 - Loader.outlier_threshold*IQR,
                                     q75 + Loader.outlier_threshold*IQR)
                # compute the bin count as in np.histogram_bin_edges
                bincount = int(np.round(np.ceil((self.binrange[1] - self.binrange[0]) / binwidth)))
                # compute the bins
                bins = np.histogram_bin_edges(sample, bins=bincount, range=self.binrange)
                # add a bin at the start and end for outliers
                bins_total = np.array([bins[0], *bins, bins[-1]])
                bins_band = [np.array([bins[0], *bins, bins[-1]])
                             for _ in range(len(self.dataset.indexes))]
                self.signals.progress.emit(20)
                # build the histograms (split between interleaving cases)
                nd = self.dataset.profile['nodata']
                histogram_total = np.zeros(bins_total.shape[0]-1)
                histograms_band = [np.zeros(bins_band[i].shape[0]-1)
                                   for i in range(len(self.dataset.indexes))]
                with warnings.catch_warnings():
                    # ignore RuntimeWarning for slices that contain only nans
                    warnings.filterwarnings("ignore", category=RuntimeWarning,
                                            message="All-NaN slice encountered")
                    if self.dataset.interleaving == rasterio.enums.Interleaving.pixel:
                        # pixel interleaving => open block by block
                        assert len(set(self.dataset.block_shapes)) == 1
                        block = np.empty((len(self.dataset.indexes), *self.dataset.block_shapes[0]))
                        block_count = sum(1 for _ in self.dataset.block_windows())
                        for k, window in enumerate(self.dataset.block_windows()):
                            with self.read_lock:
                                block = self.dataset.read(window=window[1], out=block)
                            block[block == nd] = np.nan
                            for i in range(len(self.dataset.indexes)):
                                tmp_min = np.nanmin(block[i])
                                bins_total[0] = np.nanmin((tmp_min, bins_total[0]))
                                bins_band[i][0] = np.nanmin((tmp_min, bins_band[i][0]))
                                tmp_max = np.nanmax(block[i])
                                bins_total[-1] = np.nanmax((tmp_max, bins_total[-1]))
                                bins_band[i][-1] = np.nanmax((tmp_max, bins_band[i][-1]))
                                tmp_hist = np.histogram(block[i], bins=bins_band[i])[0]
                                histograms_band[i] += tmp_hist
                                histogram_total += tmp_hist
                            self.signals.progress.emit(20 + (80 * k) // block_count)
                    else:
                        # band interleaving or no interleaving metadata => open band by band
                        band = np.empty(self.dataset.shape)
                        band_count = len(self.dataset.indexes)
                        for i, idx in enumerate(self.dataset.indexes):
                            with self.read_lock:
                                band = self.dataset.read(idx, out=band)
                            band[band == nd] = np.nan
                            band_min = np.nanmin(band)
                            bins_total[0] = np.nanmin((band_min, bins_total[0]))
                            bins_band[i][0] = np.nanmin((band_min, bins_band[i][0]))
                            band_max = np.nanmax(band)
                            bins_total[-1] = np.nanmax((band_max, bins_total[-1]))
                            bins_band[i][-1] = np.nanmax((band_max, bins_band[i][-1]))
                            histograms_band[i] += np.histogram(band, bins=bins_band[i])[0]
                            histogram_total += histograms_band[i]
                            self.signals.progress.emit(20 + (80 * i) // band_count)
                # normalize the histograms in order to plot them in PaletteView
                for i, h in enumerate(histograms_band):
                    histograms_band[i] = h / sum(h)
                histogram_total = histogram_total / sum(histogram_total)
                t1 = time.time()
                logger.info(f"computed histograms in {t1-t0}s ({len(bins)-1} bins)")
                self.signals.progress.emit(100)
                self.signals.done.emit((histogram_total, bins_total),
                                       list(zip(histograms_band, bins_band)))
        task = Task(self.dataset, self.read_lock, binrange)
        task.signals.done.connect(self.set_histograms)
        QThreadPool.globalInstance().start(task)
        return task

    def set_histograms(self, total_histogram: tuple[np.ndarray, np.ndarray],
                       band_histograms: list[tuple[np.ndarray, np.ndarray]]) -> bool:
        assert self.dataset is not None
        if len(band_histograms) != len(self):
            logger.warning("number of band histograms not equal to number of bands")
            return False
        total_histogram = tuple([np.array(a) for a in total_histogram])
        if len(total_histogram[0].shape) != 1 or len(total_histogram[1].shape) != 1:
            logger.warning("total histogram is not an array of dimension 1")
            return False
        if len(total_histogram[1]) != len(total_histogram[0]) + 1:
            logger.warning("total histogram number of bins is not equal to number of values + 1")
            return False
        for i in range(len(self)):
            band_histograms[i] = tuple([np.array(a) for a in band_histograms[i]])
            if len(band_histograms[i][0].shape) != 1 or len(band_histograms[i][1].shape) != 1:
                logger.warning(f"band {self.dataset.indexes[i]} histogram is not an array of "
                               "dimension 1")
                return False
            if len(band_histograms[i][1]) != len(band_histograms[i][0]) + 1:
                logger.warning(
                    f"band {self.dataset.indexes[i]} histogram number of bins is not equal to "
                    "number of values + 1")
                return False
        self.total_histogram = total_histogram
        self.band_histograms = band_histograms
        self.histograms_computed.emit()
        return True

    def load_band(self, i: int = 0):
        """
        load band i from dataset
        print loading time

        Parameters
        ----------
        i : int, optional
            Band number to load. The default is 0.

        Returns
        -------
        band : array
            Loaded band data.
        TYPE
            nodata value in band i.
        TYPE
            type of data in band i.
        """
        assert self.dataset is not None, "Loader.load_band: no dataset opened"
        dataset = self.dataset
        assert i in self.dataset.indexes
        index = self.dataset.indexes.index(i)
        t0 = time.time()
        with self.read_lock:
            band = dataset.read(i)
        t1 = time.time()
        print('loaded band', i, 'in', t1-t0, 's')
        return band, dataset.profile.get('nodata', np.nan), dataset.dtypes[index]

    def load_profile_window(self, i_start: float, j_start: float, i_stop: Optional[float] = None,
                            j_stop: Optional[float] = None) -> np.ndarray:
        """
        TODO
        Load data corresponding to all bands/dates, at point (i,j)
        (texture/data coordinates)

        Parameters
        ----------
        i : float or int
            col number
        j : float or int
            row number

        Returns
        -------
        list[float]
            dataset values at point (i,j) (in texture/data coordinates)
            for all bands/dates.
        """
        assert self.dataset is not None, "Loader.load_profile_window: no dataset opened"
        i, j = int(i_start), int(j_start)
        width = abs(i_start - int(i_stop)) + 1 if i_stop else 1
        length = abs(j_start - int(j_stop)) + 1 if j_stop else 1
        with self.read_lock:
            data = self.dataset.read(self.dataset.indexes,
                                     window=rasterio.windows.Window(i, j, width, length))
        # set nodata to nan
        nd = self.dataset.profile.get('nodata', np.nan)
        data[data == nd] = np.nan
        with warnings.catch_warnings():
            # ignore RuntimeWarning for slices that contain only nans
            warnings.filterwarnings("ignore", category=RuntimeWarning,
                                    message="Mean of empty slice")
            data = np.nanmean(data, axis=(1, 2))
        return data

    def get_metadata(self, filename: str) -> None:
        """
        Create a dictionnary containing all metadata entries in self.matadata,
        if a '.meta' file exists in same repo as the datacube file

        Parameters
        ----------
        filename : str
            name of the datacube file
        """
        metafilename = filename.split('.')[0] + '.meta'
        self.metadata = {}
        try:
            with open(metafilename, encoding="utf-8") as f:
                for line in f:
                    # TODO error if blank lines
                    (key, val) = line.split(sep=': ', maxsplit=1)
                    self.metadata[key] = val.strip()
        except FileNotFoundError:
            print('no metadata file found')
