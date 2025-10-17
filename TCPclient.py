import socket 
import threading

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[95m {}\033[00m]"
RESET = "\033[0m"  # Resets all formatting

'''
This function is responsible for sending messages 
'''
def send_message(s: socket.socket, name: str) -> None: 
    while True: #always look for a message 
        inp = input("") #ask for a message 
        s.send(inp.encode())#send a message 
        if inp == "exit": #the user closed the connection 
            print(f"{RED}closing connection...{RESET}") 
            s.close()#close the connection 
            break
        
    return None

'''
This function is responsible for recieving messages
'''
def recieve(s: socket.socket) -> None: 
    while True: #always look for a message that has been sent 
        try:
            message = s.recv(1024).decode()#hold the recieved message  
            if not message:#then the server closed he connection 
                print(f"{RED}server closed the connection{RESET}") 
                break
            #print the message 
            print(message)
        except: 
            break 
    s.close()#if is breaks then close the connection
    return None

def talk_server(s: socket.socket, name: str) -> None: 
    s.send(name.encode())#send the message which is the name
    thread = threading.Thread(target = recieve, args=(s, ))#make a thread for the client to recieve messages  
    thread.start()#start the thread 
    send_message(s , name) #start for sending messages 

    return None

def start_client() ->None:
    sock = socket.socket() #make the socket 
    sock.connect(('localhost', 12345))#connect to the server 

    name = input("Enter your name: ")#the first thing is the name 

    talk_server(sock, name)


    return None

if __name__ == '__main__':
    start_client()