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
        deltaY = self.pos2.y() - self.pos1.y()
        deltaX = self.pos2.x() - self.pos1.x()
        aleft = 0 if deltaX > 0 else deltaX
        atop = 0 if deltaY > 0 else deltaY
        return QtCore.QRectF(aleft, atop, abs(deltaX), abs(deltaY))

    def paint(self, painter: QtGui.QPainter, option, widget: typing.Optional[QWidget] = ...) -> None:
        if self.type == 'dda':
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
        elif self.type == 'Bresenham':
            diff = self.pos2 - self.pos1
            delta_primary = diff.x() if abs(diff.x()) >= abs(diff.y()) else diff.y()
            delta_secondary = diff.x() if abs(diff.y()) > abs(diff.x()) else diff.y()
            e = delta_secondary / delta_primary - 1/2

            primary = 0
            secondary = 0
            primary_grow = 1 if delta_primary > 0 else -1
            secondary_grow = 1 if delta_secondary > 0 else -1

            for i in range(0, int(abs(delta_primary)) + 1):

                if e >= 0:
                    secondary += secondary_grow
                    e -= 1

                primary += primary_grow
                e += abs(delta_secondary/delta_primary)

                new_color = 255 * (abs(e) - abs(int(e)))
                painter.setPen(QColor(new_color, new_color, new_color))
                res = QPoint(int(primary), int(secondary)) if abs(diff.x()) >= abs(diff.y())\
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

        elif self.type == 'anti-aliasing':
            diff = self.pos2 - self.pos1
            delta_primary = diff.x() if abs(diff.x()) >= abs(diff.y()) else diff.y()
            delta_secondary = diff.x() if abs(diff.y()) > abs(diff.x()) else diff.y()
            e = delta_secondary / delta_primary - 1/2

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
                e += abs(delta_secondary/delta_primary)

                new_color = 255 * (abs(e) - abs(int(e)))
                painter.setPen(QColor(new_color, new_color, new_color))
                res = QPoint(int(primary), int(secondary)) if abs(diff.x()) >= abs(diff.y())\
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
