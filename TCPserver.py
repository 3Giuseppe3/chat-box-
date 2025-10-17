#This will be for netwroking and for multiple clients 
import socket 
import threading
import datetime as dt

MAX_CLIENTS: int = 3 #max number of clients  
clients: dict[str, socket.socket] = dict()#list of all the clients -> [name: socket]
cache: list[tuple] = list(tuple())#list of all the date and times people have come and gone -> [(client name, time-in, time-out)]  

def sendMessage(sender, message) -> None:
    for name,sock in clients.items():
        if name != sender: 
            sock.send(message.encode())
        
    return None

'''
takes one parameter client which a tuple
which has the client name in the first spot and the 
client socket in the second spot 
'''
def clientHandler(name: str) -> None:  
    s = clients[name] 
    while True:
        #check if the clint sends: 
        # 'exit' which closes the connection 
        # 'status' which lists the content in the cache 
        # 'list' 

        data = s.recv(1024).decode() 
        if data: 
            if data == name + ": exit":
                clients.remove((name, s))
                break
            elif data == name + ": status": 
                pass
            elif data == name + ": list": 
                pass 
            else:#normal case but there may need a change do to 
                #part 11 of the assignment 
                sendMessage(name, data)
    return None 

'''
take one parameter s which is the serverSocket
'''
def listening(s: socket) -> None:
    while True:    
        client_socket, address = s.accept()
        print("connection from: " + str(address))
        client = ('client0'+str(len(clients) + 1), client_socket)
        clients[client[0]] = client[1]
        print(client[0])
        thread = threading.Thread(target=clientHandler, args=(client[0],))
        thread.start()
    return None

def start_server() -> None: 
    #create a new socket given address and protocol number 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('localhost', 12345))
    serverSocket.listen(MAX_CLIENTS) 

    print("Server is listening...") 

    listening(serverSocket)

    return None

if __name__ == '__main__':
    start_server()