from colorama import Fore, init
import connection
import sys

#make sure colors work properly in Windows
if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)

args = ''
description = 'list available connections'

#this is what's used to actually call the module in server.py
cmdstring = 'list'


#run module
def execute(cmd):
    cmd = cmdstring
    if parse(cmd):
        try: 
            command()
            #print_notification()
        except Exception as e:
            print_error(e)

#what happens when module is run
def command():
    results = ''
    for i, conn in enumerate(connection.connections):

        #send newline to test if client if still alive
        try:
            conn.send(str.encode('\n'))
            connection.recieve_immediately(conn)

        #client is dead, delete any leftovers
        except:
            del connection.connections[i]
            del connection.addresses[i]
            del connection.hostnames[i]

    #get info on clients      
    for i, conn in enumerate(connection.connections):
        try:
            results += Fore.LIGHTYELLOW_EX + str(i+1) + '. ' + Fore.RESET + connection.hostnames[i] + ' (' + str(connection.addresses[i][0]) + ':' + str(connection.addresses[i][1]) + ')\n'

        #this is a weird one :/    
        except Exception as e:
            print_error(e)
            print_error('Something weird happened. Try again!')

    #print clients in pretty format
    print(Fore.LIGHTCYAN_EX + '\n-------- Clients --------\n' + Fore.RESET + results, end='')
    print(Fore.LIGHTCYAN_EX + '-------------------------\n' + Fore.RESET)

#just some color coding 
def print_error(error):
    print(Fore.LIGHTRED_EX + '[!] ' + error + Fore.RESET)

def print_notification(notification):
    print(Fore.LIGHTYELLOW_EX + '[+] ' + notification + Fore.RESET)

#handle argument parsing for the module
def parse(cmd):
    return True
