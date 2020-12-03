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
                    message = ['!BOARDSTATE', [server_board_state.board_state, server_board_state.player_state()]]



            elif msg[0] == '!PLAYERSTATE':
                message = ['!PLAYERSTATE', server_board_state.player_state()]







            else:
                message = "!NONE"




            print(f"[Sending back to client: {addr}]: {message}\r\n")
            message = pickle.dumps(message)
            conn.send(message)
            #conn.send("!NONE".encode(FORMAT))
    conn.close()
















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



