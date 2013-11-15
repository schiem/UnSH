What it is:
UnSH provides an insecure means of connecting two computers, allowing basic terminal commands which rely on stdout, stdin and stderr to be run.  One machine functions as a server, while the other functions as a client.  Files can also be transferred from one machine to another using a set of commands provided by UnSH.  Address scanning in order to find machines willing to accept connections is coming soon.

How it works:
Python sockets were used to establish a connection between the two machines, with one acting as a client and the other acting as a server.  The client would receive commands to be run from the command line and send them as strings to the server.  The server would execute the commands, record the output, and send that data back to the client.
File sharing was also implemented by writing a very small protocol which sits on top of TCP.  Because TCP only allows packets of a certain size, most files could not be sent in a single packet.  This resulted in parts of files essentially being lost, as the client would top listening after the end of a data stream was reached.  To counter this, each file is prefaced with an eight byte header which contains the length of the following file.  The client is then told to continue to receive data from the server until data which satisfies the length of the file has been received.
The same protocol was implemented for sending files from the client to the server.
Address scanning will be implemented soon, which will allow for the discovery of servers that are listening on a particular port.  A range of IP addresses could be put in, and those would be scanned for listening servers.  Any of the listening servers could then be connected to.

How to use it:
On the server machine, run the command "python server.py" with the option argument of -p to specify a port ("python server.py -p 2000").  On unix systems, this can be run in the background by appending an "&" to the end of the command.  The default port is 5000.

On the client machine, run the command "python client.py -a {IP-Address}" with the optional argument of -p to specify a port.  If -a is not specified, the default address is localhost (127.0.0.1) and port 5000.  The -s flag will be implemented soon, which will allow for address scannning.

Once the connection is established, commands can be typed on the client as if in a normal bash prompt.  However, tab to auto-complete has not yet been implemented.  The command "grab {file}" can be used to get a file from the current directory of the server and place it in the same directory of as the client.py file.  The command "put {file}" is used to place a file in the same directory as the client.py onto the current directory of the server.  Note: grab and put may have slightly erratic behavior from machine to machine.

Ideally, this project is cross platform, but it has only been tested on Unix based systems (OsX, linux).
Commands like vim, nano, lynx, etc. will not work because they do not rely on the terminal standard windows. 

In file documentation coming soon!
