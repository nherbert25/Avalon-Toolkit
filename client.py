import pickle
import socket
import time
import queue
import threading
import client_board_state


class Client():

    # fixed header length
    HEADER = 64

    # IP address of the server that we're connecting to
    # set this to the IP address of the AWS server! Ex: 172.105.4.10
    # SERVER_IP = '192.168.1.47' #this is the device the serve will run off of. ipconfig
    SERVER_IP = socket.gethostbyname(socket.gethostname())
    # SERVER_IP = "34.122.32.4" #google ip
    # SERVER_IP = "45.33.6.23"  #Linode manager ip address. This is an external ip. USE THIS ADDRESS TO CONNECT TO ONLINE SERVER!

    # may have to consider port forwarding
    PORT = 5050

    ADDR = (SERVER_IP, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    RECEIVE_MESSAGE_LENGTH = 3048
    # 0.5 #number of seconds to sleep before request full board state from the server again
    CLIENT_CONNECT_TIME = 2

    # this is all of the data coming in
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    def __init__(self):
        print(f'Server IP Address: {self.SERVER_IP}')

    ###########################################################################
    # client methods

    # sends a message to the server and receives a message back. WILL HANG IF IT DOES NOT RECEIVE A MESSAGE BACK FROM THE SERVER!!!

    def send(self, msg):

        print(f"[Client Send Function] Sending instructions: {msg}")
        message = pickle.dumps(msg)

        # determine the length of the message to be sent to the server, message must be 64 bits to be valid
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        # b' ' means the byte representation of a space
        send_length += b' ' * (self.HEADER - len(send_length))

        # send message length then message to the server
        # client.send is a method of the socket object, NOT this send method. See the following: client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.send(send_length)
        self.client.send(message)

        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)

        # if message is not None
        if msg_length:
            # set the received message length to be dynamically returned from server
            msg_length = int(msg_length)
            print(f"Message length in bytes: {msg_length}")
            return_message = pickle.loads(self.client.recv(msg_length))
            #return_message = pickle.loads(self.client.recv(self.RECEIVE_MESSAGE_LENGTH))

            print(
                f"[Client Send Function] Server return message: {return_message}")
            return(return_message)

    # def receive(self, msg):
    #     message = msg.decode(self.FORMAT)
    #     print(message)

    def initial_connect(self, username):
        print('got here')
        username = self.send(['!INITIAL_CONNECT', username])
        print('got here')
        return(username)

    def send_instructions_to_server(self, instruction):

        # if instruction == '!GAMESTART':
        #     server_return = self.send(instruction)

        # else:
        #     server_return = self.send(instruction)
        server_return = self.send(instruction)

    def ask_server_for_board_state(self):

        # do instructions

        # ask server for board state
        print(
            '\r\n\r\n[ask_server_for_board_state] Asking server for board state...')

        #print('Sending to server board state...')
        #threading.Timer(1.0, threaded_server_connection(que)).start()

        #client_board_state.board_state = self.send(['!BOARDSTATE'])

        # if client_board_state.board_state['phase'] == 'lobby_phase':
        #     string_players = self.send(['!PLAYERSTATE'])
        #     players = string_players
        #     print(f'[ask_server_for_board_state] Server returned the following for !PLAYERSTATE: {players}')
        #     return players

        return_data = self.send(['!BOARDSTATE'])

        return(return_data)

        # else:
        #     return board_state

    ###################################################################################################
    # Queued threading for sending/receiving from server
    # https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/

    # A thread that produces data and puts it on the queue

    def to_server_queue(self, send_queue, lock):
        while True:

            # put pre-queue onto queue
            if client_board_state.client_queue:
                for instruction in client_board_state.client_queue:
                    send_queue.put(instruction)

            # clear the pre-queue
            client_board_state.client_queue = []

            # debugging
            for elem in list(send_queue.queue):
                print(f'To Server Queue: {elem}')

            # send instructions to the server
            while not send_queue.empty():
                self.send_instructions_to_server(send_queue.get())
                #print('sent instructions!!')

            time.sleep(1)

    # queue which runs every x seconds. Updates the client boardstate to match the server board state

    def from_server_queue(self, receive_queue, lock):
        while True:

            # ask server for board state and put it on the queue
            data_recieved = self.ask_server_for_board_state()

            if data_recieved[0] != '!NONE':
                receive_queue.put(data_recieved)

            # for elem in list(receive_queue.queue):
            #    print(f'[from_server_queue] From Server Queue: {elem}')

            #print(f'From Server Queue: {list(receive_queue)}')
            # set board state to variable

            for elem in list(receive_queue.queue):
                instruction, data = receive_queue.get()

                lock.acquire()

                # if instruction == '!INITIAL_CONNECT':
                #     if client_board_state.board_state != data[0]:
                #         client_board_state.board_state = data[0]

                #     client_board_state.message_from_server = data[1]

                # if instruction == '!GAMESTART':
                #     if client_board_state.board_state != data[0]:
                #         client_board_state.board_state = data[0]

                #     client_board_state.message_from_server = data[1]

                if instruction == '!PLAYERSTATE':
                    client_board_state.players = data
                    #client_board_state.board_state = data

                elif instruction == '!GAMESTART':
                    client_board_state.board_state = data

                elif instruction == '!BOARDSTATE':
                    if client_board_state.board_state != data[0]:
                        client_board_state.board_state = data[0]
                    if client_board_state.players != data[1]:
                        client_board_state.players = data[1]

                    try:
                        if data[2] != '':
                            client_board_state.message_from_server = data[2]
                            print(client_board_state.message_from_server)
                    except:
                        pass

                elif instruction == '!VOTINGPHASE':
                    if client_board_state.board_state != data[0]:
                        client_board_state.board_state = data[0]
                    client_board_state.message_from_server = data[1]

                elif instruction == '!ENDVOTINGPHASE':
                    if client_board_state.board_state != data[0]:
                        client_board_state.board_state = data[0]
                    client_board_state.message_from_server = data[1]

                elif instruction == '!ENDMISSION':
                    if client_board_state.board_state != data[0]:
                        client_board_state.board_state = data[0]
                    client_board_state.message_from_server = data[1]

                else:
                    if client_board_state.board_state != data[0]:
                        client_board_state.board_state = data[0]

                lock.release()

            time.sleep(self.CLIENT_CONNECT_TIME)


#################################################################################
def main():

    lock = threading.Lock()
    lock.acquire()

    my_client = Client()

    # sends !INITIAL_CONNECT to server, which takes in the username from client_board_state and adds it to the player list there
    initial_connect_to_client = my_client.initial_connect(
        client_board_state.username)
    print(
        f'initial connect:  {initial_connect_to_client}, {initial_connect_to_client[1]}')
    client_board_state.username = initial_connect_to_client[1]
    client_board_state.board_state = initial_connect_to_client[2]

    print(f'client username:  {client_board_state.username}')
    print(f'client board state:  {client_board_state.board_state}')

    lock.release()

    # Create the shared queue and launch both threads
    send_to_server_queue = queue.Queue()
    received_from_server_queue = queue.Queue()

    t1 = threading.Thread(target=my_client.from_server_queue, args=(
        send_to_server_queue, lock), daemon=True)
    t2 = threading.Thread(target=my_client.to_server_queue, args=(
        received_from_server_queue, lock), daemon=True)

    t1.start()
    t2.start()

    return my_client, send_to_server_queue, lock


if __name__ == '__main__':
    main()
