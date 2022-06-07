import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("main.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 버튼에 기능을 연결하는 코드
        self.sellogin_s.clicked.connect(self.sellogin_s_click)
        self.sellogin_t.clicked.connect(self.sellogin_t_click)
        self.stackedWidget.setCurrentIndex(0)

    # btn_1이 눌리면 작동할 함수
    def sellogin_s_click(self):
        self.stackedWidget.setCurrentIndex(2)

    # btn_2가 눌리면 작동할 함수
    def sellogin_t_click(self):
        self.stackedWidget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
