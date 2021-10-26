# Developed by Sapeginskiy Evgeniy BSUIR group 821703
from PyQt5 import QtWidgets, QtCore
from scene import MyScene

import graphic_editor_ui


class GraphicEditor(QtWidgets.QMainWindow, graphic_editor_ui.Ui_GraphicEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_line_type1.clicked.connect(self.btn_line_type1_clicked)
        self.btn_line_type1.setDisabled(True)
        self.btn_line_type2.clicked.connect(self.btn_line_type2_clicked)
        self.btn_line_type3.clicked.connect(self.btn_line_type3_clicked)
        self.btn_circle1.clicked.connect(self.btn_circle1_clicked)
        self.btn_ellipse.clicked.connect(self.btn_ellipse_clicked)
        self.btn_debug_start.clicked.connect(self.btn_debug_clicked)
        self.btn_debug_next.clicked.connect(self.btn_debug_next_clicked)
        self.scene = MyScene(self.main_graphicsView, self.main_graphicsView.rect(), self.debug_text_bar)
        self.main_graphicsView.setScene(self.scene)
        self.scene.set_line_type('dda')

    def btn_line_type1_clicked(self):
        self.scene.set_line_type('dda')
        self.btn_line_type1.setDisabled(True)
        self.btn_line_type2.setEnabled(True)
        self.btn_line_type3.setEnabled(True)
        self.btn_circle1.setEnabled(True)
        self.btn_ellipse.setEnabled(True)

    def btn_line_type2_clicked(self):
        self.scene.set_line_type('Bresenham')
        self.btn_line_type2.setDisabled(True)
        self.btn_line_type1.setEnabled(True)
        self.btn_line_type3.setEnabled(True)
        self.btn_circle1.setEnabled(True)
        self.btn_ellipse.setEnabled(True)

    def btn_line_type3_clicked(self):
        self.scene.set_line_type('anti-aliasing')
        self.btn_line_type3.setDisabled(True)
        self.btn_line_type2.setEnabled(True)
        self.btn_line_type1.setEnabled(True)
        self.btn_circle1.setEnabled(True)
        self.btn_ellipse.setEnabled(True)

    def btn_circle1_clicked(self):
        self.scene.set_line_type('Bresenham_circle')
        self.btn_line_type3.setEnabled(True)
        self.btn_circle1.setDisabled(True)
        self.btn_line_type1.setEnabled(True)
        self.btn_line_type3.setEnabled(True)
        self.btn_ellipse.setEnabled(True)

    def btn_ellipse_clicked(self):
        self.scene.set_line_type('Ellipse')
        self.btn_line_type3.setEnabled(True)
        self.btn_circle1.setEnabled(True)
        self.btn_line_type1.setEnabled(True)
        self.btn_line_type3.setEnabled(True)
        self.btn_ellipse.setDisabled(True)

    def btn_debug_clicked(self):
        if self.scene.debug:
            self.debug_text_bar.insertPlainText('Debug off\n')
            self.scene.set_debug(False)
        else:
            self.debug_text_bar.insertPlainText('Debug on\n')
            self.scene.set_debug(True)

    def btn_debug_next_clicked(self):
        if self.scene.debug:
            self.scene.debug_counter += 1
            self.scene.draw_line()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = GraphicEditor()
    window.show()
    app.exec()
