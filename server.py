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
            '!DISCONNECT': self.client_disconnect,
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
    # takes the list [my_function, var1, var2, var3] sent by the client and converts/runs it as my_function(var1, var2, var3) according to the network_commands table
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

    def receive_message(self, client_socket):

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

    def client_disconnect(self, connected):
        print(f"Received disconnect request from {addr}.")

        connected = False
        message = "!NONE"

        print(
            f"Client {addr} sent disconnect message. Closing thread, unlocking if thread is locked.")
        print(f"Is a lock on? {self.lock.locked()}")

        if self.lock.locked():
            print("Great, unlocking and killing thread.")
            self.lock.release()
            print(f"Is a lock on? {self.lock.locked()}")

        return (connected, message)

    def client_initial_connect(self, msg):
        client_username = msg[1]

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

    # once a client connects, a thread is created and this function runs indefintely within that thread
    def handle_client_revamp(self, conn, addr):
        print(f"[NEW CONNECTION]: {addr} connected.")

        connected = True

        while connected:

            try:
                # conn.recv is a locking function, waits here until a message is received from the client
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                self.lock.acquire()

                # if message is not None
                if msg_length:
                    msg_length = int(msg_length)
                    msg = pickle.loads(conn.recv(msg_length))
                    print(
                        f"[Received the following instructions from {addr}]: {msg}")

                    self.process_network_command(msg)

                else:
                    message = "!NONE"

                # send response message to client
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

            except:
                pass

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION]: {addr} connected.")

        connected = True
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

                    if msg == self.DISCONNECT_MESSAGE:
                        connected = False
                        print(f"Received disconnect request from {addr}.")
                        message = "!NONE"

                        print(
                            f"Client {addr} sent disconnect message. Closing thread, unlocking if thread is locked.")
                        print(f"Is a lock on? {self.lock.locked()}")

                        if self.lock.locked():
                            print("Great, unlocking and killing thread.")
                            self.lock.release()
                            print(f"Is a lock on? {self.lock.locked()}")

                        continue

                    elif msg[0] == '!INITIAL_CONNECT':

                        client_username = msg[1]

                        if client_username in server_board_state.players:
                            # send server state to reconnect the player
                            print('Player already logged in, reconnecting.')
                            message = ['!INITIAL_CONNECT', client_username,
                                       server_board_state.board_state]

                        else:
                            if client_username not in (None, ''):
                                server_board_state.players.append(
                                    client_username)
                                message = ['!INITIAL_CONNECT', client_username,
                                           server_board_state.board_state]

                            else:
                                message = ['!INITIAL_CONNECT', client_username,
                                           server_board_state.board_state]

                    elif msg[0] == '!GAMESTART':
                        # randomize player orders and roles
                        random.shuffle(server_board_state.players)
                        server_board_state.roles = server_board_state.create_roles_list(
                            msg[1])
                        random.shuffle(server_board_state.roles)

                        server_board_state.board_state = server_board_state.create_board_state(
                            server_board_state.players, server_board_state.board_state)
                        server_board_state.board_state['phase'] = 'picking_phase'
                        server_board_state.start_game(
                            server_board_state.board_state)
                        # server_board_state.next_round(server_board_state.board_state)

                        # send game start to all clients with player information to each player
                        message = ['!GAMESTART',
                                   server_board_state.board_state]

                    elif msg[0] == '!BOARDSTATE':
                        message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.players,
                                                   server_board_state.message_to_client(server_board_state.board_state)]]

                    elif msg[0] == '!PLAYERSTATE':
                        message = ['!PLAYERSTATE', server_board_state.players]

                    elif msg[0] == '!TEAMSELECT':

                        selected_team = msg[1]
                        server_board_state.board_state['team_selected'] = selected_team

                        # if team is not null?
                        for player in server_board_state.board_state['players']:

                            # update player data to show who made team
                            try:
                                player['made_team'][server_board_state.board_state['round'] -
                                                    1].append(None)
                                if player['name'] == server_board_state.board_state['player_picking_team']:
                                    player['made_team'][server_board_state.board_state['round'] -
                                                        1][server_board_state.board_state['turn']-1] = True
                                else:
                                    player['made_team'][server_board_state.board_state['round'] -
                                                        1][server_board_state.board_state['turn']-1] = False
                            except:
                                print(
                                    f"\r\nSomething went wrong updating player_picking_team data point")
                                # print(f"Made team: {server_board_state.board_state['player_picking_team']},  Player made team data points: {player['made_team']}\r\n")
                                pass
                            # update player data to show them on team
                            try:
                                # if turn is longer than array, add player to selected team
                                # if len(player['on_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1]) < server_board_state.board_state['turn']:

                                player['on_team'][server_board_state.board_state['round'] -
                                                  1].append(None)

                                if player['name'] in server_board_state.board_state['team_selected']:
                                    player['on_team'][server_board_state.board_state['round'] -
                                                      1][server_board_state.board_state['turn']-1] = True
                                    # player['on_team'][server_board_state.board_state['round']-1].append(True)
                                else:
                                    # player['on_team'][server_board_state.board_state['round']-1].append(False)
                                    player['on_team'][server_board_state.board_state['round'] -
                                                      1][server_board_state.board_state['turn']-1] = False

                            except:
                                print(
                                    '\r\nThis function has already been ran? Something went wrong.')
                                # print(f"{len(player['on_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1])}")
                                # print(f"{server_board_state.board_state['turn']}")
                                # print(f"{player['name']}, {server_board_state.board_state['team_selected']}, player on team round array: {player['on_team'][server_board_state.board_state['round']-1]}")
                                pass

                        # if turn 5, force the hammer
                        # if server_board_state.board_state['turn'] == 5:
                        #     server_board_state.board_state['phase'] = 'mission_phase'

                        # otherwise update voting data points and set mission phase to waiting_on_votes
                        # else:
                        server_board_state.board_state['waiting_on_votes'] = server_board_state.get_list_of_player_names(
                            server_board_state.board_state)
                        server_board_state.board_state['votes_cast'] = []
                        server_board_state.board_state['mission_votes_cast'] = [
                        ]

                        to_send_message = f"Waiting on votes from: {server_board_state.board_state['waiting_on_votes']}"
                        print(to_send_message)

                        server_board_state.board_state['phase'] = 'voting_phase'
                        message = ['!VOTINGPHASE', [
                            server_board_state.board_state, to_send_message]]

                    elif msg[0] == '!VOTE':
                        player_voting = msg[1]
                        vote = msg[2]

                        to_send_message = f"Waiting on votes from: {server_board_state.board_state['waiting_on_votes']}"
                        message = ['!BOARDSTATE', [
                            server_board_state.board_state, server_board_state.players, to_send_message]]

                        if player_voting in server_board_state.board_state['waiting_on_votes'] and server_board_state.board_state['phase'] == 'voting_phase':

                            server_board_state.board_state['waiting_on_votes'].remove(
                                player_voting)
                            server_board_state.board_state['votes_cast'].append(
                                [player_voting, vote])

                            to_send_message = f"Waiting on votes from: {server_board_state.board_state['waiting_on_votes']}"
                            message = ['!BOARDSTATE', [
                                server_board_state.board_state, server_board_state.players, to_send_message]]

                            # if not waiting on anyone, append votes to players and either go to next round or begin mission phase
                            if len(server_board_state.board_state['waiting_on_votes']) == 0:
                                print(
                                    'calculating votes in function calculate_votes!')

                                server_board_state.board_state, vote_message = server_board_state.calculate_votes(
                                    server_board_state.board_state)  # 'approve' 'reject'

                                #print(f'Calculated votes! Team {team_approve_or_reject}')
                                # print(vote_message)
                                message = ['!ENDVOTINGPHASE', [
                                    server_board_state.board_state, vote_message]]

                            # else:
                            #     to_send_message = f"Waiting on votes from: {server_board_state.board_state['waiting_on_votes']}"
                            #     message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.players, to_send_message]]

                    elif msg[0] == '!MISSION':
                        player_voting = msg[1]
                        mission_vote = msg[2]

                        message = ['!MISSION', [
                            server_board_state.board_state, server_board_state.players]]

                        if player_voting in server_board_state.board_state['team_selected'] and server_board_state.board_state['phase'] == 'mission_phase':

                            server_board_state.board_state['team_selected'].remove(
                                player_voting)
                            server_board_state.board_state['mission_votes_cast'].append(
                                [player_voting, mission_vote])

                            message = ['!MISSION', [
                                server_board_state.board_state, server_board_state.players]]

                            # if not waiting on anyone, append votes to players and either go to next round or begin mission phase
                            if len(server_board_state.board_state['team_selected']) == 0:
                                print('calculating!')

                                # appends success/failure to board_state['mission'], calculates and changes phase to next round or assassination phase. Returns a string meant for players (round 4 failed with 2 fails!)
                                server_board_state.board_state, mission_message = server_board_state.calculate_mission_votes(
                                    server_board_state.board_state)
                                print('calculated votes!')
                                print(mission_message)

                                message = ['!ENDMISSION', [
                                    server_board_state.board_state, mission_message]]

                        # if vote does not exist for player, add player and vote

                        # else ignore

                        # if all votes are accounted for, add information to the player sheets (reveal the information) and update the phase
                            # if pass go to mission phase
                            # if fail, call next turn function

                        # else:
                        #     message = ['!MISSION', [server_board_state.board_state, server_board_state.players]]

                    else:
                        message = "!NONE"

                    # if message[0] == '!BOARDSTATE':
                    #     print(f"[Sending back to client: {addr}]: {server_board_state.message_to_client(server_board_state.board_state)}\r\n")
                    # if message[0] != '!BOARDSTATE':
                    #    print(f"[Sending back to client: {addr}]: {message}\r\n")

                    #print(f"[Client Send Function] Sending instructions: {msg}")
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

            # lock.locked() shows the visual studio error: "Instance of 'lock' has no 'locked' member" but it's a bug. This method works.
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
                # lock.release()

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


"""

#!/usr/bin/python3
import asyncio 

loop = asyncio.get_event_loop()
try:
    loop.run_forever()
finally:
    loop.close()


example of an infinite loop. Maybe use this to continually scan for changes to board state, then loop through and send new board state to all clients?
"""
