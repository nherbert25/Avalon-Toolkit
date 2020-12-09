import socket
import threading
import random
import pickle

import server_board_state






#threading lets you seperate code out so it's not stacked waiting for code to finish

#number of bytes of the header message
HEADER = 64
PORT = 5050 #arbitrary port number, may have to consider port forwarding




#If you leave SERVER as a blank string, when running "server.bind(ADDR)" it will bind to any available ip address.
#For my computer, there's only one. It doesn't display anything... but it still works and is functionally identical to hard coding this to my IP ('192.168.1.47')
SERVER = '192.168.1.47' #this is the device the serve will run off of. ipconfig
#SERVER = socket.gethostbyname(socket.gethostname())  #pulls in the ipaddress based off your computer's local name
#SERVER = ''


ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

lock = threading.Lock()

#this is all of the data coming in
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#anything that hits this address, hits this socket
server.bind(ADDR)








#main function for handling client pings
#expects a list ['!INSTRUCTION', DATA_TYPE]
def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")

    connected = True
    while connected:



        msg_length = conn.recv(HEADER).decode(FORMAT)


        lock.acquire()




        #if message is not None
        if msg_length:
            msg_length = int(msg_length)
            msg = pickle.loads(conn.recv(msg_length))
            print(f"[Received the following instructions from {addr}]: {msg}")



            if msg == DISCONNECT_MESSAGE:
                connected = False
                message = "!NONE"


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


                print(server_board_state.roles)


                server_board_state.board_state = server_board_state.create_board_state(server_board_state.players)
                #send game start to all clients with player information to each player
                server_board_state.board_state['phase'] = 'picking_phase'
                server_board_state.start_game(server_board_state.board_state)
                #server_board_state.next_round(server_board_state.board_state)
                message = ['!GAMESTART', server_board_state.board_state]





            elif msg[0] == '!BOARDSTATE':
                    message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.players, server_board_state.message_to_client()]]



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



            if message[0] != '!BOARDSTATE':
                print(f"[Sending back to client: {addr}]: {message}\r\n")

            message = pickle.dumps(message)
            conn.send(message)

            lock.release()
            #conn.send("!NONE".encode(FORMAT))
    conn.close()



##    lock = threading.Lock()
    #lock.acquire()
    #lock.release()














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



