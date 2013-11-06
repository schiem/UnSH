import socket
import os
import sys

HOST = ''
if len(sys.argv)>1:
    PORT = sys.argv[1]
else:
    PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


