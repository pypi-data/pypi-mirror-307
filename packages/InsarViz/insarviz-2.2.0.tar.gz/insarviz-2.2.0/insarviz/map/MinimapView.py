#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" MinimapView

This module handles the creation of the Minimap view (general image display
of a band data) and user interactions with it (pan and zoom).
Works with the module MapModel (as in a Model/View architecture).

Contains class:
* MinimapView
"""
# imports ###################################################################

from PyQt5.QtCore import Qt, QSize, QPoint, pyqtSignal, pyqtSlot

from PyQt5.QtGui import (
    QMouseEvent, QWheelEvent, QOpenGLVersionProfile, QOpenGLShaderProgram, QOpenGLShader,
    QMatrix4x4, QPolygon, QPainter, QPen, QColor
)

from PyQt5.QtWidgets import QWidget

import math

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_LINE_LOOP,
    GL_BLEND
)

from insarviz.map.AbstractMapView import AbstractMapView

from insarviz.map.MapModel import MapModel

from insarviz.map.Layer import MainLayer

from insarviz.map.Shaders import VIEWPORTRECT_VERT_SHADER, VIEWPORTRECT_FRAG_SHADER

from insarviz.linalg import matrix

# MiniMapView ##################################################################


class MinimapView(AbstractMapView):
    """
    Minimap
    This is a general view of the data. A white rectangle
    shows the area cureently displayed in Map (zoom/pan synchronized).
    """

    CLICK = 1

    pan_map_view = pyqtSignal(float, float)
    zoom_map_view = pyqtSignal(float, float, float)
    set_center_map_view = pyqtSignal(float, float)
    # TODO self.p0 does not match AbstractMapView.p0

    def __init__(self, map_model: MapModel, parent: QWidget):
        super().__init__(map_model, parent)
        # model matrix of the rectangle figuring MapView's viewport (in data coordinate system)
        self.mapview_viewport_matrix = matrix.identity()
        self.program: QOpenGLShaderProgram
        self.setCursor(Qt.OpenHandCursor)

    def initializeGL(self) -> None:
        super().initializeGL()
        version = QOpenGLVersionProfile(self.context().format())
        version.setVersion(4, 1)
        glfunc = self.context().versionFunctions(version)
        glfunc.glDisable(GL_BLEND)
        # shaders for the rectangle figuring MapView's viewport
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, VIEWPORTRECT_VERT_SHADER)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, VIEWPORTRECT_FRAG_SHADER)
        self.program.link()
        self.program.bind()
        self.program.setUniformValue('rect_color', 1., 1., 1., 1.)
        self.program.release()

    def sizeHint(self) -> QSize:
        return QSize(100, 100)

    def paintGL(self) -> None:
        """
        Generate and display OpenGL texture for Map.
        """
        version = QOpenGLVersionProfile(self.context().format())
        version.setVersion(4, 1)
        glfunc = self.context().versionFunctions(version)
        glfunc.glClear(GL_COLOR_BUFFER_BIT)
        ####
        for layer in self.map_model.layer_model.layers:
            if isinstance(layer, MainLayer):
                layer.show(self.view_matrix, self.projection_matrix, vao=self.vao, glfunc=glfunc,
                           blend=False)
        # white rectangle figuring MapView's viewport
        self.vao.bind()
        self.program.bind()
        self.program.setUniformValue('model_matrix', QMatrix4x4(
            matrix.flatten(self.mapview_viewport_matrix)))
        self.program.setUniformValue('view_matrix', QMatrix4x4(matrix.flatten(self.view_matrix)))
        self.program.setUniformValue('projection_matrix', QMatrix4x4(
            matrix.flatten(self.projection_matrix)))
        glfunc.glDrawArrays(GL_LINE_LOOP, 0, 4)
        self.program.release()
        self.vao.release()

    # TODO DISABLING THIS FOR NOW, NEEDS RETHINKING
        # overlay orbit+LOS symbol using QPainter
        # if info available from metadata file
        # try:
        #     assert(self.map_model.loader.metadata['Antenna_side'] in (
        #         'LEFT', 'RIGHT'))
        #     painter = QPainter(self)
        #     painter.setRenderHint(QPainter.Antialiasing)  # does not work...

        #     # symbol is made of two perpendicular arrows, orbit arrow and LOS
        #     # arrow (which starts at orbit arrow's mid-point)
        #     # drawn twice, in black and in white to improve readability
        #     for dx, dy, color in [
        #             (1, 1, QColor('black')),
        #             (0, 0, QColor('white'))]:

        #         painter.setPen(QPen(color, 2))
        #         painter.setBrush(color)
        #         painter.pen().setWidth(10)

        #         center_pt = QPoint(self.width()-25+dx, self.height()-25+dy)

        #         # drawing points
        #         (orb_start,
        #          orb_end,
        #          los_end) = self.make_orbit_LOS_symbol(center_pt)
        #         los_start = center_pt

        #         # orbit arrow:
        #         painter.drawLine(orb_start, orb_end)
        #         rotation = math.degrees(
        #             math.atan2(orb_start.y()-orb_end.y(),
        #                        orb_end.x()-orb_start.x())) + 90
        #         arrowhead_poly = [
        #             QPoint(orb_end.x()+5*math.sin(math.radians(rotation)),
        #                    orb_end.y()+5*math.cos(math.radians(rotation))),
        #             QPoint(orb_end.x()+5*math.sin(math.radians(rotation-120)),
        #                    orb_end.y()+5*math.cos(math.radians(rotation-120))),
        #             QPoint(orb_end.x()+5*math.sin(math.radians(rotation+120)),
        #                    orb_end.y()+5*math.cos(math.radians(rotation+120)))]
        #         painter.drawPolygon(QPolygon(arrowhead_poly))

        #         # LOS arrow:
        #         painter.drawLine(los_start, los_end)
        #         rotation = math.degrees(
        #             math.atan2(los_start.y()-los_end.y(),
        #                        los_end.x()-los_start.x())) + 90
        #         arrowhead_poly = [
        #             QPoint(los_end.x()+4*math.sin(math.radians(rotation)),
        #                    los_end.y()+4*math.cos(math.radians(rotation))),
        #             QPoint(los_end.x()+4*math.sin(math.radians(rotation-120)),
        #                    los_end.y()+4*math.cos(math.radians(rotation-120))),
        #             QPoint(los_end.x()+4*math.sin(math.radians(rotation+120)),
        #                    los_end.y()+4*math.cos(math.radians(rotation+120)))]
        #         painter.drawPolygon(QPolygon(arrowhead_poly))

        # except (AssertionError, AttributeError, KeyError):
        #     # no metadata or wrong format
        #     pass

    # interaction

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """
        Overload method
        Set interaction according to user mouse input:
            - Left-click: pan
            - Right-click: zoom

        Parameters
        ----------
        e : QMouseEvent
        """
        # check if data loaded
        if self.map_model.i is not None:
            if self.interaction == self.INTERACTIVE:
                self.p0 = *self.get_texture_coordinate(e.x(), e.y()), e.x(), e.y()
                self.p_prev = self.p0
                if e.button() == Qt.LeftButton:
                    self.interaction = self.CLICK
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """
        Overload method
        Interaction mode according to user input:
            - Left-click+drag (pan): change position
            - Right-click+drag (zoom): change zoom level

        Parameters
        ----------
        e : QMouseEvent
        """
        if self.interaction == self.CLICK or self.left_drag or self.right_drag:
            x_data0, y_data0, x_widget0, y_widget0 = self.p0
            x_data1, y_data1, x_widget1, y_widget1 = * \
                self.get_texture_coordinate(e.x(), e.y()), e.x(), e.y()
            dx, dy = x_data1-x_data0, y_data1-y_data0
            if self.interaction == self.CLICK:
                # if the cursor has moved away from the press position buffer zone
                if abs(x_widget1 - x_widget0) + abs(y_widget1 - y_widget0) > 4:
                    self.interaction = self.INTERACTIVE
                    self.setCursor(Qt.ClosedHandCursor)
            elif self.left_drag:
                self.pan_map_view.emit(dx, dy)
                self.p0 = x_data1, y_data1, x_widget1, y_widget1
            elif self.right_drag:
                # make the difference in view coordinates between the cursor previous
                # and current positions and zoom accordingly
                _, _, x_prev, y_prev = self.p_prev
                self.zoom_map_view.emit((x_widget1 - x_prev) -
                                        (y_widget1 - y_prev), x_data0, y_data0)
                # update previous positions
                self.p_prev = x_data1, y_data1, x_widget1, y_widget1

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """
        Overload method
        End interaction mode.

        Parameters
        ----------
        e : QMouseEvent
        """
        if self.interaction == self.CLICK and e.button() == Qt.LeftButton:
            x0, y0, _, _ = self.p0
            self.set_center_map_view.emit(x0, y0)
            self.interaction = self.INTERACTIVE
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(e)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Overload method
        Update zoom value in Map model according to wheel angle change for
        zoom level update on Map

        Parameters
        ----------
        event : QWheelEvent

        Returns
        -------
        None.
        """
        x, y = self.get_texture_coordinate(event.x(), event.y())
        ds = event.angleDelta().y()/8  # degrees
        self.zoom_map_view.emit(ds, x, y)

    # connected to MapView's viewport_matrix_changed
    @pyqtSlot(object)
    def update_mapview_viewport_matrix(self, m: matrix.Matrix) -> None:
        self.mapview_viewport_matrix = m
        self.update()

    def update_view_matrix(self) -> None:
        if self.map_model.tex_width and self.map_model.tex_height:
            # texture size
            tex_w, tex_h = self.map_model.tex_width, self.map_model.tex_height
            self.cx, self.cy = tex_w//2, tex_h//2
            # view size
            view_w, view_h = self.width(), self.height()
            # size ratios
            view_ratio, tex_ratio = view_w / view_h, tex_w / tex_h
            if view_ratio > tex_ratio:
                # view is wider than texture
                # zoom is thus the height ratio between view and texture
                self.z = view_h / tex_h
            else:
                # view is higher than texture
                # zoom is thus the width ratio between view and texture
                self.z = view_w / tex_w
        super().update_view_matrix()

    def make_orbit_LOS_symbol(self, center_pt):
        """
        determine the coordinates or the points for the symbol representing
        the satellite's orbit direction and LOS in the Minimap

        Symbol for ASCENDING RIGHT:

        Orbit direction
        ^
        |
        |
        |-> LOS
        |
        |

        Parameters
        ----------
        center_pt : QPoint
            center point for the symbol (near bottom-right corner of Minimap)

        Returns
        -------
        orb_start : QPoint
            starting point of the orbit arrow.
        orb_end : QPoint
            end point of the orbit arrow.
        los_end : QPoint
            end point of the LOS arrow.

        """

        AR = AL = DR = DL = False

        orbit, side, flipped = (self.map_model.loader.metadata['Orbit_direction'],
                                self.map_model.loader.metadata['Antenna_side'],
                                self.map_model.isflipped_ud)

        AR = ((orbit == 'ASCENDING' and
               side == 'RIGHT' and
               not flipped) or (
            orbit == 'DESCENDING' and
            side == 'LEFT' and
            flipped))
        AL = ((orbit == 'ASCENDING' and
               side == 'LEFT' and
               not flipped) or (
            orbit == 'DESCENDING' and
            side == 'RIGHT' and
            flipped))
        DR = ((orbit == 'DESCENDING' and
               side == 'RIGHT' and
               not flipped) or (
            orbit == 'ASCENDING' and
            side == 'LEFT' and
            flipped))
        DL = ((orbit == 'DESCENDING' and
               side == 'LEFT' and
               not flipped) or (
            orbit == 'ASCENDING' and
            side == 'RIGHT' and
            flipped))
        if AR:
            orb_start = QPoint(center_pt.x() + 4, center_pt.y() + 15)
            orb_end = QPoint(center_pt.x() - 4, center_pt.y() - 15)
            los_end = QPoint(center_pt.x() + 3, center_pt.y() - 1)
        elif AL:
            orb_start = QPoint(center_pt.x() + 4, center_pt.y() + 15)
            orb_end = QPoint(center_pt.x() - 4, center_pt.y() - 15)
            los_end = QPoint(center_pt.x() - 3, center_pt.y() + 1)
        elif DR:
            orb_start = QPoint(center_pt.x() + 4, center_pt.y() - 15)
            orb_end = QPoint(center_pt.x() - 4, center_pt.y() + 15)
            los_end = QPoint(center_pt.x() - 3, center_pt.y() - 1)
        elif DL:
            orb_start = QPoint(center_pt.x() + 4, center_pt.y() - 15)
            orb_end = QPoint(center_pt.x() - 4, center_pt.y() + 15)
            los_end = QPoint(center_pt.x() + 3, center_pt.y() + 1)

        else:
            print('unrecognized orbit/LOS parameters')

        return (orb_start, orb_end, los_end)
