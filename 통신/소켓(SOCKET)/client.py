# 클라이언트
import socket
s = socket.socket()
s.connect(('localhost', 9090))
# 서버로 걸기
s.send('안녕, 서버'.encode())
print(s.recv(1024).decode())
s.close()