#-*-coding:utf-8 -*-

# connect to server
# 2018.10.03
# BCODE

import socket

class Connect(object):

    #initializing function
    #   Description : 소켓을 생성해서 연결하는 함수
    #   input:
    #       self : 자신의 주소를 가리키는 포인터
    #       HOST : 
    #       PORT : 연결하는 포트 번호
    #   output : None
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socket.socket() -> 소켓 객체 생성
        #AF_INET과 SOCK_STREAM은 family와 type의 기본 인자값
        #걍 socket.socket()이라고 써도 상관 없음
        self.server_socket.connect((self.host, self.port))
        #소켓을 host와 port에 연결
        print('Connected')

    def Get_Data(self):
        return self.server_socket.recv(2).decode()
    #소켓으로부터 데이터를 읽는 함수
    
    def Get_Socket(self):
        return self.server_socket
    #서버 소켓을 리턴하는 함수

    def Send_Data(self, data) :
        self.server_socket.send(data)
    #소켓으로 정보를 보내는 함수

    def __del__(self):
        self.server_socket.close()
    #서버 소켓을 닫는 함수
           

