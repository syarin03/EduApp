import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("main.ui")[0]
job = ""


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.gotosignin.clicked.connect(self.gotosignin_click)
        self.gotosignup.clicked.connect(self.gotosignup_click)
        self.stackedWidget.setCurrentIndex(0)

    def gotosignin_click(self):
        self.stackedWidget.setCurrentIndex(1)
        if self.inchoose_s.isChecked(): job = "stu"
        elif self.inchoose_t.isChecked(): job = "tea"
        self.signinbtn.clicked.connect(self.login_click)

    def gotosignup_click(self):
        self.stackedWidget.setCurrentIndex(2)

    def login_click(self):
        if job == "stu":
            print(job)
            self.stackedWidget.setCurrentIndex(3)
        elif job == "tea":
            print(job)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
