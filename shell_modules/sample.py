from colorama import Fore, init
import argparse
import sys
import connection

#make sure colors work properly in Windows
if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)
    isWindows = True
else:
    isWindows = False


args = ''
description = 'a sample program'

#this is what's used to actually call the module in server.py
cmdstring = 'p-sample'

#run module
def execute(cmd, conn, isColor):
    cmd = cmd.split(cmdstring)[1].lstrip().split()
    if parse(cmd, conn):
        try: 
            command(conn, isColor)
        except Exception as e:
            print(e)
            print_error('bad command')

#what happens when module is run
def command(conn, isColor):
    command = args.test

    #show command if user wants to see
    if args.show:
        print_notification(command)

    conn.send(str.encode(args.test + '\n'))

    if isColor:
        text = connection.recieve_separate(conn)
        text[0] = text[0].replace('\r', '\n')
        print(Fore.LIGHTMAGENTA_EX + text[0] + Fore.RESET)
        print(Fore.LIGHTCYAN_EX + text[1] + Fore.RESET, end='')
    else:
        print(connection.recieve(conn), end='')

    conn.send(str.encode('\n'))

#just some color coding 
def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

#handle argument parsing for the module
def parse(cmd, conn):
    global args
    global description

    try:
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument(dest='test', type=str, help='test argument')
        parser.add_argument('-s', '--show', action='store_true', help='show command(s) being run')

        if len(cmd) == 0:
            parser.print_help()
            print()
            return False

        args = parser.parse_args(cmd)
        return True
    except:
        conn.send(str.encode('\n'))
        print(connection.recieve(conn), end='')
        return False
