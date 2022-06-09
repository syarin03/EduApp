import sys
from PyQt5 import QtWidgets, uic
from socket import *
from PyQt5.QtWidgets import QMessageBox
from threading import Thread

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic


class Mainwindow(QtWidgets.QMainWindow,QThread):
    client_socket = None

    def __init__(self):
        super(Mainwindow, self).__init__()
        uic.loadUi('client.ui', self)
        self.label_8.setText('학생')
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        address = ('localhost', 50004)
        self.client_socket.connect(address)
        self.recevie_thread()

        # 서버에 메세지 보내기
        self.pushButton.clicked.connect(self.Chat_ServerConnect)
        self.pushButton_2.clicked.connect(self.ServerConnect)
        self.pushButton_3.clicked.connect(self.join)
        self.pushButton_4.clicked.connect(self.login)
        self.pushButton_5.clicked.connect(self.Question)
        self.pushButton_6.clicked.connect(self.answer)

        self.dic_list=[]

    def chat(self):
        self.stackedWidget.setCurrentIndex(1)

    #메세지 받을때 쓰는 스레드
    def recevie_thread(self):
        recevie_thread = Thread(target= self.Server_recive)
        recevie_thread.start()

    #서버에서 오는 메세지
    def Server_recive(self):
        while True:
            re_message = self.client_socket.recv(1024)
            de_mge = re_message.decode()
            print(1, de_mge)

            if not re_message:
                break

            if de_mge == '채팅거부':
                QMessageBox.question(self, 'Message', '채팅이 거부됐습니다.', QMessageBox.Yes)

            elif de_mge == '채팅수락':
                QMessageBox.question(self, 'Message', '채팅 연결완료.', QMessageBox.Yes)
                self.chat()

            else:
                self.textBrowser.append(de_mge)



    # 서버에 채팅요청 메세지 보내기
    def Chat_ServerConnect(self):
        QMessageBox.question(self, 'Message', '채팅 연결중.. 잠시만 기다려주십시오.', QMessageBox.Yes)
        self.client_socket.send('chat/채팅요청'.encode())
        # self.Server_recive()
        # recevie_thread = Thread(target=self.Server_recive)
        # recevie_thread.start()

        # while True:
        #     re_message = self.client_socket.recv(4096)
        #     de_mge = re_message.decode()
        #     print(1, de_mge)
        #
        #     if not re_message:
        #         break
        #
        #     if de_mge == '//채팅거부':
        #         QMessageBox.question(self, 'Message', '채팅이 거부됐습니다.', QMessageBox.Yes)
        #
        #     elif de_mge == '//채팅수락':
        #         QMessageBox.question(self, 'Message', '채팅 연결완료.', QMessageBox.Yes)
        #         self.chat()
        #
        #     else:
        #         self.textBrowser.append(de_mge)

            # a = eval(de_mge)
            # print(type(a))
            # self.dic_list.append(a[0][3])
            # self.label_9.setText(a[0][3])


    # 상담 내용
    def ServerConnect(self):
        self.student_msg = self.chat_input.text()
        self.client_socket.send(self.student_msg.encode())
        print('send', self.student_msg)
        self.textBrowser.append(self.student_msg)
        self.chat_input.clear()

    def Question(self):

        self.client_socket.send('문제풀기'.encode())
        self.stackedWidget.setCurrentIndex(2)

        re_message = self.client_socket.recv(4096)
        de_mge = re_message.decode()
        print('문제',de_mge)

        a=eval(de_mge)
        print(type(a),a)
        for i in a:
            self.dic_list.append(i)
        self.textBrowser_2.append(self.dic_list[0])
        # self.label_9.setText(self.dic_list[0])

    def answer(self):
        a='정답/'+self.lineEdit_7.text()
        self.client_socket.send(a.encode())

        re_message = self.client_socket.recv(1024)
        de_mge = re_message.decode()
        print(123)

        if de_mge == '정답임':
            msg = QMessageBox()
            msg.setWindowTitle("안내문")
            msg.setText("정답.")
            msg.move(400, 400)
            msg.exec_()

        elif de_mge == '실패임':
            msg = QMessageBox()
            msg.setWindowTitle("안내문")
            msg.setText("오답.")
            msg.move(400, 400)
            msg.exec_()




    def join(self):
        join_info = ['학생', self.lineEdit.text() ,self.lineEdit_2.text(),self.lineEdit_3.text(), self.lineEdit_4.text()]
        sql = 'join/'+str(join_info)
        self.client_socket.send(sql.encode())
        print('send', sql)

        re_message = self.client_socket.recv(1024)
        de_mge = re_message.decode()
        if de_mge == '아이디중복':
            msg = QMessageBox()
            msg.setWindowTitle("안내문")
            msg.setText("중복된 아이디 입니다.")
            msg.move(400, 400)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("안내문")
            msg.setText("회원가입 완료.")
            msg.move(400, 400)
            msg.exec_()

    def login(self):
        login_info=['학생', self.lineEdit_5.text() ,self.lineEdit_6.text()]
        sql = 'login/'+str(login_info)
        self.client_socket.send(sql.encode())
        print('send', sql)

        re_message = self.client_socket.recv(1024)
        de_mge = re_message.decode()

        if de_mge == '성공':
            msg = QMessageBox()
            msg.setWindowTitle("안내문")
            msg.setText("로그인성공.")
            msg.move(400, 400)
            msg.exec_()

        elif de_mge == '실패':
            msg = QMessageBox()
            msg.setWindowTitle("안내문")
            msg.setText("아이디와 비밀번호가 일치하지않습니다. 다시 입력해주세요.")
            msg.move(400, 400)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("안내문")
            msg.setText("존재하지않은 아이디 입니다. 다시 입력해주세요.")
            msg.move(400, 400)
            msg.exec_()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    main.setWindowTitle('채팅창')
    sys.exit(app.exec_())
