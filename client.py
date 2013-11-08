import socket
import os
import sys

if len(sys.argv)>2:
    PORT = sys.argv[1]
    HOST = sys.argv[2]
elif len(sys.argv) == 2:
    PORT = sys.argv[1]
else:
    PORT = 5000
    HOST = 'localhost'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while 1:
    s.sendall(raw_input('>'))
    data = s.recv(1024)
    print data

s.close()
