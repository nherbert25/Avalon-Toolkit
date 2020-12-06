import socket
import threading
import random
import pickle

import server_board_state






#threading lets you seperate code out so it's not stacked waiting for code to finish

HEADER = 64
PORT = 5050 #arbitrary port number
#SERVER = '192.168.1.47' #this is the device the serve will run off of. ipconfig
SERVER = socket.gethostbyname(socket.gethostname())  #pulls in the ipaddress based off your computer's local name
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





        if msg_length:
            msg_length = int(msg_length)
            msg = pickle.loads(conn.recv(msg_length))
            print(f"[Received the following instructions from {addr}]: {msg}")



            if msg == DISCONNECT_MESSAGE:
                connected = False
                message = "!NONE"


            elif msg[0] == '!INITIAL_CONNECT':
                if msg[1] in server_board_state.players:
                    #send server state to reconnect the player
                    print('player already logged in')

                    message = ['!INITIAL_CONNECT', msg[1], server_board_state.board_state]
                    #message = msg[1]

                else:
                    server_board_state.players.append(msg[1])
                    message = ['!INITIAL_CONNECT', msg[1], server_board_state.board_state]



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

                #SEND THIS TO ALL CONNECTED CLIENTS!!!!!




            elif msg[0] == '!BOARDSTATE':
                    message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.players]]



            elif msg[0] == '!PLAYERSTATE':
                message = ['!PLAYERSTATE', server_board_state.players]




            elif msg[0] == '!TEAMSELECT':




                server_board_state.board_state['team_selected'] = msg[1]
                selected_team = msg[1]


                #if 5th round:
                #server_board_state.board_state['phase'] = 'mission_phase'


                #if NOT fifth round:


                #list of list
                server_board_state.board_state['waiting_on_votes'] = server_board_state.get_list_of_player_names(server_board_state.board_state)
                server_board_state.board_state['votes_cast'] = []
                server_board_state.board_state['mission_votes_cast'] = []

                print(f"Waiting on votes from: {server_board_state.board_state['waiting_on_votes']}")


                server_board_state.board_state['phase'] = 'voting_phase'
                message = ['!VOTINGPHASE', [server_board_state.board_state, server_board_state.players]]






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
                    message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.players]]






            elif msg[0] == '!MISSION':
                player_voting = msg[1]
                mission_vote = msg[2]


                if player_voting in server_board_state.board_state['team_selected']:

                    server_board_state.board_state['team_selected'].remove(player_voting)
                    server_board_state.board_state['mission_votes_cast'].append([player_voting, vote])


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



