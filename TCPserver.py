#This will be for netwroking and for multiple clients 
import socket 
import threading
import os 
from datetime import datetime

#This is the change the color of text to the console
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[95m {}\033[00m]"
RESET = "\033[0m"  # Resets all formatting

MAX_CLIENTS: int = 3 #max number of clients  
clients: dict[str, tuple[socket.socket, int]] = dict()#list of all the clients -> [name: (socket,int) ]
cache: dict[str, tuple[str, str]] = dict()#list of all the date and times people have come and gone -> [client name: (time-in, time-out)] 
PATH: str = r"C:\Users\Giuseppe\School\3rd year Fall\cp372\programming assignment\src\repo"#gets the current working directory 

'''
takes one parameter client which a name of the client 
This function is used when a client sends a message and recieving a message. 
data will hold the message being recieved 
'''
def clientHandler(name: str) -> None:
    #this will hold the socket related to the clients name   
    s = clients[name][0]
    while True:
        #check if the clint sends: 
        # 'exit' which closes the connection 
        # 'status' which lists the content in the cache 
        # 'list' 
        
        # data is the value the client sends 
        data = s.recv(1024).decode() 
        #printing out the data the client has just sent 
        print(f"{name}: {data}")
        #s.send(f"{name}: {data}AWK".encode())
        #make sure there was data sent 
        if data:
            message = f""
            #so the client would like to stream a file in the repo directory 
            if clients[name][1] == 1: 
                try: #check if the path exists
                    fullpath = os.path.join(PATH, data) #get the path to the repo 
                    if os.path.exists(fullpath):#make sure the path exists 
                        
                        #print(f"{name} would like to stream the files in the repo: {PATH}, {data}")
                        #message += f"{name}, i will stream to you {PATH}\n"
                        with open(fullpath, "rb") as f:
                            while True:
                                chunck = f.read(1024)
                                if not chunck: 
                                    break 
                                else:
                                    s.send(chunck)
                    else:
                        message += f"{RED}{name} the directory files are not available{RESET}"
                        print(f"{RED}{name}, the file/directory does not exist{RESET}")
                except: #catch an error probably a does not exist error 
                    message += f"{RED}{name} an error has occured{RESET}"
                    print(f"{RED}{name}, an error has occured{RESET}")
                clients[name] = (s, 0) 
            #if the message is exit then the client should leave and kill the connection 
            elif data == "exit":#this is good 
                #delete clients name from the dictionary 
                del clients[name]
                #print on the server the client has left 
                print(f"{RED}{name} have left!{RESET}")
                #close the connection
                s.close()
                #Here we will keep the time the client joined, get the current time (time they have left) and place it in the cache 
                joined = cache[name][0] 
                now = datetime.now()
                format_date = now.strftime("%Y-%m-%d %H:%M:%S")
                cache[name] = (joined, format_date)
                #print out the cache at the client who has just left 
                print(f"{GREEN}{name}: {cache[name]}{RESET}")
                break
            #if the message is status then we should print out the cache and send it to the client who has requested it 
            elif data == "status": #this is works
                #hold the message in a string 
                #go through all the items in the dictionary -> cache = {name: (enter time, leave time)}
                #key = name 
                #value = (enter time, leave time)
                for key, value in cache.items(): 
                    string = f"client: {key} entered: {value[0]} and exited: {value[1]}\n"
                    message += string
                #now send the message and encode it 
            #if the client enters list, then we must send all of the files in the directory
            elif data == "list": 
                #try to list all of the files in the specified path 
                try: 
                    #files will hold all of the files in the cwd 
                    files = os.listdir(PATH)
                    if files: #if the files are available 
                        print(f"{name} would like to see the files in: {files} and they are available")
                        message += f"Available files:\n ".join(files)
                    else:#they not not available
                        message += f"no files in the repo"
                #catch any FileNotFoundError
                except FileNotFoundError:
                    message += f"file not found"
                clients[name] = (s, 1)

            else:
                # send back 
                message += f"{name}: {data}AWK"
            #message += f"\n" 
            s.send(message.encode())

'''
take one parameter s which is the serverSocket
This function is used for alistening for new clients who want to join the
conversation 
'''
def listening(s: socket) -> None:
    while True:    
        #this waits for new clients to join (max of three) 
        client_socket, address = s.accept()
        #prints the address from where the client joined from 
        print(f"{BLUE}connection from: {str(address)}{RESET}")
        #This gets the name of the client which is the first thing the new client sends 
        name = client_socket.recv(1024).decode().strip()
        client_socket.send(f"{GREEN}Welcome {name}{RESET}\n".encode())
        print(f"{GREEN}{name} has joined the conversation{RESET}")
        #this puts the client name, socket and value of is the client wants a file in a dictionary: {name: (socket, int),}
        clients[name] = (client_socket, 0)
        #gets the current date and time, formats the date and time then places it in cache: cache = {name: (enter time, exit time)}
        now = datetime.now()
        format_date = now.strftime("%Y-%m-%d %H:%M:%S")
        cache[name] = (format_date, 'is still present')
        #here we start the thread for the client and the client handler will be the threaded function which deals with sending and 
        #recieving messages
        thread = threading.Thread(target=clientHandler, args=(name,))
        thread.start()

'''
This function is the main server function which initializzes the 
socket... 
'''
def start_server() -> None: 
    #create a new socket given address and protocol number 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('localhost', 12345))
    serverSocket.listen(MAX_CLIENTS) 
    print(f"-"*50)
    print(f"{YELLOW}Server is listening...{RESET}") 

    listening(serverSocket)

    return None

if __name__ == '__main__':
    start_server()