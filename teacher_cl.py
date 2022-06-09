import sys
from PyQt5 import QtGui, QtWidgets, uic
from socket import *
from PyQt5.QtWidgets import QMessageBox
from threading import Thread


class Mainwindow(QtWidgets.QMainWindow):
    client_socket = None

    def __init__(self):
        super(Mainwindow, self).__init__()
        uic.loadUi('client.ui', self)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        address = ('localhost', 50004)
        self.client_socket.connect(address)
        self.recevie_thread()

        self.pushButton_2.clicked.connect(self.ServerConnect)

    def chat(self):
        self.stackedWidget.setCurrentIndex(1)

    # 메세지 받을때 쓰는 스레드
    def recevie_thread(self):
        recevie_thread = Thread(target=self.Server_recive)
        recevie_thread.start()

    # 서버에서 오는 메세지
    def Server_recive(self):
        while True:
            re_message = self.client_socket.recv(1024)
            de_mge = re_message.decode()
            print(1, de_mge)

            if not re_message:
                break
            if de_mge == '채팅요청':
                msg = QMessageBox.question(self, 'Message', '채팅요청이 들어왔습니다.', QMessageBox.Yes | QMessageBox.No)
                # QMessageBox.question(self, 'Message', '채팅요청이 들어왔습니다.', QMessageBox.Yes | QMessageBox.No)

                if msg == QMessageBox.Yes:
                    msg_box = QMessageBox.question(self, 'Message', '채팅을 수락했습니다. 채팅창으로 이동합니다. ', QMessageBox.Yes)
                    self.client_socket.send("chat/채팅수락".encode())
                    if msg_box == QMessageBox.Yes:
                        self.chat()

                if msg == QMessageBox.No:
                    QMessageBox.question(self, 'Message', '채팅을 거부하셨습니다.', QMessageBox.Yes)
                    self.client_socket.send("chat/채팅거부".encode())

            else:
                self.textBrowser.append(de_mge)

    # 채팅창
    def ServerConnect(self):
        self.teacher_msg = self.chat_input.text()
        self.client_socket.send(self.teacher_msg.encode())
        print('send', self.teacher_msg)
        self.textBrowser.append(self.teacher_msg)
        self.chat_input.clear()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    main.setWindowTitle('채팅창')
    sys.exit(app.exec_())
