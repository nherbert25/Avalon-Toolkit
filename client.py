import socket


class Client():

    HEADER = 64
    PORT = 5050
    #SERVER = '192.168.1.47' #this is the device the serve will run off of. ipconfig
    print(socket.gethostbyname(socket.gethostname()))
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    def __init__(self):
        pass

    #this is all of the data coming in
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)


    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)

        #message must be 64 bits to be valid
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

        print(self.client.recv(2048).decode(self.FORMAT))


    def receive(self, msg):
        message = msg.decode(self.FORMAT)
        print(message)






#client.recv(1024)
#send("Hello world!")
#send(input())

#send(DISCONNECT_MESSAGE)