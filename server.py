import sqlite3
from socket import *
from threading import *
import time


class MultiChatServer:
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.user_id = []
        self.user_pw = []
        self.Q_dic = {}
        self.dic_A_list = []
        self.dic_Q_list = []
        self.all = []

        self.final_received_message = '' #최종 수신 메세지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = 'localhost'
        self.port = 50004
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        self.s_sock.listen(50)
        print('클라이언트 대기 중....')
        self.accept_client()

        # 데이터베이스 저장
        self.db_education = list()  #회원가입 정보
        self.db_study = list() #학습진도 정보

   # # 회원가입 db저장
   #  def DB_education(self):
   #      conn = sqlite3.connect("education")
   #      cur = sqlite3.Cursor()
   #      sql = self.db_study(tuple)   # 튜플로 변환 이게 맞는지 모르겠어요.
   #      print(sql)
   #      cur.execute(sql)
   #      conn.commit()
   #      conn.close()
   #
   #  # 학습 진도 db 저장
   #  def DB_study(self):
   #      conn = sqlite3.connect("study")
   #      cur = sqlite3.cursor()
   #      sql = self.db_study(tuple)  # 튜플로 변환 이게 맞는지 모르겠어요.2
   #      cur.execute(sql)
   #      conn.commit()
   #      conn.close()

    def accept_client(self):
        while True:
            client_socket, address = self.s_sock.accept()
            # 클라이언트 이름 넣는 과정
            if client_socket not in self.clients:
                self.clients.append(client_socket)
            print(address, '가 연결되었습니다.')
            cth = Thread(target=self.received_message, args=(client_socket,))
            cth.start()

    # 메세지 받기
    def received_message(self, client_socket):
        conn = sqlite3.connect("education")
        cur = conn.cursor()
        cur.execute("SELECT * FROM usertbl")
        userlist = cur.fetchall()
        num = 0
        for i in userlist:
            self.user_id.append(i[1])
            self.user_pw.append(i[2])


        while True:
            incoming_message = client_socket.recv(4096)
            self.cl_message = incoming_message.decode()
            print(11, self.cl_message)
            if not self.cl_message:
                break

            if self.cl_message.split('/')[0] == '정답':
                print(4164684, self.cl_message.split('/')[0])
                ans = self.cl_message.split('/')[1]
                print(ans)

                if ans in self.dic_A_list:
                    index = self.dic_A_list.index(ans)
                    if self.Q_dic[self.dic_Q_list[index]] == ans:
                        # client_socket.send('[33]/정답임'.encode())
                        client_socket.send('[33]/정답임'.encode())
                        print('맞아서 보냇다')
                        # print("로그인에 성공하셨습니다")
                    else:
                        # client_socket.send('[33]/실패임'.encode())
                        client_socket.send('[33]/실패임'.encode())
                        print('틀려서 보냇다.')
                else:
                    # client_socket.send('[33]/실패임'.encode())
                    client_socket.send('[33]/실패임'.encode())
                    print('틀려서 보냇다.')

                num += 1
                b = '[22]/'+str(self.dic_Q_list[num])
                print(b)
                client_socket.send(b.encode())
                print('보냄')

            if self.cl_message =='문제풀기':
                cur.execute("SELECT * FROM dic")
                diclist = cur.fetchall()
                # print(self.dic_list)
                for i in diclist:
                    a = list(i)
                    self.Q_dic[a[2]] = a[1]
                    self.all.append(a)
                    # print(len(self.Q_dic))

                for i in range(len(self.all)):
                    self.dic_Q_list.append(self.all[i][2])
                    self.dic_A_list.append(self.all[i][1])

                # print(self.Q_dic)
                b = '[22]/'+str(self.dic_Q_list[0:6])
                print(b)
                client_socket.send(b.encode())
                print('보냄')

            #로그인                    self.user_pw.append(i[2]) 함수
            if self.cl_message.split('/')[0]=='login':
                # conn = sqlite3.connect("education")
                # cur = conn.cursor()
                cur.execute("SELECT * FROM usertbl")
                userlist = cur.fetchall()
                for i in userlist:
                    self.user_id.append(i[1])
                    self.user_pw.append(i[2])
                # cur.execute("SELECT * FROM usertbl")
                a = eval(self.cl_message.split('/')[1])
                inputid = a[1]
                inputpw = a[2]
                # userlist = cur.fetchall()
                # for i in userlist:
                #     self.user_id.append(i[1])
                #     self.user_pw.append(i[2])

                if inputid in self.user_id:
                    self.id_index = self.user_id.index(inputid)
                    if self.user_pw[self.id_index] == inputpw:
                        client_socket.send('[55]/성공'.encode())
                        # print("로그인에 성공하셨습니다")

                    else:
                        client_socket.send('[55]/실패'.encode())
                        # print("로그인에 실패")

                else:
                    client_socket.send('[55]/아이디없음'.encode())
                    # print("아이디없음")

            #만약 인덱스의 1번째가 //회원가입이면 회원가입 DB에 저장해라
            if self.cl_message.split('/')[0] == 'join':
                a = eval(self.cl_message.split('/')[1])
                input_id = a[1]
                if input_id in self.user_id:
                    client_socket.send('[44]/아이디중복'.encode())
                else:
                    self.db_education = eval(self.cl_message.split('/')[1])
                    client_socket.send('[44]/회원가입완료'.encode())
                    print(tuple(self.db_education))
                    # 회원가입 DB 저장
                    sql = "INSERT INTO usertbl(job, userid, userpw, username, userphone) VALUES(?, ?, ?, ?, ?)"
                    val = tuple(self.db_education)
                    cur.execute(sql, val)
                    conn.commit()
                    conn.close()
                    print('삽입완료')


            # 만약 인덱스의 1번째가 //학습진도이면 학습진도 DB에 저장해라
            if self.cl_message.split('/')[0] == '학습진도':
                self.db_study.append(self.cl_message[2])
                # 학습진도 DB 저장
                conn = sqlite3.connect("education")
                cur = conn.cursor()
                sql = tuple(self.db_study)  # 튜플로 변환 이게 맞는지 모르겠어요.
                print(sql)
                cur.execute(sql)
                conn.commit()
                conn.close()

            # 1대1 상담요청
            if self.cl_message.split('/')[0] == 'chat':

                if self.cl_message.split('/')[1] == '채팅요청':
                    for client in self.clients:
                        if client is not client_socket:
                            client.send('[11]/채팅요청'.encode())

                elif self.cl_message.split('/')[1] == '채팅거부':
                    for client in self.clients:
                        if client is not client_socket:
                            client.send('[11]/채팅거부'.encode())

                elif self.cl_message.split('/')[1] == '채팅수락':
                    for client in self.clients:
                        if client is not client_socket:
                            client.send('[11]/채팅수락'.encode())

            else:
                final_received_message = incoming_message.decode()
                print(1, final_received_message)
                self.send_all_clients(client_socket, final_received_message)
                print(33)

    # 메세지 보내기
    def send_all_clients(self, client_socket, final_received_message):
        print(22)
        for client in self.clients:
            if client is not client_socket:
                client.send(final_received_message.encode())

if __name__ == "__main__":
    MultiChatServer()
