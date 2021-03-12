from colorama import Fore, init
import argparse
import sys

#make sure colors work properly in Windows
if sys.platform == 'win32' or sys.platform == 'win62':
    init(convert=True)

args = ''
description = 'a sample program'

#this is what's used to actually call the module in server.py
cmdstring = 'sample'

#run module
def execute(cmd):
    cmd = cmd.split(cmdstring)[1].lstrip().split()
    if parse(cmd):
        try: 
            command()
            print_notification('I did something!')
        except:
            print_error('bad command')

#what happens when module is run
def command():
    print('haha')

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

        parser.add_argument(dest='test', type=str, help='test argument')

        if len(cmd) == 0:
            parser.print_help()
            print()
            return False

        args = parser.parse_args(cmd)
        return True
    except:
        print()
        return False
