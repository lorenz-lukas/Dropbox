# coding=utf-8
import numpy as np
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

def moveFile(file_name,soc,user_data):
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
    shutil.make_archive(file,
                    'zip',
                    '.',
                    'file')
    with open(file,'r') as infile:
        data = json.loads(infile.read())
    user_data['data'] = data
    user_data['command'] = 'upload'
    user_data['Argument'] = file
    pl.sendFile(user_data,soc)

def download(file,soc,user_data):
    user_data['command'] = 'download'
    user_data['Argument'] = file
    pl.sendFile(user_data,soc)
    file = pl.receiveFile(soc)
    strDB = json.dumps(file['data'])
    fDB = open(user_data['Argument'], 'w')
    fDB.write(strDB)
    fDB.close()

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass

## references:
#http://www.pythonforbeginners.com/os/python-the-shutil-module
#
