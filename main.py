#!/usr/bin/env python
# coding=utf-8
import numpy as np
import client_lib as cl
import server_lib as ser
import os
import sys

def login(status,strikes):
    choise = str(raw_input("Press 'l' to Login or 's' to Sign in.\n"))
    if choise == 'l' or choise == 'L':
        foundDB, db = ser.DB()
        user = str(raw_input("User name:"))
        password = str(raw_input("Password:"))
        for i in xrange(len(db)):
            if db[i]['User name'] == user and db[i]['Password'] == password:
                print "Login successfull. Trying conection..."
                status = 1
        if status != 1:
            print "Registering User. Login done! Trying connection..."
            ser.saveDB({"User name": user, "Password": password})
            status = 1
    elif choise == 's' or choise == 'S':
        user = str(raw_input("Set users name:"))
        password = str(raw_input("Set password:"))
        ser.saveDB({"User name": user, "Password": password})
        status = 1
    else:
        if strikes < 2:
            print("Invalid input. Please enter valid ones..\n")
        status = -1
        strikes+=1
    return status,strikes

def listCommand():
    print "\n\nCommand List:\n\n"
    print "checkdir -> List folders and files in the current directory."
    print "cd path_to_dir -> Acess directory 'path_to_dir'."
    print "mv file dest_dir -> Move 'file' to 'dest_dir'."
    print "rm file -> Remove 'file'."
    print "makedir dirname -> Creates 'dirname' directory."
    print "upload path_to_file -> Upload file in 'path_to_file' directory to server."
    print "download file -> Download 'file' to local."
    c = raw_input('Set command: ')
    if c == 'checkdir':
        arg = None
    else:
        c, arg = c.split(' ')
    print c
    return c,arg

def main(*args):
    os.system('cls' if os.name == 'nt' else 'clear')
    print "################################################################"
    print "                     DropBox service                            "
    print "                       python 2.7                               "
    print "################################################################"
    print "\n\n"
    status = -1
    strikes = 0
    while(status!=1):
        status,strikes = login(status,strikes)
        if(strikes == 3):
            print "Wrong input."
            exit()
    #cl.conection()
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Welcome!"
    while(status):
        command = raw_input("Enter the 'help' command to see all options: ")
        if command == 'help':
            command , arg = listCommand()
        #elif command = 'list tree'
        #    cl.listLocalTree(arg)
        if command == 'checkdir':
            cl.checkDir()
main(sys.argv)
