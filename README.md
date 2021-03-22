# plasma
A command line interface for managing shells on multiple clients. Plasma is made up of two main components: a server and a client. The plasma server can be started through server.py and the client through client.py, although any other method of sending a reverse shell can be substituted for client.py. In addition to being able to seamlessly capture and swap between multiple clients, plasma contains a library of built in commands that can be executed while interacting with a client shell. Pre-compiled binaries can be found for plasma but I do not currently recommend using them as they are out of date and not properly tested.

## server.py
The plasma server can be started with the following command.
```
python server.py
```
Once inside, you'll be greeted with a prompt. To list available commands inside the program type in the command 'help' and press enter. Typing in the name of one of the command modules will display information on their usage. An example of capturing a connection from our local machine can be found below. Note that this process will also work for connections made from remote machines.

### Example
We start first start up the program.
```
python server.py
```
![plasma](https://user-images.githubusercontent.com/10237135/111933464-ea43bc80-8a95-11eb-93b1-939f13af7647.PNG)</br></br>
We use the 'listener' command module to start a listener on port 4444.
```
plasma> listener add 4444
```
![listener](https://user-images.githubusercontent.com/10237135/111933512-034c6d80-8a96-11eb-8213-ba5bc97c0458.PNG)</br></br>
In this case, we'll use client.py on the local machine to connect back to our server on the port we opened previously. Usage of client.py can be found later in this document.</br>
![111932248-6ab4ee00-8a93-11eb-89e9-6c252ce5c470](https://user-images.githubusercontent.com/10237135/111933770-879ef080-8a96-11eb-95c6-d949b7ac814e.png)</br></br>
With the 'list' command module, we can view the connected clients. Here we can see the connection we just established being listed.
```
plasma> list
```
![conn2](https://user-images.githubusercontent.com/10237135/111932254-6e487500-8a93-11eb-9ade-6cc3413d1618.PNG)</br></br>
To interact with the client, we use the 'select' command module and specify the client we would like to interact with. Upon running this command we are greeted with a command prompt.
```
plasma> select 1
```
![inter](https://user-images.githubusercontent.com/10237135/111932267-73a5bf80-8a93-11eb-88bf-dd94a9aeb09d.PNG)</br></br>
Here, running the in-shell module 'p-help' displays a help message. Running 'p-list' would display a list of all the plasma commands available to us.
```
C:\Users\treza\Desktop\Code\github\plasma> p-help
```
![help](https://user-images.githubusercontent.com/10237135/111933546-152e1080-8a96-11eb-8185-d0f8c9cd9013.PNG)</br>

## client.py
This is a custom client with some added functionality, although it is not necessary to use plasma. Plasma can recieve connections from any normal methods of sending shells including that from netcat, powershell, etc. This client has the added feature of being able to automatically attempt to restore connection with the server if the connection is lost.
```
usage: client.py [-h] -s  -p  [-r] [--max-retries]

optional arguments:
  -h, --help      show this help message and exit
  -s , --server   server to connect to
  -p , --port     port to connect to
  -r , --retry    set time between each retry if a connection is lost
  --max-retries   set max number of times to retry forming a connection before exiting
```

## Installation
Navigate to directory of choice and download the neccessary files with the following command.
```
git clone https://github.com/trezar001/plasma.git
```
Use pip to install any missing dependencies.
```
pip install -r requirements.txt
