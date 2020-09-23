from colorama import Fore, init
import argparse
import sys
import connection

if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)

args = ''
description = 'kill connection to a client'
cmdstring = 'kill'

def execute(cmd):
    cmd = cmd.split(cmdstring)[1].lstrip().split()
    if parse(cmd):
        try: 
            command()
        except:
            pass

def command():
    if(args.action == 'killall'):
        if len(connection.connections) == 0:
            print_error('There are no connections to close!')
        else:
            for i,conn in enumerate(connection.connections):
                try:
                    conn.send(str.encode('exit\n'))               
                    conn.close()
                    del connection.connections[i]
                    del connection.addresses[i]
                    del connection.hostnames[i]

                except:
                    del connection.connections[i]
                    del connection.addresses[i]
                    del connection.hostnames[i]

            print_notification('Successfully closed all connections')


    elif(args.action == 'killone'):
        if args.id-1 in range(0, len(connection.connections)):
            connection.connections[args.id-1].send(str.encode('exit\n')) 
            connection.connections[args.id-1].close()              
            del connection.connections[args.id-1]
            del connection.addresses[args.id-1]
            del connection.hostnames[args.id-1]
            print_notification('Successfully closed connection to client ' + str(args.id))
        else:
            print_error('client with id ' + str(args.id) + ' could not be found!')


def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

def parse(cmd):
    global args

    try:
        parser = argparse.ArgumentParser()
        
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-a', '--all', dest='action', action='store_const',const='killall', help='kill all clients')
        group.add_argument('-c', '--client', dest='id', metavar='id', type=int, help='kill client with id')
        group.set_defaults(action='killone')

        if len(cmd) == 0:
            parser.print_help()
            print()
            return False

        try:
            args = parser.parse_args(cmd)
            return True
        except:
            return False
        
    except Exception as e:
        print(e)
        return False
