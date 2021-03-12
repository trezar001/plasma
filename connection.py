import socket
import time
import sys
import shell_modules
from colorama import Fore, init

#make sure colors work properly in Windows
if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)
else:
    import readline
    
ismodule = False
isColor = False
cmd = ''

connections = []
addresses = []
hostnames = []


#send custom commands. A normal shell can't do this! ;)
def send_commands(conn, index):
    global ismodule
    global isColor
    global cmd

    #print nicely on new line and prepare for cmd
    conn.send(str.encode('\n'))
    prompt = recieve_immediately(conn)
    if sys.platform == 'win32' or sys.platform == 'win64':
        if isColor:
            print(Fore.LIGHTCYAN_EX + prompt + Fore.RESET, end='')
            cmd = input()
        else:
            print(prompt, end='')
            cmd = input()
    else:
        if isColor:
            cmd = input(Fore.LIGHTCYAN_EX + prompt + Fore.RESET)
        else:
            cmd = input(prompt)

    while(True):
        try:
                 
            for module in shell_modules.get_modules():
                if cmd.split(' ')[0] == module.cmdstring:
                    newprompt = module.execute(cmd, conn, isColor)

                    if isColor:
                        if sys.platform == 'win32' or sys.platform == 'win64':
                            print(Fore.LIGHTCYAN_EX + newprompt + Fore.RESET, end='')
                            cmd = input()
                        else:
                            cmd = input(Fore.LIGHTCYAN_EX + newprompt + Fore.RESET)
                    else:
                        cmd = input(newprompt)

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
                        print(Fore.LIGHTGREEN_EX + str(isColor) + Fore.RESET)
                    else:
                        print(Fore.LIGHTRED_EX + str(isColor) + Fore.RESET)

                    conn.send(str.encode('\n'))
                    text = recieve(conn)
                    text[0] = text[0].replace('\r', '\n')
                    if isColor:
                        print(Fore.LIGHTMAGENTA_EX + text[0] + Fore.RESET)
                        if sys.platform == 'win32' or sys.platform == 'win64':
                            print(Fore.LIGHTCYAN_EX + text[1] + Fore.RESET, end='')
                            cmd = input()
                        else:
                            cmd = input(Fore.LIGHTCYAN_EX + text[1] + Fore.RESET)

                    else:
                        print(text[0])
                        cmd = input(text[1])

                elif cmd == 'p-color':
                    isColor = not isColor
                    consoleprint(conn)

                elif cmd == 'p-list':
                    print(Fore.LIGHTCYAN_EX + '<---------------PLASMA MODULES---------------> ' + Fore.RESET)
                    for module in shell_modules.get_modules(): 
                        print(Fore.LIGHTYELLOW_EX + module.cmdstring + ': ' + module.description + Fore.RESET)

                    consoleprint(conn)

                elif cmd == '':
                    consoleprint(conn)        
 
                elif len(str.encode(cmd)) > 0:
                    consoleprint(conn, cmd)

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

def consoleprint(conn, newcmd=''):
    global cmd 

    if newcmd != '':
        conn.send(str.encode(newcmd + '\n'))
    else:
        conn.send(str.encode('\n'))

    text = recieve(conn)
    text[0] = text[0].replace('\r', '\n')
    if isColor:
        print(Fore.LIGHTMAGENTA_EX + text[0] + Fore.RESET)
        if sys.platform == 'win32' or sys.platform == 'win64':
            print(Fore.LIGHTCYAN_EX + text[1] + Fore.RESET, end='')
            cmd = input()
        else:
            cmd = input(Fore.LIGHTCYAN_EX + text[1] + Fore.RESET)
    else:
        print(text[0])
        cmd = input(text[1])

#get responses but separate prompt from text for potential to color
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
    temp = res.split('\n')
    text = [''.join(temp[:-1]), temp[-1]]
    return text

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
