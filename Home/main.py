#!/usr/bin/env python
# coding=utf-8
from time import sleep
import client_lib as cl
#import server_lib as ser
import os
import sys

def login(status,strikes,ip,port):
    choise = str(raw_input("Press 'l' to Login or 's' to Sign in.\n"))
    if choise == 'l' or choise == 'L':
        user = str(raw_input("User name:" ))
        password = str(raw_input("Password:"))
        status = cl.checkUserName(user, password,ip,port)
    elif choise == 's' or choise == 'S':
        user = str(raw_input("Set users name:"))
        password = str(raw_input("Set password:"))
        status = cl.checkUserName(user,password,ip,port)
    else:
        if strikes < 2:
            print("Invalid input. Please enter valid ones..\n")
        status = -1
        strikes+=1
    return status,strikes

def listCommand():
    print "\n\nCommand List:\n\n"
    print "checkdir            -> List folders and files in the current directory."
    print "cd path_to_dir      -> Acess directory 'path_to_dir'."
    print "mv file dest_dir    -> Move 'file' to 'dest_dir'."
    print "rm file             -> Remove 'file'."
    print "makedir dirname     -> Creates 'dirname' directory."
    print "upload path_to_file -> Upload file in 'path_to_file' directory to server."
    print "download file       -> Download 'file' to local."
    print "exit                -> Logout.\n"

def exception(c):
    if c != 'help':
        if c == 'checkdir' or c == 'exit':
            arg = None
        elif [pos for pos, char in enumerate(c) if char == ' '] != []:
                array = c.split(' ')
                c = array[0]
                arg = array[1:len(array)]
        else:
            print 'Bad argument.\n'
            c = None
            arg = None
    else:
        arg = None
    return c,arg

def main(*args):
    os.system('cls' if os.name == 'nt' else 'clear')
    print "################################################################"
    print "                     DropBox service                            "
    print "                       python 2.7                               "
    print "################################################################"
    print "\n\n"
    IP = "127.0.0.0.1"
    PORT = "1234"
    if sys.argv != [] or len(sys.argv) != 2:
        IP = sys.argv[1]
        PORT = sys.argv[2]
        user = sys.argv[3]
        password = sys.argv[4]
        #foundDB, db = ser.DB()
        #status = ser.verify(db,user,password)
        sleep(1.5)
    else:
        status = -1
        strikes = 0
        while(status!=1):
            status,strikes = login(status,strikes,IP,PORT) ###
            if(strikes == 3):
                print "Wrong input."
                exit()
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Welcome!\nEnter 'help' to see all options."
    while(status):
        cl.conection(name,password)
        command = raw_input(cl.printDir())
        command, arg = exception(command)
        if command == 'help':
            listCommand()
        elif command == 'checkdir':
            cl.checkDir()
        elif command == 'rm':
            cl.removeFile(arg)
        elif command == 'mv':
            cl.moveFile(arg)
        elif command == 'cd':
            cl.goToDir(arg)
        elif command == "makedir":
            cl.mkDir(arg)
        else:
            print 'Bad Argument.\n'

main(sys.argv)
