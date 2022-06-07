import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("main.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.sellogin_s.clicked.connect(self.sellogin_s_click)
        self.sellogin_t.clicked.connect(self.sellogin_t_click)
        self.stackedWidget.setCurrentIndex(0)

    def sellogin_s_click(self):
        self.stackedWidget.setCurrentIndex(2)

    def sellogin_t_click(self):
        self.stackedWidget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
