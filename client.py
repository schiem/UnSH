import socket
import os
import sys

'''
Command line arguments.
Default to localhost and port 5000
'''
if '-p' in sys.argv:
    try:
        PORT = int(sys.argv[sys.argv.index('-p') + 1])
    except:
        print "Invalid port input"
        PORT = 5000
else:
    PORT = 5000

if '-a' in sys.argv:
    try:
        HOST = sys.argv[sys.argv.index('-a') + 1]
    except:
        print "Invalid address option"
        HOST = 'localhost'
else:
    HOST = 'localhost'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while 1:
    s.sendall(raw_input('>'))
    data = s.recv(1024)
    print data

s.close()
