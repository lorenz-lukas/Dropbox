# coding=utf-8
import pLukas as pl
import sys
from os import walk
from os import listdir
from os import path
from os import remove
from os import makedirs
from os import chdir
from os import getcwd
import ast
import errno
import json
import shutil

def checkUserName(user, password, IP, PORT):
    soc = pl.connectionClient()
    # Handshake
    message = {'user': user, 'password': password, 'IP': '0.0.0.0', 'Port': PORT,'command': None,'Argument':None,'data': None, 'path': None}
    pl.sendFile(message,soc)
    file = pl.receiveFile(soc)
    print 'ok'
    return int(file['data']),soc,file

def checkDir(soc,user_data):
    user_data['command'] = 'checkdir'
    pl.sendFile(user_data,soc)
    file = pl.receiveFile(soc)
    #user_data = {'user': str(file['user']), 'password': str(file['password']),
    #            'IP': str(file['IP']), 'Port': str(file['Port']),
    #            'command': str(file['command']),'Argument':str(file['Argument']),
    #            'data': str(file['data']), 'path': str(file['path'])}
    user_data = json.dumps(file)
    user_data = ast.literal_eval(user_data)
    dir = ast.literal_eval(user_data['data'])
    for i in dir:
        print i

def removeFile(file_name,soc,user_data):
    user_data['command'] = 'rm'
    user_data['Argument'] = file_name
    pl.sendFile(user_data,soc)
    message = pl.receiveFile(soc)
    if message['data'] == 0:
        print("Error: %s file not found" % file_name)
    else:
        print("File %s removed successful" %file_name)

def moveFile(args,soc,user_data):
    user_data['command'] = 'mv'
    user_data['Argument'] = args
    pl.sendFile(user_data,soc)

def goToDir(args,soc,user_data):
    user_data['command'] = 'cd'
    user_data['Argument'] = args
    pl.sendFile(user_data,soc)
    user_data = pl.receiveFile(soc)
    return user_data

def printDir(file):
    pth = '~'
    pth +=('/'+file['path'])
    return (pth + '$' + ' Set command: ')

def mkDir(args,soc,user_data):
    user_data['command'] = 'makedir'
    user_data['Argument'] = args
    pl.sendFile(user_data,soc)

def exit(soc,user_data):
    user_data['command'] = 'exit'
    pl.sendFile(user_data,soc)
    string = pl.receiveFile(soc)
    if string['data'] == 'ok':
        soc.close()
        print "Exiting..."
        sys.exit()

def upload(file,soc,user_data):
    root, dirs, files = walk('.').next()
    print 'Files in current client directory:'
    print files
    print 'Folders in current client directory:'
    print dirs
    found = 0
    for i in files:
        found = 1
        makedirs('temp')
        shutil.move(file[0],'temp')
        file[0] = 'temp'
    for i in dirs:
        if i == file[0]:
            found = 1
    if found:
        dirpath = getcwd()
        user_data['command'] = 'upload'
        user_data['Argument'] = file[0]
        pl.sendFile(user_data,soc)
        shutil.make_archive(dirpath + '/' + file[0], 'zip', file[0])
        size = path.getsize(file[0]+'.zip')
        soc.send(str(size))
        Handshake = soc.recv(2)
        if Handshake == 'ok': # if authorized to send then send
            print "Uploading", file[0]," ..."
            with open(file[0] + '.zip','rb') as f:
                data = f.read(1024)
                while data:
                    soc.send(data)
                    data = f.read(1024)
            remove('temp.zip')
            shutil.rmtree('temp', ignore_errors=True)
        else:
            print "Error to send file",file[0]," to Server."
    else:
        print("Error: %s file not found" % file)

def download(file,soc,user_data):
    user_data['command'] = 'download'
    user_data['Argument'] = file
    pl.sendFile(user_data,soc)
    print 'User: ',user_data['user']
    print 'Downloading file: ', user_data['Argument']
    with open(file[0]+'.zip', 'wb') as f:
        file_size = soc.recv(1024)
        file_size = int(file_size)
        rsize = 0
        soc.send("ok") # Handshake
        while True:
            print 'Downloading...'
            data = soc.recv(1024)
            rsize += len(data)
            f.write(data)
            if  rsize >= file_size:
                break
    # Unzip file
    #remove(file['Argument'] + '.zip')

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass

## references:
#http://www.pythonforbeginners.com/os/python-the-shutil-module
#
