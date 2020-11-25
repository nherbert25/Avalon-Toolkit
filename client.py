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







    def send_instructions_to_server(self, instructions=None):


        #do instructions





        #ask server for board state
        print('Asking server for board state...')

        #print('Sending to server board state...')
        #threading.Timer(1.0, threaded_server_connection(que)).start()

        string_players = self.send('!PLAYERSTATE')
        players = string_players.split(" ")
        print(f'players: {players}')


        #returns list of players from the server
        return(players)






    def ask_server_for_board_state(self):


        #do instructions

        #ask server for board state
        print('Asking server for board state...')

        #print('Sending to server board state...')
        #threading.Timer(1.0, threaded_server_connection(que)).start()

        string_players = self.send('!PLAYERSTATE')
        players = string_players.split(" ")
        print(f'players: {players}')


        #returns list of players from the server
        return(players)









    ###################################################################################################
    #Queued threading for sending/receiving from server
    #https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/

    # A thread that produces data and puts it on the queue
    def to_server_queue(self, send_queue, instructions): 
        while True: 

            # Produce some data 

            #put the return of this function into the queue
            send_queue.put(self.send_instructions_to_server(instructions))
            time.sleep(5)





    # A thread that consumes data and takes it from the queue
    def from_server_queue(self, receive_queue):
        while True: 

            # ask server for board state and put it on the queue
            receive_queue.put(self.ask_server_for_board_state())


            # set board state to variable
            data = receive_queue.get() 

            print(data)

            # Process the board state 
            client_board_state.players = data
            time.sleep(5)









#################################################################################
def main():


    my_client = Client()
    #my_example_var = 'TESTING!!!'
    #print(my_example_var)



    client_board_state.username = my_client.initial_connect()
    print(client_board_state.username)
    client_board_state.players = client_board_state.username


            
    # Create the shared queue and launch both threads 
    send_to_server_queue = queue.Queue() 

    received_from_server_queue = queue.Queue()



    t1 = threading.Thread(target = my_client.from_server_queue, args =(send_to_server_queue, ), daemon = True)

    #t2 = threading.Thread(target = my_client.to_server_queue, args =(received_from_server_queue, ), daemon = True)


    t1.start()
    #t2.start()


    return my_client, send_to_server_queue


if __name__ == '__main__':
    main()