# Developed by Sapeginskiy Evgeniy BSUIR group 821703
import math
import random
import typing
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget


class PixelItem(QtWidgets.QGraphicsItem):
    def __init__(self, pos1: QPoint, pos2: QPoint, type_, debug, parent_scene):
        super().__init__()
        self.pos1 = pos1
        self.pos2 = pos2
        self.debug = debug
        self.parent_scene = parent_scene
        self.debug_counter = self.parent_scene.debug_counter
        self.type = type_
        self.enableDebugPrint = True

    def boundingRect(self) -> QtCore.QRectF:
        if self.type == 'Bresenham_circle':
            a = (self.pos1.x() - self.pos2.x()) ** 2
            b = (self.pos1.y() - self.pos2.y()) ** 2
            radius = math.sqrt(a + b)
            return QtCore.QRectF(-radius, -radius, 2 * radius, 2 * radius)
        elif self.type in ['dda', 'Bresenham', 'anti-aliasing']:
            deltaY = self.pos2.y() - self.pos1.y()
            deltaX = self.pos2.x() - self.pos1.x()
            aleft = 0 if deltaX > 0 else deltaX
            atop = 0 if deltaY > 0 else deltaY
            return QtCore.QRectF(aleft, atop, abs(deltaX), abs(deltaY))
        else:
            point = self.pos2 - self.pos1
            return QtCore.QRectF(-abs(point.x()), -abs(point.y()), 2 * abs(point.x()), 2 * abs(point.y()))

    def paint(self, painter: QtGui.QPainter, option, widget: typing.Optional[QWidget] = ...) -> None:
        if self.type == 'dda':
            self.dda_line(painter)
        elif self.type == 'Bresenham':
            self.bresenham_line(painter)
        elif self.type == 'anti-aliasing':
            self.anti_aliasing(painter)
        elif self.type == 'Bresenham_circle':
            self.bresenham_circle(painter)
        elif self.type == 'Ellipse':
            self.ellipse(painter)
        elif self.type == 'Hyperbola':
            self.hyperbola(painter)

    def dda_line(self, painter):
        Diff = self.pos2 - self.pos1
        len_ = max(abs(Diff.x()), abs(Diff.y()))
        dx = Diff.x() / len_
        dy = Diff.y() / len_
        x = 0
        y = 0
        for i in range(int(len_) + 1):
            x = x + dx
            y = y + dy
            point = QPoint(int(x), int(y))
            painter.drawPoint(point)
            if self.debug:
                if self.debug_counter == len_ or not self.debug:
                    self.scene().debug = False
                    self.debug = False
                    self.parent_scene.debug_counter = 0
                if i == self.debug_counter:
                    if self.enableDebugPrint:
                        self.enableDebugPrint = False
                        self.parent_scene.textPanel.insertPlainText(f'x: {round(x, 2)} y: {round(y, 2)}\n')
                    break

    def bresenham_line(self, painter):
        diff = self.pos2 - self.pos1
        delta_primary = diff.x() if abs(diff.x()) >= abs(diff.y()) else diff.y()
        delta_secondary = diff.x() if abs(diff.y()) > abs(diff.x()) else diff.y()
        e = delta_secondary / delta_primary - 1 / 2

        primary = 0
        secondary = 0
        primary_grow = 1 if delta_primary > 0 else -1
        secondary_grow = 1 if delta_secondary > 0 else -1

        for i in range(0, int(abs(delta_primary)) + 1):

            if e >= 0:
                secondary += secondary_grow
                e -= 1

            primary += primary_grow
            e += abs(delta_secondary / delta_primary)

            new_color = 255 * (abs(e) - abs(int(e)))
            painter.setPen(QColor(new_color, new_color, new_color))
            res = QPoint(int(primary), int(secondary)) if abs(diff.x()) >= abs(diff.y()) \
                else QPoint(int(secondary), int(primary))
            painter.drawPoint(res)
            if self.debug:
                if self.debug_counter == int(abs(delta_primary)) or not self.debug:
                    self.scene().debug = False
                    self.debug = False
                    self.parent_scene.debug_counter = 0
                if i == self.debug_counter:
                    if self.enableDebugPrint:
                        self.enableDebugPrint = False
                        self.parent_scene.textPanel.insertPlainText(f'x: {round(res.x(), 2)} '
                                                                    f'y: {round(res.y(), 2)}\n')
                    break

    def anti_aliasing(self, painter):
        diff = self.pos2 - self.pos1
        delta_primary = diff.x() if abs(diff.x()) >= abs(diff.y()) else diff.y()
        delta_secondary = diff.x() if abs(diff.y()) > abs(diff.x()) else diff.y()
        e = delta_secondary / delta_primary - 1 / 2

        primary = 0
        secondary = 0
        primary_grow = 1 if delta_primary > 0 else -1
        secondary_grow = 1 if delta_secondary > 0 else -1
        increment = -1 if delta_secondary >= 0 else 1

        for i in range(0, int(abs(delta_primary)) + 1):
            if e >= 0:
                secondary += secondary_grow
                e -= 1
            primary += primary_grow
            e += abs(delta_secondary / delta_primary)
            new_color = 255 * (abs(e) - abs(int(e)))
            painter.setPen(QColor(new_color, new_color, new_color))
            res = QPoint(int(primary), int(secondary)) if abs(diff.x()) >= abs(diff.y()) \
                else QPoint(int(secondary), int(primary))
            painter.drawPoint(res)
            if (i != 0) and (i != abs(delta_primary)):
                new_color = 255 * (1 - (abs(e) - abs(int(e))))
                painter.setPen(QColor(new_color, new_color, new_color))
                new_increment = increment * -1 if e >= 0 else increment
                res = QPoint(int(primary), int(secondary) + new_increment) if abs(diff.x()) >= abs(diff.y()) \
                    else QPoint(int(secondary) + new_increment, int(primary))
                painter.drawPoint(res)
            if self.debug:
                if self.debug_counter == int(abs(delta_primary)) or not self.debug:
                    self.scene().debug = False
                    self.debug = False
                    self.parent_scene.debug_counter = 0
                if i == self.debug_counter:
                    if self.enableDebugPrint:
                        self.enableDebugPrint = False
                        self.parent_scene.textPanel.insertPlainText(f'x: {round(res.x(), 2)} '
                                                                    f'y: {round(res.y(), 2)}\n')
                    break

    def bresenham_circle(self, painter: QtGui.QPainter):
        # painter.setPen(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        radius = math.sqrt((self.pos1.x() - self.pos2.x())**2 + (self.pos1.y() - self.pos2.y())**2)
        p = 0
        q = radius
        d = 3 - 2 * radius
        while p <= q:
            self.draw_circle(painter, 0, 0, p, q)
            p += 1
            if d < 0:
                d = d + 4 * p + 6
            else:
                radius -= 1
                q = radius
                d = d + 4 * (p - q) + 10
        self.draw_circle(painter, 0, 0, p, q)

    def draw_circle(self, painter: QtGui.QPainter, x, y, p, q):
        painter.drawPoint(x + p, y + q)
        painter.drawPoint(x - p, y + q)
        painter.drawPoint(x + p, y - q)
        painter.drawPoint(x - p, y - q)
        painter.drawPoint(x + q, y + p)
        painter.drawPoint(x - q, y + p)
        painter.drawPoint(x + q, y - p)
        painter.drawPoint(x - q, y - p)

    def ellipse(self, painter: QtGui.QPainter):
        rx = abs(self.pos1.x() - self.pos2.x())
        ry = abs(self.pos1.y() - self.pos2.y())
        x = 0
        y = ry
        d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
        dx = 2 * ry * ry * x
        dy = 2 * rx * rx * y

        while dx < dy:
            painter.drawPoint(x, y)
            painter.drawPoint(-x, y)
            painter.drawPoint(x, -y)
            painter.drawPoint(-x, -y)
            if d1 < 0:
                x += 1
                dx = dx + (2 * ry * ry)
                d1 = d1 + dx + (ry * ry)
            else:
                x += 1
                y -= 1
                dx = dx + (2 * ry * ry)
                dy = dy - (2 * rx * rx)
                d1 = d1 + dx - dy + (ry * ry)

        d2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry)
        while y >= 0:
            painter.drawPoint(x, y)
            painter.drawPoint(-x, y)
            painter.drawPoint(x, -y)
            painter.drawPoint(-x, -y)
            if d2 > 0:
                y -= 1
                dy = dy - (2 * rx * rx)
                d2 = d2 + (rx * rx) - dy
            else:
                y -= 1
                x += 1
                dx = dx + (2 * ry * ry)
                dy = dy - (2 * rx * rx)
                d2 = d2 + dx - dy + (rx * rx)

    def hyperbola(self, painter: QtGui.QPainter):
        a = abs(self.pos1.x() - self.pos2.x())
        b = abs(self.pos1.y() - self.pos2.y())
        x = a
        y = 0
        d = 2 * a * a - 2 * a * b * b - b * b
        while y <= b * b * x / (a * a):
            painter.drawPoint(x, y)
            painter.drawPoint(-x, y)
            painter.drawPoint(x, -y)
            painter.drawPoint(-x, -y)
            if d < 0:
                d += 2 * a * a * (2 * y + 3)
            else:
                d += 2 * a * a * (2 * y + 3) - 4 * b * b * (x + 1)
                x += 1
            y += 1

        init = 100
        while init - 1:
            if d < 0:
                d += 2 * b * b * (3 + 2 * x)
            else:
                d += 2 * b * b * (3 + 2 * x) - 4 * a * a * (y + 1)
                y += 1
            x += 1
            painter.drawPoint(x, y)
            painter.drawPoint(-x, y)
            painter.drawPoint(x, -y)
            painter.drawPoint(-x, -y)

