import typing
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from random import randint


class PixelItem(QtWidgets.QGraphicsItem):
    def __init__(self, pos1: QPoint, pos2: QPoint, type_):
        super().__init__()
        self.pos1 = pos1
        self.pos2 = pos2
        if type_:
            self.type = type_
        else:
            self.type = 'dda'

    def boundingRect(self) -> QtCore.QRectF:
        deltaY = self.pos2.y() - self.pos1.y()
        deltaX = self.pos2.x() - self.pos1.x()
        aleft = 0 if deltaX > 0 else deltaX
        atop = 0 if deltaY > 0 else deltaY
        return QtCore.QRectF(aleft, atop, abs(deltaX), abs(deltaY))

    def paint(self, painter: QtGui.QPainter, option, widget: typing.Optional[QWidget] = ...) -> None:
        if self.type == 'dda':
            Diff = self.pos2 - self.pos1
            len = max(abs(Diff.x()), abs(Diff.y()))
            dx = Diff.x() / len
            dy = Diff.y() / len
            x = 0
            y = 0
            for i in range(int(len)):
                x = x + dx
                y = y + dy
                point = QPoint(int(x), int(y))
                painter.drawPoint(point)
        elif self.type == 'Bresenham':
            x = 0
            y = 0
            # diff = self.pos2 - self.pos1
            len_x = abs(self.pos2.x() - self.pos1.x())
            len_y = abs(self.pos2.y() - self.pos1.y())

            main_axis = x if max(len_x, len_y) == len_x else y
            main_axis_delta = max(len_x, len_y)
            secondary_axis = x if min(len_x, len_y) == len_x else y
            secondary_axis_delta = min(len_x, len_y)
            if main_axis_delta == len_x:
                main_increase = 1 if self.pos2.x() > self.pos1.x() else -1
                secondary_increase = 1 if self.pos2.y() > self.pos1.y() else -1
            else:
                secondary_increase = 1 if self.pos2.x() > self.pos1.x() else -1
                main_increase = 1 if self.pos2.y() > self.pos1.y() else -1

            e = 2 * secondary_axis_delta - main_axis_delta
            if main_axis_delta == len_x:
                painter.drawPoint(main_axis, secondary_axis)
            else:
                painter.drawPoint(secondary_axis, main_axis)

            for i in range(int(main_axis_delta)):
                if e >= 0:
                    secondary_axis += secondary_increase
                    e -= 2 * main_axis_delta
                main_axis += main_increase
                e += 2 * secondary_axis_delta
                if max(len_x, len_y) == len_x:
                    painter.drawPoint(main_axis, secondary_axis)
                else:
                    painter.drawPoint(secondary_axis, main_axis)

        elif self.type == 'anti-aliasing':
            x = 0
            y = 0
            len_x = abs(self.pos2.x() - self.pos1.x())
            len_y = abs(self.pos2.y() - self.pos1.y())

            main_axis = x if max(len_x, len_y) == len_x else y
            main_axis_delta = max(len_x, len_y)
            secondary_axis = x if min(len_x, len_y) == len_x else y
            secondary_axis_delta = min(len_x, len_y)
            if main_axis_delta == len_x:
                main_increase = 1 if self.pos2.x() > self.pos1.x() else -1
                secondary_increase = 1 if self.pos2.y() > self.pos1.y() else -1
            else:
                secondary_increase = 1 if self.pos2.x() > self.pos1.x() else -1
                main_increase = 1 if self.pos2.y() > self.pos1.y() else -1
            increment = -1 if secondary_axis_delta >= 0 else 1

            e = 2 * secondary_axis_delta - main_axis_delta
            if main_axis_delta == len_x:
                painter.drawPoint(main_axis, secondary_axis)
            else:
                painter.drawPoint(secondary_axis, main_axis)

            for i in range(int(main_axis_delta) + 1):
                if e >= 0:
                    secondary_axis += secondary_increase
                    e -= 2 * main_axis_delta
                main_axis += main_increase
                e += 2 * secondary_axis_delta
                color = 255 * abs(e - int(e))
                painter.setPen(QColor(color, color, color))
                if max(len_x, len_y) == len_x:
                    painter.drawPoint(main_axis, secondary_axis)
                else:
                    painter.drawPoint(secondary_axis, main_axis)
                if i != 0 and i != int(main_axis_delta):
                    color = 255 * (1 - abs(e - int(e)))
                    painter.setPen(QColor(color, color, color))
                    new_increment = increment * -1 if e >= 0 else increment
                    if max(len_x, len_y) == len_x:
                        painter.drawPoint(main_axis, secondary_axis + new_increment)
                    else:
                        painter.drawPoint(secondary_axis + new_increment, main_axis)
