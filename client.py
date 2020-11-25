import socket
import time
import queue
import threading
import client_board_state


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

        return_message = self.client.recv(2048).decode(self.FORMAT)
        print(f"server return message: {return_message}")
        return(return_message)


    def receive(self, msg):
        message = msg.decode(self.FORMAT)
        print(message)


    def initial_connect(self):
        username = input('Enter your name: ')
        print('!USERNAME',username)
        self.send('!USERNAME '+username)
        return(username)

    def board_state(self):

        print('Asking server for board state...')
        #threading.Timer(1.0, threaded_server_connection(que)).start()

        string_players = self.send('!PLAYERSTATE')
        players = string_players.split(" ")
        print(f'players: {players}')
        return(players)


    ###################################################################################################
    #Queued threading for sending/receiving from server
    #https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/

    # A thread that produces data 
    def producer(self, out_q): 
        while True: 
            # Produce some data 
            out_q.put(self.board_state())
            time.sleep(5)
            

    # A thread that consumes data 
    def consumer(self, in_q):
        while True: 
            # Get some data 
            data = in_q.get() 

            print(data)

            # Process the data 
            client_board_state.players = data
            time.sleep(5)



def main():


    my_client = Client()

    client_board_state.username = my_client.initial_connect()
    print(client_board_state.username)
    client_board_state.players = client_board_state.username


            
    # Create the shared queue and launch both threads 
    q = queue.Queue() 
    t1 = threading.Thread(target = my_client.consumer, args =(q, )) 
    t2 = threading.Thread(target = my_client.producer, args =(q, )) 
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()