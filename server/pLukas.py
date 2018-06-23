# coding=utf-8
import socket
from os import walk
from os import listdir
from os import chdir
from time import sleep
import json
import sys
import thread
import server_lib as sr

server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def message(arg):
    return {'user': arg[0], 'password': arg[1],'IP': arg[2], 'Port': arg[3],'command': arg[4],'Argument':arg[5],'data': arg[6], 'path': arg[7]}

def service(refSocket,clientData,server_soc):
    server_ip = '0.0.0.0'
    sr.checkServer()
    print "Server initialized. Connected to: ",clientData,"\n\n\n"
    ip,port = clientData #127.0.0.1 , port_interface
    file = receiveFile(refSocket)
    status = sr.login(file['user'],file['password'])
    file = message([file['user'],file['password'],ip,port,None,None,status,None])
    sendFile(file,refSocket)
    sr.mkDir(file['user'])
    chdir(file['user'])
    if status:
        while file['command']!='exit':
            sleep(0.1) #sync
            file = receiveFile(refSocket)
            if file['command'] == 'help':
                listCommand(file,refSocket)
            elif file['command'] == 'checkdir':
                sr.checkDir(file,refSocket)
            elif file['command'] == 'rm':
                sr.removeFile(file,refSocket)
            elif file['command'] == 'mv':
                sr.moveFile(file,refSocket)
            elif file['command'] == 'cd':
                #current_directory = sr.goToDir(file)
                chdir(file['Argument'])
            elif file['command'] == "makedir":
                sr.mkDir(file['Argument'])
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
        ref_soc, client = server_soc.accept()
        thread.start_new_thread(service, tuple([ref_soc, client,server_soc]))

    server_soc.close()
    print "Exiting..."
    sys.exit()

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
