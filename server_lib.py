import numpy as np
#import plukas as p
import sys
from os import walk
from os import listdir
import json

def listServer(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass
