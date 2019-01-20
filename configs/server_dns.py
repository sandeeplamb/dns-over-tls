#!/usr/bin/env python3.6
import os
import sys
import socket
import time
import dns
import signal
import logging
from datetime import datetime
from dns import *
from subprocess import PIPE, run

######################################################################
### Global Variables
SOCKET_ADDR = "/tmp/socket"
HISTORY_LOGGER = logging.getLogger("save_history")
CURRENT_DIRECTORY = os.getcwd()
CURRENT_DIR_NAME = os.path.basename(CURRENT_DIRECTORY)
LOG_FILENAME = CURRENT_DIRECTORY + "/" + os.path.basename(__file__) + '-history.log'

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    #format="%(asctime)s %(name)23s %(levelname)7s %(message)s",
    format="%(asctime)s %(levelname)3s %(message)s",
    datefmt='%a, %d %b %Y %H:%M:%S'
    )

######################################################################
### History Modules
### Save History
def save_history(command_arg):
    """ Saves the History of the Channel. """
    HISTORY_LOGGER.info(command_arg)
    ##### DO NOT DELETE
    #with open(log_filename, 'a+') as outfile:
    #    now = datetime.now()
    #    time_stamp = now.strftime('%d, %b %Y %I:%M:%S')
    #    outfile.write(time_stamp + " : " + command_arg + "\n")
    ##### DO NOT DELETE
    return True

######################################################################
### Module to check script arguements
def get_output(command):
    """
    subprocsess sends back command output
    """
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout


######################################################################
### Module to check script arguements
def get_client_socket():
    try:
        SERVER_SOCK = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        SERVER_SOCK.bind(SOCKET_ADDR)
        SERVER_SOCK.listen(1)
    except OSError as ose:
        print("Socket '{}' : {} ".format(SOCKET_ADDR,ose))
        print("Clearing the socket and running it again.")
        time.sleep(1)
        if os.path.exists(SOCKET_ADDR):
            print("Socket : {} exists.".format(SOCKET_ADDR))
            os.system("rm -rf " + SOCKET_ADDR)
            get_client_socket()
        else:
            sys.exit(0)
    try:
        while True:
            RECVD, ARRGS = SERVER_SOCK.accept()

            msg = RECVD.recv(2048)
            DOMAIN_NAME = msg.decode("utf-8")
            save_history("Checking domain " + DOMAIN_NAME)
            print("Checking Domain : {}".format(DOMAIN_NAME))
            #ANSWERS = dns.resolver.query(DOMAIN_NAME, "A")
            #for rdata in ANSWERS:
            #    print("Domain A Record : {}".format(rdata.address))
            DNS_COMMAND = "dig @localhost " + DOMAIN_NAME
            save_history("Running command " + DNS_COMMAND)
            output = get_output(DNS_COMMAND)
            RECVD.send(str.encode(output))
            #os.system(DNS_COMMAND)
    except OSError as ose:
        print("Error : ", ose)
    
    RECVD.close()
    SERVER_SOCK.close()
    os.unlink(SOCKET_ADDR)

########################################################################
### Signal Handler
def signal_handler(signum, frame):
    """ Handles the Signals. """
    print("\n\n*****************************************")
    print("*****************************************")
    print('\nSignal handler called with signal : ' + str(signum))
    print('Because, you pressed Ctrl+C! \n')
    print("*****************************************")
    print("*****************************************\n\n")
    #save_history("Ctrl^C Pressed")
    sys.exit(0)

######################################################################
if __name__ == "__main__":
    print("Ready to receive commands...")
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(1)
    get_client_socket()
else:
    print("Connection failed. Exception traceback printed above.")
