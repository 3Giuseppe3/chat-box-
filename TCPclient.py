import socket 
import threading

def send_message(s: socket.socket, name: str) -> None: 
    while True: 
        inp = input("") 
        client_message = name + ": " + input 
        s.send(client_message.encode())
        
    return None

def recieve(s: socket.socket) -> None: 
    while True: 
        message = s.recv(1024).decode() 

    return None

def talk_server(s: socket.socket, name: str) -> None: 
    s.send(name.encode())
    thread = threading.Thread(target = recieve)
    thread.start()
    send_message(s , name)

    return None

def start_client() ->None:
    sock = socket.socket() 
    sock.connect(('localhost', 12345))

    name = input("Enter your name: ")

    talk_server(sock, name)
    return None

if __name__ == '__main__':
    start_client()