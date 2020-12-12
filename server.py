import socket
import threading
import random
import pickle
import traceback


import server_board_state






#threading lets you seperate code out so it's not stacked waiting for code to finish

#number of bytes of the header message
HEADER = 64
PORT = 5050 #arbitrary port number, may have to consider port forwarding




#If you leave SERVER as a blank string, when running "server.bind(ADDR)" it will bind to any available ip address.
#For my computer, there's only one. It doesn't display anything... but it still works and is functionally identical to hard coding this to my IP ('192.168.1.47')
#SERVER = '192.168.1.47' #this is the device the serve will run off of. ipconfig
#SERVER = socket.gethostbyname(socket.gethostname())  #pulls in the ipaddress based off your computer's local name
SERVER = ''


ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
SERVER_TIMEOUT = 12 #automatically disconnect from client after x seconds if we don't hear anything
DISCONNECT_MESSAGE = "!DISCONNECT"


#this is all of the data coming in
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#anything that hits this address, hits this socket
server.bind(ADDR)



lock = threading.Lock()








#main function for handling client pings
#expects a list ['!INSTRUCTION', DATA_TYPE]
def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")

    connected = True
    while connected:

        try:

            msg_length = conn.recv(HEADER).decode(FORMAT)


            lock.acquire()




            #if message is not None
            if msg_length:
                msg_length = int(msg_length)
                msg = pickle.loads(conn.recv(msg_length))
                print(f"[Received the following instructions from {addr}]: {msg}")



                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"Received disconnect request from {addr}.")
                    message = "!NONE"

                    print(f"Client {addr} sent disconnect message. Closing thread, unlocking if thread is locked.")
                    print(f"Is a lock on? {lock.locked()}")
                    lock.release()
                    print(f"Is a lock on? {lock.locked()}")
                    if lock.locked():
                        lock.release()
                    continue


                elif msg[0] == '!INITIAL_CONNECT':

                    client_username = msg[1]

                    if client_username in server_board_state.players:
                        #send server state to reconnect the player
                        print('Player already logged in, reconnecting.')
                        message = ['!INITIAL_CONNECT', client_username, server_board_state.board_state]

                    else:
                        if client_username not in (None, ''):
                            server_board_state.players.append(client_username)
                            message = ['!INITIAL_CONNECT', client_username, server_board_state.board_state]

                        else:
                            message = ['!INITIAL_CONNECT', client_username, server_board_state.board_state]



                elif msg[0] == '!GAMESTART':
                    #randomize player orders and roles
                    random.shuffle(server_board_state.players)
                    server_board_state.roles = server_board_state.create_roles_list(msg[1])
                    random.shuffle(server_board_state.roles)

                    server_board_state.board_state = server_board_state.create_board_state(server_board_state.players)
                    server_board_state.board_state['phase'] = 'picking_phase'
                    server_board_state.start_game(server_board_state.board_state)
                    #server_board_state.next_round(server_board_state.board_state)
                    
                    #send game start to all clients with player information to each player
                    message = ['!GAMESTART', server_board_state.board_state]





                elif msg[0] == '!BOARDSTATE':
                        message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.players, server_board_state.message_to_client(server_board_state.board_state)]]



                elif msg[0] == '!PLAYERSTATE':
                    message = ['!PLAYERSTATE', server_board_state.players]




                elif msg[0] == '!TEAMSELECT':

                    selected_team = msg[1]
                    server_board_state.board_state['team_selected'] = selected_team

                    #if team is not null? 
                    for player in server_board_state.board_state['players']:

                        #update player data to show who made team
                        try:
                            player['made_team'][server_board_state.board_state['round']-1].append(None)
                            if player['name'] == server_board_state.board_state['player_picking_team']:
                                player['made_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1] = True
                            else:
                                player['made_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1] = False
                        except:
                            print(f"\r\nSomething went wrong updating player_picking_team data point")
                            # print(f"Made team: {server_board_state.board_state['player_picking_team']},  Player made team data points: {player['made_team']}\r\n")
                            pass
                        #update player data to show them on team
                        try:
                            #if turn is longer than array, add player to selected team
                            #if len(player['on_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1]) < server_board_state.board_state['turn']:
                            
                            player['on_team'][server_board_state.board_state['round']-1].append(None)

                            if player['name'] in server_board_state.board_state['team_selected']:
                                player['on_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1] = True
                                #player['on_team'][server_board_state.board_state['round']-1].append(True)
                            else:
                                # player['on_team'][server_board_state.board_state['round']-1].append(False)
                                player['on_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1] = False

                        except:
                            print('\r\nThis function has already been ran? Something went wrong.')
                            # print(f"{len(player['on_team'][server_board_state.board_state['round']-1][server_board_state.board_state['turn']-1])}")
                            # print(f"{server_board_state.board_state['turn']}")
                            # print(f"{player['name']}, {server_board_state.board_state['team_selected']}, player on team round array: {player['on_team'][server_board_state.board_state['round']-1]}")
                            pass

                    #if turn 5, force the hammer
                    # if server_board_state.board_state['turn'] == 5:
                    #     server_board_state.board_state['phase'] = 'mission_phase'

                    #otherwise update voting data points and set mission phase to waiting_on_votes
                    # else:
                    server_board_state.board_state['waiting_on_votes'] = server_board_state.get_list_of_player_names(server_board_state.board_state)
                    server_board_state.board_state['votes_cast'] = []
                    server_board_state.board_state['mission_votes_cast'] = []

                    to_send_message = f"Waiting on votes from: {server_board_state.board_state['waiting_on_votes']}"
                    print(to_send_message)


                    server_board_state.board_state['phase'] = 'voting_phase'
                    message = ['!VOTINGPHASE', [server_board_state.board_state, to_send_message]]






                elif msg[0] == '!VOTE':
                    player_voting = msg[1]
                    vote = msg[2]

                    if player_voting in server_board_state.board_state['waiting_on_votes']:

                        server_board_state.board_state['waiting_on_votes'].remove(player_voting)
                        server_board_state.board_state['votes_cast'].append([player_voting, vote])




                    #if not waiting on anyone, append votes to players and either go to next round or begin mission phase
                    if len(server_board_state.board_state['waiting_on_votes']) == 0:
                        print('calculating!')



                        server_board_state.board_state, vote_message = server_board_state.calculate_votes()  # 'approve' 'reject'

                        #print(f'Calculated votes! Team {team_approve_or_reject}')

                        print(vote_message)
                        message = ['!ENDVOTINGPHASE', [server_board_state.board_state, vote_message]]



                    else:
                        to_send_message = f"Waiting on votes from: {server_board_state.board_state['waiting_on_votes']}"
                        message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.players, to_send_message]]






                elif msg[0] == '!MISSION':
                    player_voting = msg[1]
                    mission_vote = msg[2]


                    if player_voting in server_board_state.board_state['team_selected']:

                        server_board_state.board_state['team_selected'].remove(player_voting)
                        server_board_state.board_state['mission_votes_cast'].append([player_voting, mission_vote])


                    #if not waiting on anyone, append votes to players and either go to next round or begin mission phase
                    if len(server_board_state.board_state['team_selected']) == 0:
                        print('calculating!')

                        #appends success/failure to board_state['mission'], calculates and changes phase to next round or assassination phase. Returns a string meant for players (round 4 failed with 2 fails!)
                        server_board_state.board_state, mission_message = server_board_state.calculate_mission_votes()
                        print('calculated votes!')
                        print(mission_message)

                        message = ['!ENDMISSION', [server_board_state.board_state, mission_message]]






                    #if vote does not exist for player, add player and vote

                    #else ignore


                    #if all votes are accounted for, add information to the player sheets (reveal the information) and update the phase
                        #if pass go to mission phase
                        #if fail, call next turn function
                    
                    
                    else:
                        message = ['!MISSION', [server_board_state.board_state, server_board_state.players]]


                else:
                    message = "!NONE"


                # if message[0] == '!BOARDSTATE':
                #     print(f"[Sending back to client: {addr}]: {server_board_state.message_to_client(server_board_state.board_state)}\r\n")
                if message[0] != '!BOARDSTATE':
                    print(f"[Sending back to client: {addr}]: {message}\r\n")

                message = pickle.dumps(message)
                conn.send(message)

                lock.release()
                #conn.send("!NONE".encode(FORMAT))


        #lock.locked() shows the visual studio error: "Instance of 'lock' has no 'locked' member" but it's a bug. This method works.
        except (socket.timeout):
            connected = False
            print(f"Connection to {addr} timed out!")
            print(f"Is a lock on? {lock.locked()}. We are releasing the lock immediately after this line if one exists, if there is an error around here, this might be the issue.")
            print(f"Note if the above line is True when testing with a single connection!!! If there is only one thread and it's not locked, we should NOT be unlocking on the following line.")

            #Still to be determined if this error keeps the lock or not! This may be a bug!
            if not lock.locked() and (threading.activeCount() - 1) == 1:
                print(f"ERROR: SINGLE THREAD IS NOT LOCKED AFTER DISCONNECT, YET WE'RE ATTEMPTING TO UNLOCK AFTER THIS LINE. THIS IS A CRITICAL ERROR")
            if lock.locked():
                lock.release()

        except ConnectionResetError:
            connected = False
            print(f"Client unexpectedly closed, aborting send data. {addr} timed out!")
            print(f"Is a lock on? {lock.locked()}")
            #lock.release()
            if lock.locked() and (threading.activeCount() - 1) == 1:
                print(f"ERROR: SINGLE THREAD IS STILL LOCKED AFTER {ConnectionResetError}. THIS IS A CRITICAL ERROR. UPDATE THIS EXCEPTION BLOCK.")

        except Exception as e:
            connected = False
            print(f"WARNING: UNEXPECTED ERROR IN CLIENT DISCONNECT: {e}")
            print(traceback.format_exc())
            print(f"WARNING: Connection to {addr} broke unexpectedly! We're not sure what the issue was!!")
            print(f"WARNING: We don't know what caused this disconnect error. If this specific thread is locking it must be released or you will hang the server. Catch and categorize this error!")
            print(f"Testing if thread is currently locked: Is a lock on? {lock.locked()}")
            if lock.locked() and (threading.activeCount() - 1) == 1:
                print(f"ERROR: SINGLE THREAD IS STILL LOCKED AFTER DISCONNECTING. THIS IS A CRITICAL ERROR. CATAGORIZE THIS ERROR AND SET TO UNLOCK, IMMEDIATELY.")
            #lock.release()


    conn.close()
    print("\r\n\r\nLooks like the client disconnected. Running close thread operations and closing thread.")

    print(f"Checking if this is the last active thread. If it is, we should make sure thread is unlocked.")
    print(f"[# of ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")
    if (threading.activeCount() - 1) == 1 and lock.locked():
        print("ERROR: LAST ACTIVE THREAD WAS LOCKED, CALLING EMERGENCY UNLOCK")
        lock.release()


    print(f"Last known board and player state:\r\n")
    print("board_state =", server_board_state.board_state)
    print("players =", server_board_state.players, "\r\n\r\n")
    #print(f"[# of ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")




#ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

##    lock = threading.Lock()
    #lock.acquire()
    #lock.release()














def start():
    server.listen()
    print(f"[LISTENING]: Server is listening on {SERVER}")
    while True:
        #when a new connection occurs, we'll parse "socket object", "information about the connection"
        conn, addr = server.accept()
        conn.settimeout(SERVER_TIMEOUT)



        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[# of ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")






print("[STARTING]: Server is starting")
start()



