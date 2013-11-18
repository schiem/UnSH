##############################################################
# client.py
# Part of UnSH, and insecure protocol to connect devices.
# 
# Michael Yoder
# v. 1.0
##############################################################

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

'''
A function which takes in two IPs and a port, and will iterate
through the IPs checking connections.  This checks the last bytes
first.

RETURN: List of IP addresses containing available connections.
'''
def scan_net(ip1, ip2, port):
    ip1_list = ip1.split('.')
    ip2_list = ip2.split('.')
    conn_list = []
    for i in range(int(ip1_list[0]), int(ip2_list[0]) + 1):
        for j in range(int(ip1_list[1]), int(ip2_list[1]) + 1):
            for k in range(int(ip1_list[2]), int(ip2_list[2]) + 1):
                for l in range(int(ip1_list[3]), int(ip2_list[3]) + 1):
                    addr = str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)
                    try:
                        print "Attempting " + addr
                        s = open_connection(addr, port, 0.1)
                        s.close()
                        conn_list.append(addr)
                        print "Found connection at " + addr
                    except:
                        print "No connection found."
    return conn_list

'''
The client side function to send data from client->server.  A file
name is given, and an 8 byte header is appended to a string 
representing the file.

RETURN: A string representation of a file with an 8 byte header
packaged in a struct.
'''
def put(file_name):
    
    read_file =  open(file_name, "rb")
    file_string = read_file.read()
    read_file.close()
    file_size = len(file_string)
    return (struct.pack('>Q', file_size) +  file_string)

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

'''
Takes a host, port, and a timeout, attempting to connect to the
host.

RETURN: A socket object. 
'''
def open_connection(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port))
    return s

'''
The main code loop.  Takes commands from the user, and sends those
to the server.  Special cases are taken for the "grab"/"put" commands.
Received data is printed.  Upon receiving the "exit" command, the client
is terminated.
'''
if __name__ == "__main__":
    '''
    Address scanning, with the -s option.  If no addresses are found, the program will exit.
    '''
    if '-s' in sys.argv:
        ip = raw_input("Input ip address range (separated by a space): ")
        ip_list = scan_net(ip.split()[0], ip.split()[1], PORT)
        if not ip_list:
            print "No open addresses found."
            sys.exit(0)
        else:
            print "Available IPs on port: "
            for i in range(len(ip_list)):
                print str(i) + " " + ip_list[i]
            HOST = ip_list[int(raw_input("Select the IP on the list: "))]

    s = open_connection(HOST, PORT, None)
    print s.recv(1024)
    while 1:
        command = raw_input('>')
        s.sendall(command)
        if command == '':
            data = ''
        elif command.split()[0] == "grab":
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
