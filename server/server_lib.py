# coding=utf-8
import pLukas as pl
from os import walk
from os import listdir
from os import path
from os import remove
from os import makedirs
from os import chdir
from os import getcwd
import shutil
import ast
import json
import errno
import sys
import zipfile

def checkServer():
    # Check if is the first time that server is initialize and create first Dirs.
    current_dir = listdir('.')
    dirpath = getcwd()
    dir = dirpath.split('/')
    found = 0
    root_path = 'Home'
    path = ''
    for i in current_dir: # Check if server is initialized
        if i == 'Home':
            found = 1
    for i in xrange(len(dir)): # Check if server is initialized before
        if dir[i] == 'Home':
            path = dir[0:i]
            found = 1
    if not found:
        root_path = ""
        for i in dir:
            root_path = root_path + i + '/'
        chdir(root_path)
        mkDir('Home')
        chdir(root_path+'Home')
        mkDir('SharedFolder') #Creates Shared folder inside Home
        print 'Server created'
    else:
        root = root_path
        root_path = ''
        for i in path:
            root_path = root_path + i + '/'
        root_path = root_path + root
        chdir(root_path)

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
    #print tree
    found  = 0
    for i in xrange(len(tree)):
        if(tree[i] == "dbFile.json"):
            found = 1
            bd = loadDB()
    if(not found):
        bd = createDB()
    return found,bd

def createDB():
    #chdir('Home')
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
        if i == file['Argument']:
            remove(file['Argument'])
            deleted = 1
    for i in dirs:
        if i == file['Argument']:
            shutil.rmtree(file['Argument'], ignore_errors=True)
            deleted = 1
    if not deleted:
        print("Error: %s file not found" % file['Argument'])
    notify = pl.message([None,None,None,None,None,None,deleted,None])
    pl.sendFile(notify,soc)

def moveFile(user_data,soc):
    args = user_data['Argument']
    #print args
    file = args[0]
    dest = args[1]
    shutil.move(file,dest)

def goToDir(file,soc):
    arg = file['Argument']
    dirpath = getcwd()
    dir = dirpath.split('/')
    if arg == '..':
        if dir[-2] == 'Home':
            print 'Changing to SharedFolder'
            chdir('..')
            chdir('SharedFolder')
            file['path'] = 'Home/SharedFolder'
        else:
            chdir(arg)
            del dir[-1]
            path = ''
            for i in xrange(len(dir)):
                if dir[i] == 'Home':
                    p = dir[i:len(dir)]
            for i in p:
                path += i + '/'
            file['path'] = path
    else:
        chdir(arg)
        file['path'] = file['path'] + '/' + arg
    pl.sendFile(file,soc)
    return file

def mkDir(directory):
    try:
        makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST: # and path.isdir(path)
            if directory == 'Home' or directory == 'SharedFolder':
                pass
            else:
                print "User already registered!\n"
        else:
            print "Invalid Argument.\n"

def exit(file,soc):
    online = 0
    notify = pl.message([None,None,None,None,None,None,'ok',None])
    pl.sendFile(notify,soc)
    print file['user']," exiting...", "\n\n"
    soc.close()
    return online

def upload(file,soc):
    print 'User: ',file['user']
    print 'Uploading file: ', file['Argument']
    with open(file['Argument']+'.zip', 'wb') as f:
        file_size = soc.recv(1024)
        file_size = int(file_size)
        rsize = 0
        soc.send("ok") # Handshake
        while True:
            print 'Uploading to server...'
            data = soc.recv(1024)
            rsize += len(data)
            f.write(data)
            if  rsize >= file_size:
                break
    # Unzip file
    print 'Upload done!'
    dirpath = getcwd()
    zip_ref = zipfile.ZipFile(dirpath+'/'+ file['Argument']+'.zip', 'r')
    zip_ref.extractall(dirpath)
    zip_ref.close()
    remove(file['Argument']+'.zip')

def download(file,soc):
    root, dirs, files = walk('.').next()
    found = 0
    file_count = 0
    try:
        makedirs('temp')
    except OSError as e:
        if e.errno == errno.EEXIST: # and path.isdir(path)
            pass
    shutil.move(file['Argument'],'temp')

    for i in files:
        if i == file['Argument']:
            file_count = 1
            found = 1

    for i in dirs:
        if i == file['Argument']:
            found = 1

    if found:
        dirpath = getcwd()
        shutil.make_archive(dirpath + '/' + file['Argument'], 'zip', 'temp')
        size = path.getsize(file['Argument'] + '.zip')
        soc.send(str(size))
        Handshake = soc.recv(2)
        if Handshake == 'ok': # if authorized to send then send
            with open(file['Argument'] + '.zip','rb') as f:
                data = f.read(1024)
                while data:
                    soc.send(data)
                    data = f.read(1024)
            print 'Download done!'
            remove(file['Argument']+'.zip')
            shutil.rmtree('temp', ignore_errors=True)
        else:
            print "Error to send file",file['Argument']," to Server."
    else:
        print("Error: %s file not found" % file)
        file['data'] = 'File not found'
        pl.sendFile(file,soc)

def getPath(file):
    dirpath = getcwd()
    dir = dirpath.split('/')
    p = ''
    for i in xrange(len(dir)):
        if dir[i] == 'Home':
            p = dir[0:i]
    dir = ''
    for i in p:
        dir+= i+'/'
    dir+= file['path']
    #print dir
    return dir

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass
