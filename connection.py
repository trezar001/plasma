import socket
import time
import sys
import shell_modules
from colorama import Fore, init

#make sure colors work properly in Windows
if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)
    
ismodule = False
isColor = False

connections = []
addresses = []
hostnames = []


#send custom commands. A normal shell can't do this! ;)
def send_commands(conn, index):
    global ismodule
    global isColor

    #print nicely on new line and prepare for cmd
    conn.send(str.encode('\n'))
    print(recieve_immediately(conn),end='')

    while(True):
        try:
            cmd = input()
            
            for module in shell_modules.get_modules():
                if cmd.split(' ')[0] == module.cmdstring:
                    module.execute(cmd, conn, isColor)
                    ismodule = True
                    break

            #normal stuff
            if not ismodule:
                if cmd == 'p-quit' or cmd == 'p-exit':
                    print(Fore.LIGHTYELLOW_EX + '[+] Ending interaction with ' + str(addresses[index][0]) + Fore.RESET)
                    break
                elif cmd == 'p-help':
                    print(Fore.LIGHTCYAN_EX + '<----------------PLASMA HELP-----------------> ' + Fore.RESET)
                    print(Fore.LIGHTYELLOW_EX + 'Use \'p-exit\' to end interaction with client' + Fore.RESET)
                    print(Fore.LIGHTYELLOW_EX + 'Use \'p-list\' to view available plasma commands ' + Fore.RESET)
                    print(Fore.LIGHTYELLOW_EX + 'Use \'p-color\' to toggle colored text mode\n' + Fore.RESET)
                    print(Fore.LIGHTYELLOW_EX + 'p-color -> ', end='')
                    if isColor:
                        print(Fore.LIGHTGREEN_EX + str(isColor) + '\n' + Fore.RESET)
                    else:
                        print(Fore.LIGHTRED_EX + str(isColor) + '\n' + Fore.RESET)

                    conn.send(str.encode('\n'))
                    if isColor:
                        print(Fore.LIGHTCYAN_EX + recieve(conn) + Fore.RESET, end='')
                    else:
                        print(recieve(conn), end='')

                elif cmd == 'p-color':
                    isColor = not isColor
                    conn.send(str.encode('\n'))
                    if isColor:
                        print(Fore.LIGHTCYAN_EX + recieve(conn) + Fore.RESET, end='')
                    else:
                        print(recieve(conn), end='')

                elif cmd == 'p-list':
                    print(Fore.LIGHTCYAN_EX + '<---------------PLASMA MODULES---------------> ' + Fore.RESET)
                    for module in shell_modules.get_modules(): 
                        print(Fore.LIGHTYELLOW_EX + module.cmdstring + ': ' + module.description + Fore.RESET)

                    print()
                    conn.send(str.encode('\n'))
                    if isColor:
                        print(Fore.LIGHTCYAN_EX + recieve(conn) + Fore.RESET, end='')
                    else:
                        print(recieve(conn), end='')

                elif cmd == '':
                    conn.send(str.encode('\n'))
                    if isColor:
                        print(Fore.LIGHTCYAN_EX + recieve(conn) + Fore.RESET, end='')
                    else:
                        print(recieve(conn), end='')             
 
                elif len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd + '\n'))
                    if isColor:
                        text = recieve_separate(conn)
                        text[0] = text[0].replace('\r', '\n')
                        print(Fore.LIGHTMAGENTA_EX + text[0] + Fore.RESET)
                        print(Fore.LIGHTCYAN_EX + text[1] + Fore.RESET, end='')
                    else:
                        print(recieve(conn), end='')

            ismodule = False

            #handle random breakdown in connection
        except:
            conn.send(str.encode('exit\n')) 
            conn.close()              
            del connections[index]
            del addresses[index]
            del hostnames[index]
            print(Fore.LIGHTRED_EX + '[!] Connection was lost!' + error + Fore.RESET)
            break

#get responses
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

        #get the data
        else:
            try:
                data = conn.recv(1024)
                begin = time.time()
                res += data.decode('utf-8')
            except:
                pass

    return res

#get responses but separate prompt from text for potential to color
def recieve_separate(conn, timeout=0.1):
    res = ''
    begin=time.time()

    while True:
        if (len(res) > 0) and (time.time()-begin) > timeout:
            break

        #wait up to five seconds for a command 
        elif time.time()-begin > timeout * 50:
            print(Fore.LIGHTRED_EX + '[!] Command appears to be frozen. Wait and press enter if you think the command should still go through otherwise try reopening a new connection.' + error + Fore.RESET)
            break

        #get the data
        else:
            try:
                data = conn.recv(1024)
                begin = time.time()
                res += data.decode('utf-8')
            except:
                pass
    test = res.split('\n')
    new = [''.join(test[:-1]), test[-1]]
    res = new
    return res

#special case, get data immediately no waiting
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
