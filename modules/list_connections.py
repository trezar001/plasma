from colorama import Fore, init
import connection
import sys

if sys.platform == 'win32' or sys.platform == 'win62':
    init(convert=True)

description = 'list available connections'
cmdstring = 'list'
args = ''

def execute(cmd):
    cmd = cmdstring
    if parse(cmd):
        try: 
            command()
            #print_notification()
        except Exception as e:
            print_error(e)

def command():
    results = ''
    for i, conn in enumerate(connection.connections):
        try:
            conn.send(str.encode('\n'))
            connection.recieve_immediately(conn)
        except:
            del connection.connections[i]
            del connection.addresses[i]
            del connection.hostnames[i]
            
    for i, conn in enumerate(connection.connections):
        try:
            results += Fore.LIGHTYELLOW_EX + str(i+1) + '. ' + Fore.RESET + connection.hostnames[i] + ' (' + str(connection.addresses[i][0]) + ':' + str(connection.addresses[i][1]) + ')\n'
            
        except Exception as e:
            print_error(e)
            print_error('Something weird happened. Try again!')


    print(Fore.LIGHTCYAN_EX + '\n-------- Clients --------\n' + Fore.RESET + results, end='')
    print(Fore.LIGHTCYAN_EX + '-------------------------\n' + Fore.RESET)

def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

def parse(cmd):
    return True
