# -*- coding: utf-8 -*-
import socket
from os import walk
from os import listdir
from os import chdir
from os import makedirs
from os import getcwd
from time import sleep
import ast
import errno
import json
import sys
import thread
import threading as th
import server_lib as sr

server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ClientLog = []
connected = 1
ListThread = []
num_th = 0
def message(arg):
    return {'user': arg[0], 'password': arg[1],'IP': arg[2], 'Port': arg[3],'command': arg[4],'Argument':arg[5],'data': arg[6], 'path': arg[7]}

def service(refSocket,clientData,server_soc,root):
    global ClientLog, connected, ListThread, num_th
    server_ip = '0.0.0.0'
    num_thread = th.active_count()
    #print num_thread
    current_directory = 'Home'
    if num_thread == 1:
        sr.checkServer()
    else:
        dirpath = getcwd()
        #print dirpath
        string = dirpath.split('/')
        for i in xrange(len(string)):
            if i == 'Home':
                path = string[0:i]
                directory = string[i:len(string)]
        current_directory = []
        for i in directory:
            current_directory = current_directory + i + '/'
    dirpath = getcwd()
    #print dirpath
    string = dirpath.split('/')
    if string[-1] != 'Home':
        chdir(current_directory)

    print "Server initialized. Connected to: ",clientData,"\n"
    ip,port = clientData  #127.0.0.1 , port_interface

    file = receiveFile(refSocket)
    status = sr.login(file['user'],file['password'])
    path = 'Home'+'/'+file['user']
    file = message([file['user'],file['password'],ip,port,None,None,status,path])
    sendFile(file,refSocket)
    sr.mkDir(file['user'])
    chdir(file['user'])
    log_file = []
    online = 1
    if status:
        while online:
            sleep(0.1) #sync
            #print file['path']
            file = receiveFile(refSocket)
            path_dir = sr.getPath(file)
            chdir(path_dir)
            #note(file,refSocket)
            log_file.append((file['command'],file['Argument']))
            if file['command'] == 'help':
                listCommand(file,refSocket)
            elif file['command'] == 'checkdir':
                sr.checkDir(file,refSocket)
            elif file['command'] == 'rm':
                sr.removeFile(file,refSocket)
            elif file['command'] == 'mv':
                sr.moveFile(file,refSocket)
            elif file['command'] == 'cd':
                path = sr.goToDir(file,refSocket)
                #chdir(file['Argument'])
            elif file['command'] == 'makedir':
                sr.mkDir(file['Argument'])
            elif file['command'] == 'upload':
                sr.upload(file,refSocket)
            elif file['command'] == 'download':
                sr.download(file,refSocket)
            elif file['command'] == 'exit':
                online = sr.exit(file,refSocket)
            else:
                print 'Bad Argument.\n'
        dirpath = getcwd()
        dir = dirpath.split('/')
        directory = ''
        for i in xrange(len(dir)):
            if dir[i] == 'Home':
                directory = dir[0:i+1]
        p = ''
        for i in xrange(len(directory)):
            p += directory[i] + '/'
        chdir(p+file['user'])
        with open('LogFile.json','w') as outfile:
            outfile.write(json.dumps(log_file,indent = True))
    num_th = num_th - 1

def note(file,soc):
    global ListThread
    ListThread.append(soc)
    while ListThread[0] != soc:
        print ListThread[0]
        sleep(0.1)

def connectionServer():
    global server_soc,num_th,connected
    PORT = 1234
    server_soc.bind(('0.0.0.0',int(PORT))) #Host and Port
    server_soc.listen(1)
    print "Waiting connection...\n\n"
    while True:
        num_th+=1
        ref_soc, client = server_soc.accept()
        ClientLog.append(ref_soc)
        if num_th == 0:
            break
        t = thread.start_new_thread(service, tuple([ref_soc, client,server_soc,'Home']))
        #t.join()
    server_soc.close()
    print "Exiting..."
    sys.exit()

def receiveFile(soc):
    len = soc.recv(1024)
    soc.send('ok')
    file = soc.recv(int(len))
    file = json.loads(file)#file.decode('ascii')
    file = {'user': str(file['user']), 'password': str(file['password']),
            'IP': str(file['IP']), 'Port': str(file['Port']),
            'command': str(file['command']), 'Argument': str(file['Argument']),
            'data': str(file['data']), 'path': str(file['path'])}
    arg = file['Argument']

    if arg.find(',') != -1:
        arg1,arg2 = arg.split(',')
        j = 0
        d = ''
        len = 0
        for i in arg1:
            len+=1
        if arg1[1] == 'u':
            d = arg1[3:len-1]
        j = 0
        d2 = ''
        len = 0
        for i in arg2:
            len+=1
        if arg2[1] == 'u':
            d2 = arg2[3:len-2]
        if d != '' and d2 != '':
            file['Argument'] = [str(d),str(d2)]
    else:
        j = 0
        d = ''
        len = 0
        for i in arg:
            len+=1
        if arg[1] == 'u':
            d = arg[3:len-2]
        if d != '':
            file['Argument'] = str(d)
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
