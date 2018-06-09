import socket
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
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

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
    return {'user': arg[0], 'password': arg[1],'Argument':arg[2], 'IP': arg[3], 'Port': arg[4],'command': arg[5],'data': arg[6], 'path': arg[7]}

def connectionServer(PORT):
    global soc
    soc.bind(('0.0.0.0'),int(PORT))
    soc.listen(1)
    while(1):
        ref_socket, client_port = socket.accept() # Refsocket, ClientIP/PORT

        try:
            thread.start_new_thread( ser.service, (ref_socket, PORT))
        except:
            print "Error: Unable to connect to server."

        # Thread(client)
        # socket.close
    #soc.close() #Close connection

def connectionClient(user,password,ip,PORT):
    global soc
    soc.bind(('0.0.0.0'),int(PORT))
    soc.listen(1)
    sendFile(file = {'user': user, 'password': password, 'IP': ip, 'Port': port,'command': None,'Argument':None,'data': None, 'path': None})
    # socket.close
    #soc.close() #Close connection

def receiveFile():
    global soc
    ip,port = IP()
    soc.connect((ip,port))
    len = soc.receive(50)
    file = soc.recv(len)
    ## descomprimir e mudar o file para
    return file

def sendFile(file):
    global soc
    ip = file['IP']
    port = file['Port']
    len_file = len(bin(file))
    soc.connect((ip, port))
    soc.send(len_file)
    soc.send(file)

def IP():
    pass

### IP Loop-back - servidor local: 127.0.0.1
if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass
