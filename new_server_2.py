import sqlite3
from socket import *
from threading import *


class MultiChatServer:
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.user_id=[]
        self.user_pw=[]
        self.Q_dic={}
        self.Q_dic_subjet_answer ={}
        self.dic_A_list=[]
        self.dic_Q_list=[]
        self.all=[]
        self.chat=False
        self.graph={'경영': 0, '경제': 0, '공공': 0, '과학': 0, '금융': 0, '사회': 0}

        # self.final_received_message = '' #최종 수신 메세지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = 'localhost'
        self.port = 50008
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        self.s_sock.listen(50)
        print('클라이언트 대기 중....')
        self.data_load()
        self.accept_client()

        # 데이터베이스 저장
        self.db_education = list()  #회원가입 정보
        self.db_study = list() #학습진도 정보

    def accept_client(self):
        while True:
            client_socket, address = self.s_sock.accept()
            # 클라이언트 이름 넣는 과정
            if client_socket not in self.clients:
                self.clients.append(client_socket)
            print(address, '가 연결되었습니다.')
            cth = Thread(target=self.received_message, args=(client_socket,))
            cth.start()

    def data_load(self):
        conn = sqlite3.connect("education")
        cur = conn.cursor()

        cur.execute("SELECT * FROM data_Q2")
        diclist = cur.fetchall()

        for i in diclist:
            a = list(i)
            self.Q_dic[a[2]] = a[1]
            self.Q_dic_subjet_answer[a[1]] = a[0]
            self.all.append(a)

        for i in range(len(self.all)):
            self.dic_Q_list.append(self.all[i][2])
            self.dic_A_list.append(self.all[i][1])

    # 메세지 받기
    def received_message(self, client_socket):
        sub_list = ['경영', '경제', '공공', '과학', '금융', '사회']
        print(self.user_id)

        while True:
            conn = sqlite3.connect("education")
            cur = conn.cursor()
            incoming_message = client_socket.recv(4096)
            self.cl_message = incoming_message.decode()
            print(11,self.cl_message)
            if not self.cl_message:
                break
            if self.cl_message.split('/')[0] == '업데이트':
                teacher_update=eval(self.cl_message.split('/')[1])
                print(teacher_update)

                conn = sqlite3.connect("education")
                cur = conn.cursor()
                # sql = "INSERT INTO dic(num,answer,question) VALUES(?, ?, ?)"
                sql = "INSERT INTO data_Q2(sub,answer,question) VALUES(?, ?, ?)"
                val = tuple(teacher_update)
                cur.execute(sql, val)
                conn.commit()
                

            if self.cl_message.split('/')[0] == '정답':
                print(4164684,self.cl_message.split('/')[0])
                ans = self.cl_message.split('/')[1]
                print(ans)

                if ans in self.dic_A_list:
                    index = self.dic_A_list.index(ans)
                    if self.Q_dic[self.dic_Q_list[index]] == ans:
                        client_socket.send('[33]/정답임'.encode())
                        cur.execute("select * from usertbl where userid = ? ", (self.user_id,))  # 정답시 포인트 증가 추가
                        num = cur.fetchall()[0][7]
                        cur.execute("update usertbl set point=? where userid=?", (num + 1, self.user_id))
                        conn.commit()
                        
                        print('맞아서 보냇다')
                        for i in sub_list:
                            if self.Q_dic_subjet_answer[ans] == i:
                                self.graph[i] += 1
                            else:
                                pass

                        print(self.graph)
                        # mun1="update usertbl set 경영=? where userid=?", (self.graph['경영'], self.user_id)
                        cur.execute("update usertbl set 경영=? where userid=?", (self.graph['경영'], self.user_id))
                        print('경영넣음')
                        cur.execute("update usertbl set 경제=? where userid=?", (self.graph['경제'], self.user_id))
                        # conn.commit(),print('경제넣음')
                        cur.execute("update usertbl set 공공=? where userid=?", (self.graph['공공'], self.user_id))
                        # conn.commit()
                        cur.execute("update usertbl set 과학=? where userid=?", (self.graph['과학'], self.user_id))
                        # conn.commit()
                        cur.execute("update usertbl set 금융=? where userid=?", (self.graph['금융'], self.user_id))
                        # conn.commit()
                        cur.execute("update usertbl set 사회=? where userid=?", (self.graph['사회'], self.user_id))
                        conn.commit()


                    else:
                        client_socket.send('[33]/실패임'.encode())
                        print('틀려서 보냇다.')

                else:
                    # client_socket.send('[33]/실패임'.encode())
                    client_socket.send('[33]/실패임'.encode())
                    print('틀려서 보냇다.')

                cur.execute("select * from usertbl where userid = ? ", (self.user_id,))  # 문제 레벨 증가 추가
                num = cur.fetchall()[0][5]
                print(num)
                num +=1
                cur.execute("update usertbl set question_Lv=? where userid=?", (num, self.user_id))
                conn.commit()
             
                #num += 1
                b = '[22]/'+str(self.dic_Q_list[num])
                print(b)
                client_socket.send(b.encode())
                print('보냄')


            if self.cl_message =='문제풀기':
                cur = conn.cursor()
                cur.execute("select * from usertbl where userid = ? ", (self.user_id,))  # db에 저장된 데이터 가져와서 적용하기
                num = cur.fetchall()[0][5]
                # b = '[22]/'+str(self.dic_Q_list[num])
                b = '[22]/'+str(self.dic_Q_list[num])
                print(1,b)
                client_socket.send(b.encode())
                print(2,'보냄')
                # num += 1
                
            #로그인                    self.user_pw.append(i[2]) 함수
            if self.cl_message.split('/')[0]=='login':
                conn = sqlite3.connect("education")
                cur = conn.cursor()
                cur.execute("SELECT * FROM usertbl")
                userlist = cur.fetchall()

                for i in userlist:
                    self.user_id.append(i[1])
                    self.user_pw.append(i[2])

                a = eval(self.cl_message.split('/')[1])
                inputid = a[1]
                inputpw = a[2]
                print(self.user_id)
                print(inputid)
                if inputid in self.user_id:
                    self.id_index = self.user_id.index(inputid)
                    if self.user_pw[self.id_index] == inputpw:
                        client_socket.send('[55]/성공'.encode())
                        # print("로그인에 성공하셨습니다")
                        self.user_id = a[1]


                    else:
                        client_socket.send('[55]/실패'.encode())
                        # print("로그인에 실패")

                else:
                    client_socket.send('[55]/아이디없음'.encode())

                # self.user_id.clear() #주석
                # self.user_pw.clear()


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
                    sql = "INSERT INTO usertbl(job, userid, userpw, username, userphone, question_Lv, class, point, learning_Lv) VALUES(?, ?, ?, ?, ?, 0, 0, 0, 0)" #db파일 내용 추가
                    val = tuple(self.db_education)
                    cur.execute(sql, val)
                    conn.commit()
                    
                    print('삽입완료')


            # 만약 인덱스의 1번째가 //학습진도이면 학습진도 DB에 저장해라
            if self.cl_message.split('/')[0] == '학습진도':
                self.db_study.append(self.cl_message[2])
                # 학습진도 DB 저장
                conn = sqlite3.connect("education")
                cur = conn.cursor()
                sql = self.db_study(tuple)  # 튜플로 변환 이게 맞는지 모르겠어요. 주석
                print(sql)
                cur.execute(sql)
                conn.commit()
                

            # 1대1 상담요청
            if self.cl_message.split('/')[0] == 'chat':

                    if self.cl_message.split('/')[1] == '채팅요청':
                        # self.final_received_message ='[11]/채팅요청'
                        # self.send_all_clients(client_socket)
                        for client in self.clients:
                            if client is not client_socket:
                                client.send('[11]/채팅요청'.encode())

                    elif self.cl_message.split('/')[1] == '채팅거부':
                        # self.final_received_message = '[11]/채팅거부'
                        # self.send_all_clients(client_socket)
                        for client in self.clients:
                            if client is not client_socket:
                                client.send('[11]/채팅거부'.encode())

                    elif self.cl_message.split('/')[1] == '채팅수락':
                        # self.final_received_message = '[11]/채팅수락'
                        # self.send_all_clients(client_socket)
                        for client in self.clients:
                            if client is not client_socket:
                                client.send('[11]/채팅수락'.encode())

                    else:
                        for client in self.clients:
                            if client is not client_socket:
                                client.send(self.cl_message.split('/')[1].encode())

                        # self.final_received_message = self.cl_message.split('/')[1]
                        # print(1, self.final_received_message)
                        # self.send_all_clients(client_socket)
                        # print(33)
                        #


    # # 메세지 보내기
    # def send_all_clients(self, client_socket):
    #     print(22)
    #     for client in self.clients:
    #         if client is not client_socket:
    #             client.send(self.final_received_message.encode())

if __name__ == "__main__":
    MultiChatServer()
