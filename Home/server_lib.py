import numpy as np
import pLukas as pl
import sys
from os import walk
from os import listdir
from os import chdir
import json

def service():
    file = pl.receiveFile()
    status = login(file['name'],file['password'])
    ip,port = pl.IP()
    file = pl.message([None,None,ip,port,None,None,status,None])
    pl.sendFile(file)
    if status:
        while file['command']=='exit':
            file = pl.receiveFile()
            
def login(name, password):
    foundDB, db = DB()
    status = verify(db,user,password)
    if status != 1:
        print "Registering User. Login done! Trying connection..."
        saveDB({"User name": user, "Password": password})
        status = 1
    return status

def DB():
    tree = listdir('Home')
    found  = 0
    for i in xrange(len(tree)):
        if(tree[i] == "dbFile.json"):
            found = 1
            bd = loadDB()
    if(not found):
        bd = createDB()
    return found,bd

def createDB():
    obj = []
    strDB = json.dumps(obj)
    fDB = open("dbFile.json", 'w')
    fDB.write(strDB)
    fDB.close()

def saveDB(profile):
    db = []
    found, database = DB()
    db = database
    with open('dbFile.json','w') as outfile:
        db.append(profile)
        outfile.write(json.dumps(db,indent = True))

def loadDB():
    with open('dbFile.json','r') as infile:
        data = json.loads(infile.read())
    return data

def tree():
    tree = listdir('Home')
    found  = 0
    for i in xrange(len(tree)):
        if(tree[i] == "treeFile.json"):
            found = 1
            bd = loadTreeFile()
    if(not found):
        bd = createDB()
    return found,bd

#def treeFile():
def verify(db,user,password):
    status = -1
    for i in xrange(len(db)):
        if db[i]['User name'] == user and db[i]['Password'] == password:
            print "Login successfull. Trying conection..."
            status = 1
        elif db[i]['User name'] == user and db[i]['Password'] != password:
            print "Bad Argument."
            status = -1
    if [pos for pos, char in enumerate(db['User name']) if char == user] == -1:
        saveDB({'User name': user, 'Password': password})
        status = 1
    return status
#### File Manipulation
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
    dir_path = ""
    if arg[0] == '..':
        dirpath = getcwd()
        print dirpath
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

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass
