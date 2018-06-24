#!/usr/bin/env python
# coding=utf-8
import server_lib as sr
import pLukas as pl
import os
import sys

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print "################################################################"
    print "                     DropBox service                            "
    print "                       python 2.7                               "
    print "                     Server Interface                           "
    print "################################################################"
    print "\n\n"
    pl.connectionServer()
    sys.exit()
main()
