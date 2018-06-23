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
    return int(file['data']),soc,message

def checkDir(soc,user_data):
    user_data['command'] = 'checkdir'
    pl.sendFile(user_data,soc)
    user_data = pl.receiveFile(soc)
    dir = user_data['data']
    for i in dir:
        print i

def removeFile(file_name,soc,user_data):
    user_data['command'] = 'rm'
    user_data['Argument'] = file_name
    pl.sendFile(user_data,soc)
    message = pl.receiveFile(soc)
    if message['data'] == 0:
        print("Error: %s file not found" % file)
    else:
        print("File %s removed successful" %file)

def moveFile(file_name,soc,user_data):
    user_data['command'] = 'mv'
    user_data['Argument'] = args
    pl.sendFile(user_data,soc)

def goToDir(arg):
    user_data['command'] = 'mv'
    user_data['Argument'] = args
    pl.sendFile(user_data,soc)

def printDir():
    dirpath = getcwd()
    string = dirpath.split('/')
    #print string
    pth = '~'
    for i in xrange(len(string)):
        if string[i] == 'Home':
            rel_path = string[i:len(string)]
            for i in rel_path:
                pth +=('/'+i)
    return (pth + '$' + ' Set command: ')

def mkDir(directory):
    try:
        makedirs(directory[0])
    except OSError as e:
        if e.errno != errno.EEXIST:
            print "Directory already exist!\n"
        else:
            print "Invalid Argument.\n"

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass

## references:
#http://www.pythonforbeginners.com/os/python-the-shutil-module
#
