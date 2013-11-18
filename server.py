##############################################################
# server.py
# Part of UnSH, and insecure protocol to connect devices.
# 
# Michael Yoder
# v. 1.0
##############################################################

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

'''
This is the server side function to send data from server->client.
A file name is given, and an 8 byte header is appended to a string
representing that file.

RETURN: A string representation of a file with an 8 byte header
packaged in a struct.
'''
def grab(file_name):
    read_file =  open(file_name, "rb")

    file_string = read_file.read()
    read_file.close()
    file_size = len(file_string)
    return struct.pack('>Q', file_size) +  file_string

'''
the server side function to receive a file.  a socket object
is passed in, and the first 8 bytes are read, denoting the file
size.  the rest of the file is then read in based on the length.

return: a string object representing a file.
'''
def get_file(sock):
    full_message = recvall(sock, 8)
    print full_message
    if not full_message:
        return None
    mess_length = struct.unpack('>Q', full_message)[0]
    return recvall(sock, mess_length)

'''
A function which takes a number of bytes, and continue to receive
data until that number of bytes has been received.

RETURN: The data received, None if the string ended early.
'''

def recvall(sock, n):
    dat = ''
    while len(dat) < n:
        piece = sock.recv(n - len(dat))
        if not piece:
            return None
        dat += piece
    return dat


'''
Takes a host and a port and accepts one connection.

RETURN: A socket object with a connection.
'''

def open_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    return s, conn, addr

'''
The main code loop.  Receives data, makes a system call 
or a "grab"/"put" command.  Sends data back.  Upon
receiving an "exit" command, the program is stopped.
If the client disconnects with no "exit", the server accepts
another connection.
'''
if __name__ == "__main__":
    s, conn, addr = open_connection(HOST, PORT)
    conn.sendall('Connection established.')
    while 1:
        data = conn.recv(1024)
        if not data:
            conn, addr = s.accept()
        if data == "exit":
            conn.sendall(data)
            break

        try:
            if data.split()[0] == "grab":
                out = grab(data.split()[1])
            elif data.split()[0] == "put":
                message = get_file(conn)
                open(data.split()[1], "wb").write(message)
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
