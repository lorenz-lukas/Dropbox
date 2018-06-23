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
    status = -1
    if foundDB:
        status = verify(db,user,password)
    if status == -1:
        print "Registering User. Login done!"
        saveDB({"User name": user, "Password": password})
        status = 1
    return status

def verify(db,user,password):
    # Verify if user is in db
    status = -1
    print db
    if db != []:
        for i in xrange(len(db)):
            if db[i]['User name'] == user and db[i]['Password'] == password:
                print "Login successful."
                status = 1
            elif db[i]['User name'] == user and db[i]['Password'] != password:
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
    chdir('Home')
    obj = []
    strDB = json.dumps(obj)
    fDB = open("dbFile.json", 'w')
    fDB.write(strDB)
    fDB.close()
    return obj

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
    dir = listdir('.')
    found = 0
    for i in xrange(len(dir)):
        if dir[i] == 'Home':
            found = 1

    if not found:
        mkDir('Home')
        goToDir('Home')
        mkDir('SharedFolder') #Creates Shared folder inside Home
        print 'Server created'
    else:
        goToDir('Home')
    #print listdir('.')
#### File Manipulation
def checkDir(file,soc):
    dir = listdir('.')
    for i in dir:
        print i
    file['data'] = dir
    pl.sendFile(file,soc)

def removeFile(file,soc):
    deleted = 0
    root, dirs, files = walk('.').next()
    for i in files:
        if file['Argument'] == str(i):
            remove(file['Argument'])
            deleted = 1
    if not deleted:
        print("Error: %s file not found" % file['Argument'])
    notify = pl.message(None,None,None,None,None,None,deleted,None)
    pl.sendFile(notify,soc)

def moveFile(user_data,soc):
    args = user_data['Argument']
    file = args[0]
    dest = args[1]
    shutil.move(file,dest)

def goToDir(arg):
    #dir_path = ""
    #if arg == '..':
    #    dirpath = getcwd()
    #    print dirpath
    chdir(arg) #path
    #return arg
def mkDir(directory):
    try:
        makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST: # and path.isdir(path)
            print "User already registered!\n"
        else:
            print "Invalid Argument.\n"

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass
