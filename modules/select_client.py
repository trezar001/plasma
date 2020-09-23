import connection
import argparse
import sys
from colorama import Fore, init

if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)

description = 'select client to interact with'
cmdstring = 'select'
args = ''

def execute(cmd):
    cmd = cmd.split(cmdstring)[1].lstrip().split()
    if parse(cmd):
        try: 
            command()
            #print_notification()
        except:
            print_error('There is no client connected with that id!')

def command():
    conn = connection.connections[args.number-1]
    print(Fore.LIGHTYELLOW_EX + '[+] Interacting with ' + str(connection.addresses[args.number-1][0]) + Fore.RESET)
    connection.send_commands(conn, args.number-1)

def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

def parse(cmd):
    global args

    try:
        parser = argparse.ArgumentParser(usage='select number')

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

   
