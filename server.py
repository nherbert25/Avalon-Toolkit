import socket
import threading


#threading lets you seperate code out so it's not stacked waiting for code to finish

HEADER = 64
PORT = 5050 #arbitrary port number
#SERVER = '192.168.1.47' #this is the device the serve will run off of. ipconfig
SERVER = socket.gethostbyname(socket.gethostname())  #pulls in the ipaddress based off your computer's local name
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#this is all of the data coming in
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#anything that hits this address, hits this socket
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)



            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}]: {msg}")
            conn.send("Message received!".encode(FORMAT))

    conn.close()





def start():
    server.listen()
    print(f"[LISTENING]: Server is listening on {SERVER}")
    while True:
        #when a new connection occurs, we'll parse "socket object", "information about the connection"
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[# of ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")
    pass





print("[STARTING]: Server is starting")
start()



