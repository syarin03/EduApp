import sys
from PyQt5 import QtWidgets, uic
from socket import *
from PyQt5.QtWidgets import QMessageBox
from threading import Thread

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore


class Mainwindow(QtWidgets.QMainWindow,QThread):
    client_socket = None
    user_id = None

    def __init__(self):
        super(Mainwindow, self).__init__()
        uic.loadUi('client.ui', self)
        self.label_8.setText('학생')
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        address = ('localhost', 50008)
        self.client_socket.connect(address)
        self.sub_num=0
        self.user_id=[]
        # self.num=0

        # 서버에 메세지 보내기
        self.pushButton.clicked.connect(self.Chat_ServerConnect)
        self.pushButton_2.clicked.connect(self.ServerConnect)
        self.pushButton_3.clicked.connect(self.join)
        self.pushButton_4.clicked.connect(self.login)
        self.pushButton_5.clicked.connect(self.Question)
        self.pushButton_6.clicked.connect(self.answer)

        #쓰레드
        self.Thread = Server_message()
        self.Thread.start()
        self.Thread.chat_request.connect(self.Server_recive)
        self.Thread.server_question.connect(self.Question_recv)
        self.Thread.server_answer.connect(self.answer_recv)
        self.Thread.server_join.connect(self.join_recv)
        self.Thread.server_login.connect(self.login_recv)
        self.Thread.consulting.connect(self.consulting)

        self.dic_list=[]

    def chat(self):
        self.stackedWidget.setCurrentIndex(1)


    @pyqtSlot(str)
    #서버에서 오는 메세지
    def Server_recive(self, de_mge):
            if de_mge.split('/')[1] == '채팅거부':
                QMessageBox.question(self, 'Message', '채팅이 거부됐습니다.', QMessageBox.Yes)

            elif de_mge.split('/')[1] == '채팅수락':
                QMessageBox.question(self, 'Message', '채팅 연결완료.', QMessageBox.Yes)
                self.chat()

    # 메세지 보여주기
    @pyqtSlot(str)
    def consulting(self, de_mge):
        self.textBrowser.append(de_mge)


    # 서버에 채팅요청 메세지 보내기
    def Chat_ServerConnect(self):
        QMessageBox.question(self, 'Message', '채팅 연결중.. 잠시만 기인포머셜(Informercial)다려주십시오.', QMessageBox.Yes)
        self.client_socket.send('chat/채팅요청'.encode())


    # 상담 내용
    def ServerConnect(self):
        self.student_msg = 'chat/'+self.chat_input.text()
        self.client_socket.send(self.student_msg.encode())
        print('send', self.student_msg)
        self.textBrowser.append(self.chat_input.text())
        self.chat_input.clear()


    def Question(self):
        self.client_socket.send('문제풀기'.encode())
        self.stackedWidget.setCurrentIndex(2)

    @pyqtSlot(str)
    def Question_recv(self, de_mge):
        self.sub_num+=1
        print('question')
        Q=de_mge.split('/')[1]
        # a = eval(de_mge)
        # print(type(a), a)
        # for i in de_mge:
        #     self.dic_list.append(i)
        self.textBrowser_2.clear()
        self.lineEdit_7.clear()
        self.textBrowser_2.append(Q)
        self.label_9.setText(str(self.sub_num))
            # self.label_9.setText(self.dic_list[0])

    def answer(self):
        a = '정답/'+self.lineEdit_7.text()
        self.client_socket.send(a.encode())

    @pyqtSlot(str)
    def answer_recv(self, de_mge):
        print('answer')
        if de_mge.split('/')[1] == '정답임':
            QMessageBox.question(self, '안내문', '정답', QMessageBox.Yes)

        elif de_mge.split('/')[1] == '실패임':
            QMessageBox.question(self, '안내문', '오답', QMessageBox.Yes)

        # Q = de_mge.split('/')[1]
        # self.textBrowser_2.clear()
        # self.textBrowser_2.append(Q)

    def join(self):
        join_info = ['학생', self.lineEdit.text() ,self.lineEdit_2.text(),self.lineEdit_3.text(), self.lineEdit_4.text()]
        sql = 'join/'+str(join_info)
        self.client_socket.send(sql.encode())
        print('send', sql)

    @pyqtSlot(str)
    def join_recv(self, de_mge):
        print('join')
        if de_mge.split('/')[1] == '아이디중복':
            QMessageBox.question(self, '안내문', '중복된 아이디 입니다. ', QMessageBox.Yes)
        if de_mge.split('/')[1] == '회원가입완료':
            QMessageBox.question(self, '안내문', '회원가입 완료. ', QMessageBox.Yes)

    def login(self):
        login_info = ['학생', self.lineEdit_5.text() ,self.lineEdit_6.text()]
        self.user_id=login_info[1] # 로그인 시도할 때 아이디 저장.
        print(self.user_id)

        sql = 'login/'+str(login_info)
        self.client_socket.send(sql.encode())
        print('send', sql)

    @pyqtSlot(str)
    def login_recv(self, de_mge):
        print('login')
        if de_mge.split('/')[1] == '성공':
            QMessageBox.question(self, '안내문', '로그인성공', QMessageBox.Yes)
        elif de_mge.split('/')[1] == '실패':
            QMessageBox.question(self, '안내문', '아이디와 비밀번호가 일치하지않습니다. 다시 입력해주세요. ', QMessageBox.Yes)
            self.user_id.clear() #로그인 실패시 초기화 추가
        else:
            print(123134,self.user_id)
            QMessageBox.question(self, '안내문', '존재하지 않는 아이디 입니다. 다시 입력해주세요.', QMessageBox.Yes)
            self.user_id.clear()#로그인 실패시 초기화 추가

class Server_message(QThread):
    chat_request = QtCore.pyqtSignal(str)
    server_question = QtCore.pyqtSignal(str)
    server_answer = QtCore.pyqtSignal(str)
    server_join = QtCore.pyqtSignal(str)
    server_login = QtCore.pyqtSignal(str)
    consulting = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Server_message, self).__init__()

    def run(self):
        while True:
            self.client_socket = main.client_socket
            re_message = self.client_socket.recv(4096)
            de_mge = re_message.decode()
            print('쓰레드', de_mge)

            if not de_mge:
                break

            if '[11]' in de_mge:
                self.chat_request.emit(de_mge)

            elif '[22]' in de_mge:
                self.server_question.emit(de_mge)

            elif '[33]' in de_mge:
                self.server_answer.emit(de_mge)

            elif '[44]' in de_mge:
                self.server_join.emit(de_mge)

            elif '[55]' in de_mge:
                self.server_login.emit(de_mge)

            else:
                self.consulting.emit(de_mge)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    main.setWindowTitle('채팅창')
    sys.exit(app.exec_())
