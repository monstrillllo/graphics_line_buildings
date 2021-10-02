from PyQt5 import QtWidgets
from PyQt5.QtCore import QRectF
from pixel_item import PixelItem


class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent, rect: QRectF):
        super().__init__(QRectF(rect), parent=parent)
        # self.rclick = False
        self.pos1 = None
        self.pos2 = None
        self.type = None

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.pos1 = event.scenePos()

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.pos2 = event.scenePos()
            item = PixelItem(self.pos1, self.pos2, self.type)
            self.addItem(item)
            item.setPos(self.pos1)

    def set_line_type(self, type):
        self.type = type
