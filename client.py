import socket


HEADER = 64
PORT = 5050
#SERVER = '192.168.1.47' #this is the device the serve will run off of. ipconfig
print(socket.gethostbyname(socket.gethostname()))
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    #message must be 64 bits to be valid
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    print(client.recv(2048).decode(FORMAT))


send("Hello world!")


send(input())


send(DISCONNECT_MESSAGE)