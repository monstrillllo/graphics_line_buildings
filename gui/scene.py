from PyQt5 import QtWidgets
from PyQt5.QtCore import QRectF
from pixel_item import Pixel_item


class My_scene(QtWidgets.QGraphicsScene):
    def __init__(self, parent, rect: QRectF):
        super().__init__(QRectF(rect), parent=parent)
        self.rclick = False

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.rclick = True

    def mouseMoveEvent(self, event):
        if self.rclick:
            item = Pixel_item()
            item.setPos(event.scenePos())
            self.addItem(item)

    def mouseReleaseEvent(self, event):
        self.rclick = False
