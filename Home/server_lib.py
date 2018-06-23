# coding=utf-8
import pLukas as pl
from os import walk
from os import listdir
from os import path
from os import remove
from os import makedirs
from os import chdir
from os import getcwd
import json
import errno
import sys

def login(user, password):
    foundDB, db = DB()
    status = verify(db,user,password)
    if status != 1:
        print "Registering User. Login done!"
        saveDB({"User name": user, "Password": password})
        status = 1
    return status

def verify(db,user,password):
    # Verify if user is in db
    status = -1
    for i in xrange(len(db)):
        if db[i]['User name'] == user and db[i]['Password'] == password:
            print "Login successful."
            status = 1
        elif db[i]['User name'] == user and db[i]['Password'] != password and status == -1:
            print "Bad Argument. Wrong password."
            status = 0
    #if [pos for pos, char in enumerate(db['User name']) if char == user] == -1:
    if status == -1:
        saveDB({'User name': user, 'Password': password})
        status = 1
    return status

def DB():
    tree = listdir('.')
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

#def tree():
#    tree = listdir('Home')
#    found  = 0
#    for i in xrange(len(tree)):
#        if(tree[i] == "treeFile.json"):
#            found = 1
#            bd = loadTreeFile()
#    if(not found):
#        bd = createDB()
#    return found,bd

def checkServer():
    # Check if is the first time that server is initialize and create first Dirs.
    if listdir('.') == []:
        mkDir('Home')
        goToDir('Home')
        mkDir('SharedFolder') #Creates Shared folder inside Home
        print 'Server created'
    #print listdir('.')
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
    if arg == '..':
        dirpath = getcwd()
        print dirpath
    print arg
    chdir(arg) #path


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
        makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST: # and path.isdir(path)
            print "Directory already exist!\n"
        else:
            print "Invalid Argument.\n"

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass
