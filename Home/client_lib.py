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
    return file['data']

def checkDir():
    dir = listdir('.')
    for i in dir:
        print i

def removeFile(file):
    #if path.isfile(file):
    deleted = 0
    root, dirs, files = walk('.').next()
    print files
    for i in files:
        if file == str(i):
            remove(file)
            deleted = 1
    if not deleted:
        print("Error: %s file not found" % file)

def moveFile(args):
    file = args[0]
    dest = args[1]
    #source = listdir(orig)
    #for files in source:
    shutil.move(file,dest)

def goToDir(arg):
    chdir(arg[0]) #path


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
