import connection
import argparse
import sys
from colorama import Fore, init

#make sure colors work properly in Windows
if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)

args = ''
description = 'select client to interact with'

#this is what's used to actually call the module in server.py
cmdstring = 'select'

#run module
def execute(cmd):
    cmd = cmd.split(cmdstring)[1].lstrip().split()
    if parse(cmd):
        try: 
            command()
            #print_notification()
        except Exception as e:
            print_error(e)
            print_error('There is no client connected with that id!')

#what happens when module is run
def command():
    #interact with a hooked client so we can send commands to it
    conn = connection.connections[args.number-1]
    print(Fore.LIGHTYELLOW_EX + '[+] Interacting with ' + str(connection.addresses[args.number-1][0]) + '. For help use the command \'p-help\'.' + Fore.RESET)
    connection.send_commands(conn, args.number-1)

#just some color coding 
def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

#handle argument parsing for the module
def parse(cmd):
    global args
    global description
    
    try:
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument(dest='number', type=int, help='number of client to interact with')

        if len(cmd) == 0:
            parser.print_help()
            print()
            return False

        args = parser.parse_args(cmd)
        return True
    except:
        print()
        return False

   
