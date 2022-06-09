import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("main.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.gotosignin.clicked.connect(self.gotosignin_click)
        self.gotosignup.clicked.connect(self.gotosignup_click)
        self.stackedWidget.setCurrentIndex(0)

    def gotosignin_click(self):
        self.stackedWidget.setCurrentIndex(1)

    def gotosignup_click(self):
        self.stackedWidget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
