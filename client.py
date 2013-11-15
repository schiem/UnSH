import socket
import os
import sys
import struct

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

def put(file_name):
    
    read_file =  open(file_name, "rb")
    file_string = read_file.read()
    read_file.close()
    file_size = len(file_string)
    return (struct.pack('>Q', file_size) +  file_string)

def get_file(sock):
    full_message = recvall(sock, 8)
    print full_message
    if not full_message:
        return None
    mess_length = struct.unpack('>Q', full_message)[0]
    return recvall(sock, mess_length)

def recvall(sock, n):
    data = ''
    while len(data) < n:
        print "Receiving data of size " + str(n-len(data))
        piece = sock.recv(n - len(data))
        print "Data received."
        if not piece:
            print "No data received."
            return None
        data += piece
    return data

def open_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

if __name__ == "__main__":
    s = open_connection()
    while 1:
        command = raw_input('>')
        s.sendall(command)
        if command.split()[0] == "grab":
            data = get_file(s)
            open(command.split()[1], "wb").write(data)
            data = "Written successfully"
        elif command.split()[0] == "put":
            s.sendall(put(command.split()[1]))
            data = "Send successfully"
            data = s.recv(1024)
        else:    
            data = s.recv(1024)
        if data == "exit":
            break
        else:
            print data

    s.close()
