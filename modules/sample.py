from colorama import Fore, init
import argparse
import sys


if sys.platform == 'win32' or sys.platform == 'win62':
    init(convert=True)

args = ''
description = 'a sample program'
cmdstring = 'sample'

def execute(cmd):
    cmd = cmd.split(cmdstring)[1].lstrip().split()
    if parse(cmd):
        try: 
            command()
            print_notification('I did something!')
        except:
            print_error('bad command')

def command():
    print('haha')

def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

def parse(cmd):
    global args
    
    try:
        parser = argparse.ArgumentParser(usage='test usage')

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
