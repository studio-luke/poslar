#TODO: accept()[0]에서 [0]이 의미하는 바??
import socket 

class Server(object):

    #initializing function

    #   Description : 컴퓨터에서 소켓을 생성, 바인딩, 리슨을 하고 accpet를 위한 변수를 선언해놓는 생성자
    #   input:
    #       self : 자신의 주소를 가리키는 포인터
    #       host : 호스트의 주소(컴퓨터의 IP 주소)
    #       port : 연결하는 포트 번호
    #   output : None
    def __init__(self, host, port):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        
        self.connection = self.server_socket.accept()[0]
        
    #   Description : 클라이언트와 연결되었을 때 accept를 시작하는 함수
    #   input:
    #       self : 자신의 주소를 가리키는 포인터
    #   output : connection, 즉 클라이언트와 연결을 해주는 함수
    def Get_Client(self):
        return self.connection


    #   Description : 클라이언트와의 연결이 끊어졌을 때 소켓을 제거하는 소멸자
    #   input:
    #       self : 자신의 주소를 가리키는 포인터
    #   output : None
    def __del__(self):
        self.connection.close() #accept를 끊어주는 기능
        self.server_socket.close() #소켓을 없애는 기능

