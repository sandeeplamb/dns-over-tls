#!/usr/bin/env python3.6
import socket
import sys
import time
import sys
import os

######################################################################
### Global Variables
SERVER_ADDR = "/tmp/socket"
TOTAL_ARGUEMENT = len(sys.argv) - 1
DOMAIN_NAME = sys.argv[1]

######################################################################
### Module to call server socket
def call_server_socket():
    """
    Calls the server by sending the call to Server
    """
    try:
        CLIENT_SOCK = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            CLIENT_SOCK.connect(SERVER_ADDR)
        except ConnectionRefusedError as cre:
            print("Error connecting Server   : ", cre)
        #mess = "dig @localhost -p 53 " + DOMAIN_NAME
        CLIENT_SOCK.send(str.encode(DOMAIN_NAME))
        data = CLIENT_SOCK.recv(4096)
        print(data.decode("utf-8"))
        CLIENT_SOCK.close()
    except OSError as ose:
        print("Please see previous error : ", ose)


######################################################################
### Module to check script arguements
def check_client_arguements():
    """
    Check the total arguements Passed
    """
    if TOTAL_ARGUEMENT == 1:
        pass
    else:
        print("There is need of exacly one Arguement.")
        print("You sent : {} .".format(TOTAL_ARGUEMENT))
        sys.exit(0)

######################################################################
if __name__ == "__main__":
    check_client_arguements()
    print("Sending the command...")
    time.sleep(1)
    call_server_socket()
else:
    print("Connection failed. Exception traceback printed above.")