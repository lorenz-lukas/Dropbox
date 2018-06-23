#!/usr/bin/env python
# coding=utf-8
import client_lib as cl
#import server_lib as ser
import os
import sys

def login(status,ip,port,arg):
    if len(arg)>1:
            IP = arg[1]
            PORT = arg[2]
            user = arg[3]
            password = arg[4]
            status = cl.checkUserName(user, password,ip,port)
    else:
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
            print 'Wrong input.'
    return status

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
    print "                     Client interface                           "
    print "################################################################"
    print "\n\n"
    IP = "127.0.0.1"
    PORT = "1234"
    status = -1
    if len(sys.argv) > 1:
        status = login(status,IP,PORT,sys.argv)

    else:
        status = login(status,IP,PORT,sys.argv) ###
        print status
        if(status != 1):
            print "Wrong input."
            exit()
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Welcome!\nEnter 'help' to see all options."
    while(status):
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
