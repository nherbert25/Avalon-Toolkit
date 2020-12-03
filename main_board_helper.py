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





def select_player(player_frame, player_name):

	print(client_board_state.username)
	print('Currently ' + client_board_state.board_state['player_order'][0] + 's turn')
	print(f'Before pressing, these players are selected: {client_board_state.selected_players}')


	#if your turn, you may select players
	if client_board_state.username == client_board_state.board_state['player_order'][0]:

		max_players = client_board_state.board_state['team_size'][client_board_state.board_state['round']-1]


		if player_name in (client_board_state.selected_players):
			client_board_state.selected_players.remove(player_name)
			bg='#39658f'
			player_frame.configure(bg=bg)

		elif len(client_board_state.selected_players) < max_players:

			if player_name not in (client_board_state.selected_players):
				client_board_state.selected_players.append(player_name)
				
				
				bg='#ecf719'   #, fg='#ffffff'

				player_frame.configure(bg=bg)




		print(f'After pressing, these players are selected: {client_board_state.selected_players}')



def submit_team(all_player_frames):

	#if active player and # of selected players equals # of players for a team this round
	if client_board_state.username == client_board_state.board_state['player_order'][0] and len(client_board_state.selected_players) == client_board_state.board_state['team_size'][client_board_state.board_state['round']-1]:
		
		print('submitting!!')
		#send a voting command to the server!!!

		#MAKE SURE THIS RUNS AFTER YOU SUBMIT THIS INFORMATION TO THE SERVER
		#remove selected players from selected players list
		client_board_state.selected_players = []
		
		#return original color to players
		for player in all_player_frames:
			all_player_frames[player]['player_frame'].configure(bg='#39658f')


	else:
		print('It''s either not your turn or something''s wrong!')
		print(f'client user: {client_board_state.username}')
		print('active player: ' + client_board_state.board_state['player_order'][0])
		print('# of selected players: ' + str(len(client_board_state.selected_players)))
		print('full team size list: ' + str(client_board_state.board_state['team_size']))
		print('round: ' + str(client_board_state.board_state['round']))
		print('team size to select: ' + str(client_board_state.board_state['team_size'][client_board_state.board_state['round']-1]))






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

#function for setting the player frames to the correct color and text after game start. Takes in player objects from board state
def playerframetext(player, player_frames, username, user_info):
	display_text = player['name']


	#user_role = client_board_state.board_state['players']

	#print(f'user_info:    {user_info}')
	#print(f'characters.character_dictionary:   {characters.character_dictionary}')


	user_role = characters.character_dictionary[user_info['role']]
	#print(f'TESTING user_role!!!!!!!:   {user_role}\r\n')



	player_role = player['role']
	#player_role = characters.character_dictionary[player['role']]
	#print(f'TESTING player_role!!!!!!!:   {player_role}\r\n')


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