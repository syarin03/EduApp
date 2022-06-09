import sys
from builtins import super

from PyQt5 import QtGui, QtWidgets, uic
from socket import *
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore


class Mainwindow(QtWidgets.QMainWindow):
    client_socket = None

    def __init__(self):
        super(Mainwindow, self).__init__()
        uic.loadUi('client.ui', self)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        address = ('localhost', 50004)
        self.client_socket.connect(address)
        # self.recevie_thread()
        self.pushButton_2.clicked.connect(self.ServerConnect)

        self.Thread = Server_message()  #쓰레드 객체 생성
        self.Thread.start()
        self.Thread.chat_request.connect(self.chat_request)
        self.Thread.consulting.connect(self.consulting)


    def chat(self):
        self.stackedWidget.setCurrentIndex(1)

    # 채팅요청
    @pyqtSlot(str)
    def chat_request(self, de_mge):
        if '채팅요청' in de_mge:
            msg = QMessageBox.question(self, 'Message', '채팅요청이 들어왔습니다.', QMessageBox.Yes | QMessageBox.No)

            if msg == QMessageBox.Yes:
                msg_box = QMessageBox.question(self, 'Message', '채팅을 수락했습니다. 채팅창으로 이동합니다. ', QMessageBox.Yes)
                self.client_socket.send("chat/채팅수락".encode())

                if msg_box == QMessageBox.Yes:
                    self.chat()

            if msg == QMessageBox.No:
                QMessageBox.question(self, 'Message', '채팅을 거부하셨습니다.', QMessageBox.Yes)
                self.client_socket.send("chat/채팅거부".encode())

    # 메세지 보여주기
    @pyqtSlot(str)
    def consulting(self, de_mge):
        self.textBrowser.append(de_mge)


    # 채팅창 보내기
    def ServerConnect(self):
        self.teacher_msg = self.chat_input.text()
        self.client_socket.send(self.teacher_msg.encode())
        print('send', self.teacher_msg)
        self.textBrowser.append(self.teacher_msg)
        self.chat_input.clear()

# 서버에서 온 메세지
class Server_message(QThread):
    chat_request = QtCore.pyqtSignal(str)
    consulting = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Server_message, self).__init__()

    def run(self):
        while True:
            self.client_socket = main.client_socket
            re_message = self.client_socket.recv(1024)
            de_mge = re_message.decode()
            print(1, de_mge)
            if not re_message:
                break
            if '채팅요청' in de_mge :
                self.chat_request.emit(de_mge)
                print(12)

            else:
                self.consulting.emit(de_mge)
                print(1234567,de_mge)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    main.setWindowTitle('채팅창')
    sys.exit(app.exec_())
