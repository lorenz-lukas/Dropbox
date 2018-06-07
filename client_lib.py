import numpy as np
import pLukas as p
import sys
from os import walk
from os import listdir
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
    print listdir('.')

    #print 


def moveDir(orig, dest):
    source = istdir(orig)
    for files in source:
        shutil.move(files,dest)

def moveSameTypeFile(extension,orig,dest):
    source = listdir(orig)
    for files in source:
        if files.endswith(extension):
            shutil.move(files,dest)
def moveFile(file,orig,dest):
        shutil.move(file,dest)

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
