# 서버
import socket
s = socket.socket()
s.bind(('localhost', 9090))
# 내 주소 걸기
s.listen(1)
conn, addr = s.accept()
# 손님 올 때까지 멈춤
print(conn.recv(1024).decode())
conn.send('안녕, 클라이언트'.encode())
conn.close()
s.close()