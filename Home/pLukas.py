from socket import (socket, AF_INET, SOCK_STREAM)
from os import walk
from os import listdir
import server_lib as ser
import json
import sys
from threading import Thread #https://www.tutorialspoint.com/python/python_multithreading.htm
#{'op': op_name,'file' : file.encode('base64'), 'path': path_name, 'user', int_user}
#from datetime import datetime
#datetime.utcnow()
### Baseado no HTTP com uso de sockets e TCP
client_soc = socket(AF_INET,SOCK_STREAM)
server_soc = socket(AF_INET,SOCK_STREAM)
def get():
    pass
def post():
    pass
def update():
    pass
def delete():
    pass
def error():
    pass

def message(arg):
    return {'user': arg[0], 'password': arg[1],'command': arg[2],'Argument':arg[3], 'IP': arg[4], 'Port': arg[5],'data': arg[6], 'path': arg[7]}

def connectionServer():
    global server_soc
    soc = None
    try:
        soc = server_soc
        PORT = 1234
        soc.bind(('',int(PORT))) #Host and Port
        soc.listen(1)
        print "Waiting connection...\n\n"
        while True:
            ref_socket, client = soc.accept() # Refsocket, ClientIP/PORT
            client_handler = Thread(
            target=ser.service,
            args=(ref_socket, client,)
            )
            client_handler.start()
    except KeyboardInterrupt as e:
        soc.close()
        print "Exiting..."
        sys.exit()
    finally:
        print "Error: Unable to connect to server."

def connectionClient(user,password,ip,PORT):
    global client_soc
    ip = '127.0.0.1'
    port = 1234
    client_soc.connect((ip,port))
    #soc.close()

def receiveFile(ip,port):
    global client_soc, server_soc
    if ip == '127.0.0.1': # IP_dest
        soc = client_soc
        print 'cade'
    else:
        soc = server_soc
    len = soc.recv(4096)
    file = soc.recv(int(len))
    file = json.loads(file.decode('utf-8'))
    return file

def sendFile(file):
    global client_soc, server_soc
    if file['IP'] == '127.0.0.1': # IP_dest
        soc = client_soc
        print 'oi'
    else:
        soc = server_soc
    ip = file['IP']
    port = file['Port']
    string = json.dumps(file)
    string.encode('ascii')
    len_file = len(file)
    soc.send(str(len_file))
    soc.send(string)

### IP Loop-back - servidor local: 127.0.0.1
if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    print 'This is a library programm.\n'
    return 1
