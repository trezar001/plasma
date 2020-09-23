import socket
import threading
import sys
import modules
import connection
from colorama import Fore, init

if sys.platform == 'win32' or sys.platform == 'win62':
    init(convert=True)
ismodule = False

def plasma():
    global ismodule

    while True:
        print(Fore.LIGHTCYAN_EX + 'plasma> ' + Fore.RESET, end='')
        cmd = input()

        for module in modules.get_modules():
            if cmd.split(' ')[0] == module.cmdstring:
                module.execute(cmd)
                ismodule = True
                break

        if not ismodule:
            if cmd == 'help':
                show_help()

            elif cmd == 'quit' or cmd == 'exit':
                exit_program()

            else:
                print(Fore.LIGHTRED_EX + '[!] Invalid command. Enter \'help\' to see a list of available commands' + Fore.RESET)
        
        ismodule = False
             
def exit_program():
    for i,conn in enumerate(connection.connections):
        if conn is not None:
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

    for s in modules.listen.sockets:
        s.close()

    sys.exit(0)

def show_help():
    print(Fore.LIGHTCYAN_EX + '\n-------- Commands --------' + Fore.RESET)
    for module in modules.get_modules():
        if module.cmdstring != 'sample':
            print(Fore.LIGHTYELLOW_EX + module.cmdstring + Fore.RESET + ':\t ' + module.description)
    print(Fore.LIGHTYELLOW_EX + 'exit' + Fore.RESET + ':\t close all connections and exit program')  
    print(Fore.LIGHTCYAN_EX + '--------------------------\n' + Fore.RESET)
    
plasma()
