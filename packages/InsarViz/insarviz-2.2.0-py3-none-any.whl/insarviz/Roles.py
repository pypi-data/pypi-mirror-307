#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:52:25 2024

@author: thomcoli
"""

from enum import IntEnum, auto

from PyQt5.QtCore import Qt


class Roles(IntEnum):
    # used by Selection.SelectionFolder and LayerView.ProxyLayerModel
    FolderRole = Qt.UserRole
    # used by Selection.SelectionItem
    ShowCurveRole = auto()
    # used by Selection.SelectionProfile
    ProfileTemporalRole = auto()
    ProfileSpatialRole = auto()
    # used by LayerModel.TreeItemAttribute
    EditorRole = auto()  # used by LayerView.ItemDelegate
    DataRole = auto()
    # used by LayerModel.TreeItemAttribute as DataRole and PlotModel/PlotView
    ComputeDataRole = auto()
    CurveColorRole = auto()
