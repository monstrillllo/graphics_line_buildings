import typing

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from random import randint


class Pixel_item(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0, 1, 1)

    def paint(self, painter: QtGui.QPainter, option, widget: typing.Optional[QWidget] = ...) -> None:
        painter.setPen(QColor(randint(0, 255), randint(0, 255), randint(0, 255)))
        painter.drawPoint(0, 0)
