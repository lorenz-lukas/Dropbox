import numpy as np
import pLukas as p
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

#def listLocalTree(startpath):
#    for root, dirs, files in os.walk(startpath):
#        level = root.replace(startpath, '').count(os.sep)
#        indent = ' ' * 4 * (level)
#        print('{}{}/'.format(indent, os.path.basename(root)))
#        subindent = ' ' * 4 * (level + 1)
#        for f in files:
#            print('{}{}'.format(subindent, f))
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
    #dir_path = ""
    #if arg[0] == '..':
    #    dir = printDir()
    #    dir = dir.split('$')
    #    dir = dir[0]
    #    dir = dir.split('/')
    #    i = 1
    #    for i in xrange(len(dir)-1):
    #        dir_path += ('/'+dir[i])
    #    dir_path = dir_path.split('~')
    #    dir = dir_path[-1]
    #    print dir
    #    goToDir(dir)
    #else:
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

def moveSameTypeFile(extension,orig,dest):
    source = listdir(orig)
    for files in source:
        if files.endswith(extension):
            shutil.move(files,dest)

def copyTree(SOURCE,BACKUP):
    # create a backup directory
    shutil.copytree(SOURCE, BACKUP)
    print listdir(BACKUP)

def dellTree(dir):
    shutil.rmtree(dir)

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass

## references:
#http://www.pythonforbeginners.com/os/python-the-shutil-module
#
