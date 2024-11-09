#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" MapView

This module handles the creation of the Map view (image display of a band data)
 and user interactions with it (pan, zoom, data selection...).
 Works with the module MapModel (as in a Model/View architecture).

Contains class:
    * MapView
"""


# imports ###################################################################

from typing import Optional

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
)

from PyQt5.QtCore import QSize, pyqtSlot, pyqtSignal, Qt, QPoint, QPointF, QEvent

from PyQt5.QtWidgets import QToolTip, QWidget, QMenu, QAction, QActionGroup, QMessageBox

from PyQt5.QtGui import QPainter, QMouseEvent, QIcon, QCursor, QColor, QOpenGLVersionProfile

from insarviz.map.AbstractMapView import AbstractMapView

from insarviz.map.MapModel import MapModel

from insarviz.linalg import matrix

from insarviz.map.Selection import (
    SelectionItem, SelectionPoint, SelectionProfile, SelectionReference
)


# MapView #######################################################################

class MapView(AbstractMapView):

    size_threshold_confirmation_selection_item = 1000000

    POINTS: int = 1
    PROFILE: int = 2
    REF: int = 3

    # send the position of the mouse in data coordinate (int, int) and the band number to PlotModel
    pointer_changed = pyqtSignal(tuple, int)
    viewport_matrix_changed = pyqtSignal(object)
    interaction_changed = pyqtSignal(int)

    def __init__(self, map_model: MapModel, parent: QWidget):
        """
        Generate Map, a QOpenGLWidget display of the displacement data. Zoom
        level can be interactively set through mouse wheel or right-click+drag.
        View position on the Map can be interactively set through left-click+
        drag. View is synchronized to Minimap.

        Parameters
        ----------
        map_model : MapModel
            Model managing the data for Map and Minimap.
        """
        super().__init__(map_model, parent)
        # selection item that the user is creating before adding it to the selection layer
        self.selection_item: Optional[SelectionItem] = None
        self.setCursor(Qt.OpenHandCursor)
        self.menu = QMenu()
        self.action_group = QActionGroup(self)
        self.create_point_action = QAction("Create point", self)
        self.create_point_action.setIcon(QIcon('icons:points.png'))
        self.create_point_action.triggered.connect(self.create_point)
        self.menu.addAction(self.create_point_action)
        self.action_group.addAction(self.create_point_action)
        self.create_profile_action = QAction("Create profile", self)
        self.create_profile_action.setIcon(QIcon('icons:profile.png'))
        self.create_profile_action.triggered.connect(self.create_profile)
        self.menu.addAction(self.create_profile_action)
        self.action_group.addAction(self.create_profile_action)
        self.create_reference_action = QAction("Create reference", self)
        self.create_reference_action.setIcon(QIcon('icons:ref.png'))
        self.create_reference_action.triggered.connect(self.create_reference)
        self.menu.addAction(self.create_reference_action)
        self.action_group.addAction(self.create_reference_action)

    # opengl

    def sizeHint(self) -> QSize:
        return QSize(300, 300)

    def paintGL(self) -> None:
        """
        Generate and display OpenGL texture for Map.
        """
        version = QOpenGLVersionProfile(self.context().format())
        version.setVersion(4, 1)
        glfunc = self.context().versionFunctions(version)
        painter = QPainter(self)
        # FIX for issue #150
        # Qpainter seems to need to "paint" something in order for it to correctly give back the
        # global OpenGL state (I can't find why)
        painter.fillRect(0, 0, 0, 0, QColor("transparent"))
        # END FIX
        painter.beginNativePainting()
        glfunc.glClear(GL_COLOR_BUFFER_BIT)
        painter.endNativePainting()
        self.update_view_matrix()
        # layers is reversed so first layer is displayed last (i.e. upon the others)
        for layer in reversed(self.map_model.layer_model.layers):
            if layer.visible:
                layer.show(self.view_matrix, self.projection_matrix,
                           painter=painter, vao=self.vao, glfunc=glfunc)
        if self.selection_item is not None:
            self.selection_item.show(self.view_matrix, painter, preview=True)
        painter.end()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """
        TODO
        Overload method
        Set interaction mode according to user interaction type:
        In Interactive mode:
        - Left-click: pan
        - Right-click: zoom
        In Points and Profile modes:
        - Left-click: select points whose data will be shown in plots
        In Reference mode:
        - Left-click: first click selecs one px to be used as ref,
        subsequent clicks extend ref zone to rectangle with last point and
        new points as opposing corners.

        Update Map Model and Plot Model values accordingly

        Parameters
        ----------
        e : QMouseEvent
        """
        if (self.map_model.i is not None and (not self.left_drag) and (not self.right_drag)
                and self.selection_item is None):
            self.pointer_changed.emit((), None)
            if e.button() in (Qt.LeftButton, Qt.RightButton):
                self.p0 = *self.get_texture_coordinate(e.x(), e.y()), e.x(), e.y()
            if e.button() == Qt.LeftButton:
                if self.interaction == self.INTERACTIVE:
                    self.setCursor(Qt.ClosedHandCursor)
                else:
                    # check if pointer inside dataset
                    if ((0 <= self.p0[0] < self.map_model.tex_width)
                            and (0 <= self.p0[1] < self.map_model.tex_height)):
                        if self.interaction == self.POINTS:
                            self.create_point()
                        elif self.interaction == self.PROFILE:
                            self.create_profile()
                        elif self.interaction == self.REF:
                            self.create_reference()
            elif e.button() == Qt.RightButton:
                self.show_context_menu()
        super().mousePressEvent(e)
        # prevent right drag because right press launch context menu thus right release is missed
        self.right_drag = False

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """
        TODO
        Overload method

        Set interaction mode according to user interaction type and update
        Map view and model accordingly:
        In Interactive mode:
        - hovering: display tooltip: coordinates + data value(displacement)
        - Left-click+drag (pan): get new position and update Map view
        - Right-click+drag (zoom): get new zoom level and update Map view
        In Points mode:
        - hovering: display tooltip: coordinates + data value(displacement)
        - Left-click (+ optional drag): highlight selected points on Map,
        send coordinates to MapModel, send signal to update plots
        In Profile mode:
        - hovering: display tooltip: coordinates + data value(displacement)
        - Left-click: first click selects starting point of profile,
        subsequent clicks select end (or turning point) of profile, send
        coordinates to MapModel, send signal to update plots accordingly

        Parameters
        ----------
        e : QMouseEvent
        """
        # check if data loaded (needed when opening without data)
        if self.map_model.i is not None:
            if (not self.left_drag) and (not self.right_drag):
                self.p0 = *self.get_texture_coordinate(e.x(), e.y()), e.x(), e.y()
                i, j = int(self.p0[0]), int(self.p0[1])
                # check if pointer inside map
                if (0 <= i < self.map_model.tex_width) and (0 <= j < self.map_model.tex_height):
                    self.pointer_changed.emit((i, j), self.map_model.i)
                else:
                    self.pointer_changed.emit((), None)
            if self.interaction == self.INTERACTIVE:
                if self.left_drag:
                    # get the data coordinates of the point we are dragging
                    x0, y0, _, _ = self.p0
                    # get the data coordinates of where the cursor no is
                    x1, y1 = self.get_texture_coordinate(e.x(), e.y())
                    # make the difference between both and move the center of the view accordingly
                    dx, dy = x1-x0, y1-y0
                    self.pan(-dx, -dy)
            elif self.interaction == self.POINTS and self.left_drag:
                if self.selection_item is not None:
                    assert isinstance(self.selection_item, SelectionPoint)
                    x, y = self.get_texture_coordinate(e.x(), e.y())
                    dx = abs(int(x) - self.selection_item.x) + 1
                    dy = abs(int(y) - self.selection_item.y) + 1
                    r = min(max(dx, dy), self.selection_item.x+1, self.selection_item.y+1,
                            self.map_model.tex_width - self.selection_item.x,
                            self.map_model.tex_height - self.selection_item.y)
                    if self.selection_item.r != r:
                        self.selection_item.set_r(r)
                        self.paint()
            elif self.interaction == self.PROFILE:
                if self.selection_item is not None:
                    assert isinstance(self.selection_item, SelectionProfile)
                    x, y = self.get_texture_coordinate(e.x(), e.y())
                    x, y = int(x), int(y)
                    if (0 <= x < self.map_model.tex_width and 0 <= y < self.map_model.tex_height):
                        if (x != self.selection_item.points[-1][0] or
                                y != self.selection_item.points[-1][1]):
                            if len(self.selection_item.points) > 1:
                                self.selection_item.remove_last_point()
                            self.selection_item.add_point(x, y)
                            self.paint()
            elif self.interaction == self.REF and self.left_drag:
                if self.selection_item is not None:
                    assert isinstance(self.selection_item, SelectionReference)
                    x, y = self.get_texture_coordinate(e.x(), e.y())
                    x, y = int(x), int(y)
                    x = max(x, 0)
                    x = min(x, self.map_model.tex_width - 1)
                    y = max(y, 0)
                    y = min(y, self.map_model.tex_height - 1)
                    x0, y0 = int(self.p0[0]), int(self.p0[1])
                    left, right = min(x, x0), max(x, x0)
                    top, bottom = min(y, y0), max(y, y0)
                    if self.selection_item.get_rect() != (left, top, right, bottom):
                        self.selection_item.set_rect(left, top, right, bottom)
                        self.paint()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """
        TODO
        Overload method
        Set interaction mode according to user interaction type and update
        Map view and model accordingly:
        interaction mode set back to default (idle), keep plots if was
        profiling.

        Parameters
        ----------
        e : QMouseEvent
        """
        if self.interaction == self.INTERACTIVE and e.button() == Qt.LeftButton and self.left_drag:
            self.setCursor(Qt.OpenHandCursor)
        elif self.interaction == self.POINTS and e.button() == Qt.LeftButton:
            if self.selection_item is not None:
                assert isinstance(self.selection_item, SelectionPoint)
                size = (2*self.selection_item.r-1)**2
                if size > self.size_threshold_confirmation_selection_item:
                    if QMessageBox.question(self, "Insarviz",
                                            f"You are about to add a point of size {size}, it can "
                                            "take some time to compute its mean.\nAre you sure ?",
                                            QMessageBox.Cancel | QMessageBox.Ok,
                                            QMessageBox.Ok) == QMessageBox.Cancel:
                        self.selection_item = None
                        self.paint()
                        super().mouseReleaseEvent(e)
                        return None
                self.map_model.layer_model.add_selection_point(self.selection_item)
                self.selection_item = None
        elif self.interaction == self.PROFILE and e.button() == Qt.LeftButton:
            if self.selection_item is not None:
                assert isinstance(self.selection_item, SelectionProfile)
                if len(self.selection_item.points) > 1:
                    self.selection_item.remove_last_point()
                    x, y = self.get_texture_coordinate(e.x(), e.y())
                    x, y = int(x), int(y)
                    if (0 <= x < self.map_model.tex_width and 0 <= y < self.map_model.tex_height):
                        self.selection_item.add_point(x, y)
                        self.selection_item.add_point(x, y)
                        self.paint()
        elif self.interaction == self.PROFILE and e.button() == Qt.RightButton:
            if self.selection_item is not None:
                assert isinstance(self.selection_item, SelectionProfile)
                self.selection_item.remove_last_point()
                if len(self.selection_item.points) > 1:
                    self.map_model.layer_model.add_selection_profile(self.selection_item)
                self.selection_item = None
                self.paint()
        elif self.interaction == self.REF and e.button() == Qt.LeftButton:
            if self.selection_item is not None:
                assert isinstance(self.selection_item, SelectionReference)
                ref = self.selection_item
                size = (ref.right - ref.left + 1) * (ref.bottom - ref.top + 1)
                if size > self.size_threshold_confirmation_selection_item:
                    if QMessageBox.question(self, "Insarviz",
                                            f"You are about to add a reference of size {size}, it "
                                            "can take some time to compute its mean.\n"
                                            "Are you sure ?",
                                            QMessageBox.Cancel | QMessageBox.Ok,
                                            QMessageBox.Ok) == QMessageBox.Cancel:
                        self.selection_item = None
                        self.paint()
                        super().mouseReleaseEvent(e)
                        return None
                self.map_model.layer_model.add_selection_reference(self.selection_item)
                self.selection_item = None
        super().mouseReleaseEvent(e)

    def leaveEvent(self, event: QEvent) -> None:
        """
        TODO
        overload signal to reset (to nan) interactive curve when
        cursor leaves the Map

        Parameters
        ----------
        event : QEvent
        """
        super().leaveEvent(event)
        self.pointer_changed.emit((), None)

    def update_view_matrix(self) -> None:
        super().update_view_matrix()
        viewport_matrix = matrix.mul(self.view_matrix_inverse,
                                     matrix.scale(self.width(), self.height()))
        self.viewport_matrix_changed.emit(viewport_matrix)

    def show_context_menu(self):
        if ((0 <= self.p0[0] < self.map_model.tex_width)
                and (0 <= self.p0[1] < self.map_model.tex_height)):
            self.action_group.setEnabled(True)
        else:
            self.action_group.setDisabled(True)
        action = self.menu.exec(self.mapToGlobal(QPoint(self.p0[2], self.p0[3])))
        if action in (self.create_point_action, self.create_reference_action):
            # start left dragging to edit the newly created selection item
            # not required for profile because its edition does not use dragging
            self.left_drag = True
        # raise a mouseMoveEvent to update the position of the mouse after clicking on the menu
        event = QMouseEvent(QEvent.MouseMove, QPointF(self.mapFromGlobal(QCursor.pos())),
                            Qt.NoButton, Qt.NoButton, Qt.NoModifier)
        self.mouseMoveEvent(event)

    @pyqtSlot()
    def create_point(self):
        i, j = int(self.p0[0]), int(self.p0[1])
        assert (0 <= i < self.map_model.tex_width) and (0 <= j < self.map_model.tex_height)
        self.set_interaction(self.POINTS)
        self.selection_item = SelectionPoint(i, j, 1)
        self.paint()

    @pyqtSlot()
    def create_reference(self):
        i, j = int(self.p0[0]), int(self.p0[1])
        assert (0 <= i < self.map_model.tex_width) and (0 <= j < self.map_model.tex_height)
        self.set_interaction(self.REF)
        self.selection_item = SelectionReference(i, j)
        self.paint()

    @pyqtSlot()
    def create_profile(self):
        i, j = int(self.p0[0]), int(self.p0[1])
        assert (0 <= i < self.map_model.tex_width) and (0 <= j < self.map_model.tex_height)
        self.set_interaction(self.PROFILE)
        self.selection_item = SelectionProfile(i, j, 1)
        self.paint()

    @pyqtSlot(tuple)
    def update_mouse_tooltip(self, info: tuple) -> None:
        if info == ():
            QToolTip.hideText()
        else:
            x, y, _, value = info
            x_data, y_data, x_widget, y_widget = self.p0
            x_data, y_data = int(x_data), int(y_data)
            if (not x == x_data) or (not y == y_data):
                print("pointer info is too late")
                return None
            p = self.mapToGlobal(QPoint(x_widget, y_widget))
            # force the tooltip to update its position even if text remain the same
            # QToolTip.showText(p, "")
            QToolTip.showText(p, f"x:{x}\ny:{y}\nval:{value:.3f}")

    # interaction
    @pyqtSlot(int)
    def set_interaction(self, value: int) -> None:
        if value != self.interaction:
            self.selection_item = None
            if value == self.INTERACTIVE:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.CrossCursor)
            self.paint()
            super().set_interaction(value)
            self.interaction_changed.emit(value)
