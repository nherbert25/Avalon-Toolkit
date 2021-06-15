import pickle
import random
import select
import socket
import threading
import traceback
import functools

import server_board_state


class Server():

    def __init__(self):

        # number of bytes of the header message
        self.HEADER = 64
        self.PORT = 5050  # arbitrary port number, may have to consider port forwarding

        # If you leave SERVER as a blank string, when running "server.bind(ADDR)" it will bind to any available ip address.
        # For my computer, there's only one. It doesn't display anything... but it still works and is functionally identical to hard coding this to my IP ('192.168.1.47')
        # SERVER = '192.168.1.47' #this is the device the serve will run off of. ipconfig
        # SERVER = socket.gethostbyname(socket.gethostname())  #pulls in the ipaddress based off your computer's local name
        self.SERVER = ''
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        # automatically disconnect from client after x seconds if we don't hear anything
        self.SERVER_TIMEOUT = 12
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        ###################################################################################################
        ###################################################################################################

        # this is all of the data coming in
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allows ports to be reused after timeout error?...
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # anything that hits this address, hits this socket
        self.server.bind(self.ADDR)

        # mapping of possible client commands to the server
        self.network_commands = {
            '!DISCONNECT': 'placeholder',
            '!INITIAL_CONNECT': self.client_initial_connect,
            '!GAMESTART': 'placeholder',
            '!BOARDSTATE': 'placeholder',
            '!PLAYERSTATE': 'placeholder',
            '!TEAMSELECT': 'placeholder',
            '!VOTE': 'placeholder',
            '!MISSION': 'placeholder'
        }

        self.currently_connected_clients = {}
        self.lock = threading.Lock()

    ###################################################################################################
    ###################################################################################################
    # definitions

    # https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
    # https://softwareengineering.stackexchange.com/questions/182093/why-store-a-function-inside-a-python-dictionary/182095
    # takes the list [my_function, var1, var2, var3] sent by the client and converts then runs it as my_function(var1, var2, var3) according to the network_commands table
    def process_network_command(self, command):
        if len(command) > 1:
            adaptive_func = self.network_commands[command[0]]
            for ele in command[1:]:
                adaptive_func = functools.partial(
                    adaptive_func, ele)
            adaptive_func()
            return
        else:
            self.network_commands[command[0]]()

    def receive_message(self, conn, client_socket):

        addr = None
        msg = None

        try:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)

            # if message is None, client has disconnected
            if not len(msg_length):
                return False

            msg_length = int(msg_length)
            msg = pickle.loads(conn.recv(msg_length))
            print(f"[Received the following instructions from {addr}]: {msg}")

        except:
            return False

    ###################################################################################################
    ###################################################################################################

    def client_initial_connect(self, msg):
        client_username = msg[0]

        if client_username in server_board_state.players:
            # send server state to reconnect the player
            print('Player already logged in, reconnecting.')
            message = ['!INITIAL_CONNECT', client_username,
                       server_board_state.board_state]

        else:
            if client_username not in (None, ''):
                server_board_state.players.append(client_username)
                message = ['!INITIAL_CONNECT', client_username,
                           server_board_state.board_state]

            else:
                message = ['!INITIAL_CONNECT', client_username,
                           server_board_state.board_state]

        return message

    ###################################################################################################
    ###################################################################################################

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION]: {addr} connected.")

        connected = True

    ###################################################################################################

        def client_disconnect():
            nonlocal connected

            connected = False
            message = "!NONE"

            return (message)
        self.network_commands["!DISCONNECT"] = client_disconnect

    ###################################################################################################

        while connected:

            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                self.lock.acquire()

                # if message is not None
                if msg_length:
                    msg_length = int(msg_length)
                    msg = pickle.loads(conn.recv(msg_length))

                    print(
                        f"[Received the following instructions from {addr}]: {msg}")

                    self.process_network_command(msg)

                    print(
                        f"[Sending the following instructions to {addr}]: {msg}")
                    message = pickle.dumps(message)

                    # determine the length of the message to be sent to the server, message must be 64 bits to be valid
                    msg_length = len(message)
                    send_length = str(msg_length).encode(self.FORMAT)
                    # b' ' means the byte representation of a space
                    send_length += b' ' * (self.HEADER - len(send_length))

                    # send message length then message to the server
                    # client.send is a method of the socket object, NOT this send method. See the following: client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    conn.send(send_length)
                    conn.send(message)

                self.lock.release()

            except (socket.timeout):
                connected = False
                print(f"Connection to {addr} timed out!")
                print(
                    f"Is a lock on? {self.lock.locked()}. We are releasing the lock immediately after this line if one exists, if there is an error around here, this might be the issue.")
                print(f"Note if the above line is True when testing with a single connection!!! If there is only one thread and it's not locked, we should NOT be unlocking on the following line.")

                # Still to be determined if this error keeps the lock or not! This may be a bug!
                if not self.lock.locked() and (threading.activeCount() - 1) == 1:
                    print(
                        f"ERROR: SINGLE THREAD IS NOT LOCKED AFTER DISCONNECT, YET WE'RE ATTEMPTING TO UNLOCK AFTER THIS LINE. THIS IS A CRITICAL ERROR")
                if self.lock.locked():
                    self.lock.release()

            except ConnectionResetError:
                connected = False
                print(
                    f"Client unexpectedly closed, aborting send data. {addr} timed out!")
                print(f"Is a lock on? {self.lock.locked()}")
                # lock.release()
                if self.lock.locked() and (threading.activeCount() - 1) == 1:
                    print(
                        f"ERROR: SINGLE THREAD IS STILL LOCKED AFTER {ConnectionResetError}. THIS IS A CRITICAL ERROR. UPDATE THIS EXCEPTION BLOCK.")

            except Exception as e:
                connected = False
                print(
                    f"WARNING: SERVER IS CRASHING DUE TO TRACEBACK ERROR OR THERE IS AN UNEXPECTED ERROR IN CLIENT DISCONNECT: {e}")
                print(traceback.format_exc())
                print(
                    f"WARNING: Connection to {addr} broke unexpectedly! We're not sure what the issue was!!")
                print(f"WARNING: We don't know what caused this disconnect error. If this specific thread is locking it must be released or you will hang the server. Catch and categorize this error!")
                print(
                    f"Testing if thread is currently locked: Is a lock on? {self.lock.locked()}")
                if self.lock.locked() and (threading.activeCount() - 1) == 1:
                    print(f"ERROR: SINGLE THREAD IS STILL LOCKED AFTER DISCONNECTING. THIS IS A CRITICAL ERROR. CATAGORIZE THIS ERROR AND SET TO UNLOCK, IMMEDIATELY.")
                self.lock.release()

        self.lock.acquire()
        print(f"Connection to {client_username} broke!")
        print(f"Closing connection to address: {addr}")
        print(
            f"Closing connection in thread: {self.currently_connected_clients[addr]}")
        del self.currently_connected_clients[addr]
        print(f"Remaining clients: {self.currently_connected_clients}")
        self.lock.release()
        conn.close()

        print("\r\n\r\nLooks like the client disconnected. Running close thread operations and closing thread.")
        print(f"Checking if this is the last active thread. If it is, we should make sure thread is unlocked.")
        print(f"[# of ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")

        if (threading.activeCount() - 1) == 1 and self.lock.locked():
            print("ERROR: LAST ACTIVE THREAD WAS LOCKED, CALLING EMERGENCY UNLOCK")
            self.lock.release()

        print(f"Final check if thread is locked: {self.lock.locked()}")

        print(f"Last known board and player state:\r\n")
        print("board_state =", server_board_state.board_state)
        print("players =", server_board_state.players, "\r\n\r\n")

    def start_server(self):
        self.server.listen()
        print(f"[LISTENING]: Server is listening on {self.SERVER}")

        while True:
            # when a new connection occurs, we'll parse "socket object", "information about the connection" and start a server thread listening on this address
            # conn is a new socket object usable to send and receive data on the connection (client socket object)
            # address is the address bound to the socket on the other end of the connection
            # server.accept goes hand in hand with client.connect from the client.py module
            conn, addr = self.server.accept()
            conn.settimeout(self.SERVER_TIMEOUT)

            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))

            self.lock.acquire()
            self.currently_connected_clients[addr] = thread
            self.lock.release()

            thread.start()
            print(f"[# of ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")
            print(self.currently_connected_clients)


if __name__ == '__main__':
    print("[STARTING]: Server is starting")
    my_server = Server()
    my_server.start_server()


else:
    print("Server module loaded successfully.")
