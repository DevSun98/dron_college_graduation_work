from socket import *

''' 임의의 컴퓨터 비전 프로세스간 통신 테스트 용 클라이언트 프로그램 '''

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))

print('연결 확인 됐습니다.')

while True:
    a = input("데이터를 입럭: ")
    clientSock.send(a.encode('utf-8'))  # 전송
