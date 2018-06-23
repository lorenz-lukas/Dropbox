# coding=utf-8
import socket
from os import walk
from os import listdir
import json
import sys
#from threading import Thread #https://www.tutorialspoint.com/python/python_multithreading.htm
import thread
from time import sleep
#{'op': op_name,'file' : file.encode('base64'), 'path': path_name, 'user', int_user}
#from datetime import datetime
#datetime.utcnow()
### Baseado no HTTP com uso de sockets e TCP

def message(arg):
    return {'user': arg[0], 'password': arg[1],'IP': arg[2], 'Port': arg[3],'command': arg[4],'Argument':arg[5],'data': arg[6], 'path': arg[7]}

def connectionClient():
    client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    port = 1234
    client_soc.connect((ip,port))
    return client_soc
    #soc.close()

def receiveFile(soc):
    len = soc.recv(1024)
    soc.send('ok')
    file = soc.recv(int(len))
    file = json.loads(file)#file.decode('ascii')
    file = {'user': str(file['user']), 'password': str(file['password']),'IP': str(file['IP']), 'Port': str(file['Port']),'command': str(file['command']),'Argument':str(file['Argument']),'data': str(file['data']), 'path': str(file['path'])}
    return file

def sendFile(file,soc):
    ip = file['IP']
    port = file['Port']
    string = json.dumps(file)#string.encode('ascii')
    f = str(file)
    len_file = len(f.encode('utf-8'))#len(file)
    soc.send(str(len_file))
    s = 'wait'
    while s != 'ok': #sync
        s = soc.recv(1024)
        sleep(0.01)
    soc.send(string)
### IP Loop-back: 127.0.0.1
if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    print 'This is a library programm.\n'
    return 1
