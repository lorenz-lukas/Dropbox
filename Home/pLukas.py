# coding=utf-8
import socket
from os import walk
from os import listdir
import json
import sys
#from threading import Thread #https://www.tutorialspoint.com/python/python_multithreading.htm
import thread
import server_lib as sr
from time import sleep
#{'op': op_name,'file' : file.encode('base64'), 'path': path_name, 'user', int_user}
#from datetime import datetime
#datetime.utcnow()
### Baseado no HTTP com uso de sockets e TCP
server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

def service(refSocket,clientData,server_soc):
    server_ip = '0.0.0.0'
    sr.checkServer()
    print "Server initialized. Connected to: ",clientData,"\n\n\n"
    ip,port = clientData #127.0.0.1 , port_interface
    file = receiveFile(refSocket)
    status = sr.login(file['user'],file['password'])
    file = message([file['user'],file['password'],None,None,ip,port,status,None])
    sendFile(file,refSocket)
    sr.mkDir(file['user'])
    sr.goToDir(file['user'])
    if status:
        while file['command']!='exit':
            file = receiveFile(refSocket)
            if file['command'] == 'help':
                listCommand()
            elif file['command'] == 'checkdir':
                cl.checkDir()
            elif file['command'] == 'rm':
                cl.removeFile(arg)
            elif file['command'] == 'mv':
                cl.moveFile(arg)
            elif file['command'] == 'cd':
                cl.goToDir(arg)
            elif file['command'] == "makedir":
                cl.mkDir(arg)
            elif file['command'] == "upload":
                pass
            elif file['command'] == "download":
                pass
            else:
                print 'Bad Argument.\n'

def connectionServer():
    global server_soc
    PORT = 1234
    server_soc.bind(('0.0.0.0',int(PORT))) #Host and Port
    server_soc.listen(1)
    print "Waiting connection...\n\n"
    while True:
        #ref_socket, client = soc.accept() # Refsocket, ClientIP/PORT
        #client_handler = Thread(targetservice,args=(ref_socket, client,))
        #client_handler.start()
        ref_soc, client = server_soc.accept()
        thread.start_new_thread(service, tuple([ref_soc, client,server_soc]))

    server_soc.close()
    #except KeyboardInterrupt as e:
    #    ref_socket.close()
    #    client_handler.exit()
    print "Exiting..."
    sys.exit()
    #finally:
    #    print "Error: Unable to connect to server."

def connectionClient():
    client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    port = 1234
    client_soc.connect((ip,port))
    return client_soc
    #soc.close()

def receiveFile(soc):
    len = soc.recv(1024)
    file = soc.recv(int(len))
    file = json.loads(file)#file.decode('ascii')
    file = {'user': str(file['user']), 'password': str(file['password']),'command': str(file['command']),'Argument':str(file['Argument']), 'IP': str(file['IP']), 'Port': str(file['Port']),'data': str(file['data']), 'path': str(file['path'])}
    return file

def sendFile(file,soc):
    ip = file['IP']
    port = file['Port']
    string = json.dumps(file)#string.encode('ascii')
    f = str(file)
    len_file = len(f.encode('utf-8'))#len(file)
    soc.send(str(len_file))
    sleep(0.1)
    soc.send(string)

### IP Loop-back: 127.0.0.1
if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    print 'This is a library programm.\n'
    return 1
