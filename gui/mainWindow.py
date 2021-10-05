from PyQt5 import QtWidgets, QtCore
from scene import MyScene

import graphic_editor_ui


class GraphicEditor(QtWidgets.QMainWindow, graphic_editor_ui.Ui_GraphicEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(640*2, 480*2)
        self.btn_line_type1.clicked.connect(self.btn_line_type1_clicked)
        self.btn_line_type1.setDisabled(True)
        self.btn_line_type2.clicked.connect(self.btn_line_type2_clicked)
        self.btn_line_type3.clicked.connect(self.btn_line_type3_clicked)
        self.btn_debug_start.clicked.connect(self.btn_debug_clicked)
        self.btn_debug_next.clicked.connect(self.btn_debug_next_clicked)
        self.main_graphicsView.setGeometry(QtCore.QRect(
            self.main_graphicsView.x(),
            self.main_graphicsView.y(),
            self.width() - self.main_graphicsView.x() * 2,
            self.height() - (self.btn_line_type1.height() + 6) - 9))
        self.scene = MyScene(self.main_graphicsView, self.main_graphicsView.rect())
        self.main_graphicsView.setScene(self.scene)
        self.scene.set_line_type('dda')

    def btn_line_type1_clicked(self):
        self.scene.set_line_type('dda')
        self.btn_line_type1.setDisabled(True)
        self.btn_line_type2.setEnabled(True)
        self.btn_line_type3.setEnabled(True)

    def btn_line_type2_clicked(self):
        self.scene.set_line_type('Bresenham')
        self.btn_line_type2.setDisabled(True)
        self.btn_line_type1.setEnabled(True)
        self.btn_line_type3.setEnabled(True)

    def btn_line_type3_clicked(self):
        self.scene.set_line_type('anti-aliasing')
        self.btn_line_type3.setDisabled(True)
        self.btn_line_type2.setEnabled(True)
        self.btn_line_type1.setEnabled(True)

    def btn_debug_clicked(self):
        if self.scene.debug:
            print('Set debug False')
            self.scene.set_debug(False)
        else:
            print('set debug True')
            self.scene.set_debug(True)

    def btn_debug_next_clicked(self):
        if self.scene.debug:
            self.scene.debug_counter += 1
            self.scene.draw_line()
        # print(self.scene.debug_counter)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = GraphicEditor()
    window.show()
    app.exec()
