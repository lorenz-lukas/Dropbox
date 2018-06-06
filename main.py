#!/usr/bin/env python
# coding=utf-8
import numpy as np
import client_lib as cl
import server_lib as ser
import os

def login(status,strikes):
    choise = str(raw_input("Press 'l' to Log in or 's' to Sign in.\n"))
    if choise == 'l' or choise == 'L':
        foundDB, db = cl.DB()
        user = str(raw_input("User name:"))
        password = str(raw_input("Password:"))
        for i in xrange(len(db)):
            if db[i]['User name'] == user and db[i]['Password'] == password:
                print "Log in successfull. Trying conection..."
                status = 1
        if status != 1:
            cl.saveDB({"User name": user, "Password": password})
            status = 1
    elif choise == 's' or choise == 'S':
        user = str(raw_input("Set users name:"))
        password = str(raw_input("Set password:"))
        cl.saveDB({"User name": user, "Password": password})
        status = 1
    else:
        if strikes < 2:
            print("Invalid input. Please enter valid ones..\n")
        status = -1
        strikes+=1
    return status,strikes

def main():
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
    #ser.conection()
    print "----------------------------------------------------------------"
    print "            Choose one of the options bellow                    "
    print "       (1) Add files from server                                "
    print "       (2) Remove files from server                             "
    print "       (3) Update local repository                              "
    print "----------------------------------------------------------------"
    print "\n\n"
    item = raw_input("")
    print item

main()
