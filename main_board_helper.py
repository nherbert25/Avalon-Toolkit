import threading
import queue
import time
import requests
import tkinter as tk



import characters
import client_board_state


list_of_characters = {'Merlin': 0, 'Percival': 0, 'Resistance': 0, 'Morgana': 0, 'Assassin': 0, 'Mordred': 0, 'Oberon': 0, 'Spy': 0}








def char_add(character, characters_widget, list_of_characters=list_of_characters):
	list_of_characters[character] += 1
	characters_widget.config(text=list_of_characters)
	return list_of_characters


def char_remove(character, characters_widget, list_of_characters=list_of_characters):
	if list_of_characters[character] > 0:
		list_of_characters[character] -= 1
		characters_widget.config(text=list_of_characters)
	return list_of_characters

#def board_state():
#	my_client.send('!PLAYERSTATE')


def select_player():
	pass


def start_game(widget, start_button, list_of_characters):
	role_count = 0
	for key in list_of_characters:
		role_count += list_of_characters[key]

	if  role_count >= len(client_board_state.players):
		#add to queue  !GAMESTART
		client_board_state.roles = list_of_characters
		client_board_state.client_queue.append(['!GAMESTART', client_board_state.roles])
		print('Starting game!')
		#widget.grid_forget()
		start_button.configure(state=tk.DISABLED)
		#widget.destroy()
	else:
		print(role_count)




def game_started(widget):
	#when receiving !GAMESTART from the server, start the game
	#run  config_base_frame.grid_forget()
	#run  function to create voting widget
	#get list of players from the server/update players to sit in order
	#reveal information to players
	#update game board to show who's turn it is
	widget.destroy()
	pass





'''
import time
def threaded_server_connection_i_dunno():

	threading._start_new_thread( threaded_server_connection, que )

	starttime = time.time()
	while True:
		print("tick")
		#threading.Timer(1.0, threaded_server_connection(que)).start()
		threaded_server_connection(que)
		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
'''



    # player = {
    # 'name': name, 
    # 'role': '',  #class object?
    # 'votes': [],
    # 'on_team': [],
    # 'made_team': []
    # }
#takes in player object from board state
def playerframetext(player, player_frames, username, user_info):
	display_text = player['name']


	#user_role = client_board_state.board_state['players']

	print(f'user_info:    {user_info}')
	#print(f'TESTING!!!!!!!:   {characters.character_dictionary}')


	user_role = characters.character_dictionary[user_info['role']]
	print(f'TESTING user_role!!!!!!!:   {user_role}\r\n')



	player_role = player['role']
	#player_role = characters.character_dictionary[player['role']]
	print(f'TESTING player_role!!!!!!!:   {player_role}\r\n')


	if player_role in user_role[1]:
		#set background to red if evil
		bg = '#cf2121'
		player_frames.configure(bg = bg)


	if player['name'] == username and user_role[0] == 'evil':
		#set background to red if evil
		bg = '#cf2121'
		player_frames.configure(bg = bg)



	#if player_role in characters.character_dictionary[player.role.lower()]



	#print(player['name'])
	#print('username: '+username)
	if user_info['role'] == 'Percival' and player_role in user_role[2]:
		display_text += '\r\n'
		display_text += 'Merlin?'

	if player['name'] == username:
		display_text += '\r\n'
		display_text += player['role']

	return display_text