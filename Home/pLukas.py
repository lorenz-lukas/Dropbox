import socket
from os import walk
from os import listdir
import json
import sys

def connectionServer(PORT):
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.bind(('0.0.0.0'),int(PORT))
    soc.listen(1)
    while(1):
        client = socket.accept() # Refsocket, ClientIP/PORT
        # Thread(client)
        # socket.close
    #soc.close() #Close connection
def connectionClient(PORT):
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.bind(('0.0.0.0'),int(PORT))
    soc.listen(1)
    # socket.close
    #soc.close() #Close connection

def IP():
    pass

### IP Loop-back - servidor local: 127.0.0.1
if __name__ == "__main__":
    sys.exit(main(sys.args))

def main(*args):
    pass
