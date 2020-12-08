import threading
import queue
import time
import requests
import tkinter as tk



import characters
import client_board_state



def create_list_of_characters(character_dic):
	list_of_characters = {}
	for character in character_dic:
		list_of_characters[character] = 0
	return list_of_characters

##list_of_characters = {'Merlin': 0, 'Percival': 0, 'Resistance': 0, 'Morgana': 0, 'Assassin': 0, 'Mordred': 0, 'Oberon': 0, 'Spy': 0}
list_of_characters = create_list_of_characters(characters.character_dictionary)


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





def select_player(player_frame, player_name, player_role, user_board_state_info, username):

	print('You are ' + player_name + ', It is currently ' + client_board_state.board_state['player_picking_team'] + 's turn')
	print(f'Before pressing, these players are selected: {client_board_state.selected_players}')

	if client_board_state.board_state['phase'] != 'picking_phase':
		return None

	#if your turn, you may select players
	if client_board_state.username == client_board_state.board_state['player_picking_team']:

		max_players = client_board_state.board_state['team_size'][client_board_state.board_state['round']-1]


		if player_name in (client_board_state.selected_players):
			client_board_state.selected_players.remove(player_name)
			
			
			
			#XXX SET TO ORIGINAL COLOR, NOT BLUE!

			#player_role = characters.character_dictionary[player['role']]
			#print(f'TESTING player_role!!!!!!!:   {player_role}\r\n')

			#set background to red if evil
			user_role = characters.character_dictionary[user_board_state_info['role']]

			print('userrole', user_role)
			print('\r\n\r\n\r\n\r\n\r\nplaer role', player_role)

			if player_role in user_role[1]:
				bg = '#cf2121'
				player_frame.configure(bg = bg)

			else:
				bg = '#39658f'
				player_frame.configure(bg = bg)

			if player_name == username and user_role[0] == 'evil':
				bg = '#cf2121'
				player_frame.configure(bg = bg)


		elif len(client_board_state.selected_players) < max_players:

			if player_name not in (client_board_state.selected_players):
				client_board_state.selected_players.append(player_name)
				
				
				bg='#ecf719'   #, fg='#ffffff'

				player_frame.configure(bg=bg)

		print(f'After pressing, these players are selected: {client_board_state.selected_players}')



def submit_team(all_player_frames):

	if client_board_state.board_state['phase'] != 'picking_phase':
		return None


	#if active player and # of selected players equals # of players for a team this round
	if client_board_state.username == client_board_state.board_state['player_picking_team'] and len(client_board_state.selected_players) == client_board_state.board_state['team_size'][client_board_state.board_state['round']-1]:
		
		#send a voting command to the server
		print('submitting!')
		client_board_state.client_queue.append(['!TEAMSELECT', client_board_state.selected_players])

		#remove selected players from selected players list
		client_board_state.selected_players = []
		

		#player_base_frame_widget = player_widget_dictionary['player_base_frame_widget']

		#return original color to players
		for dictionary in all_player_frames.values():
			#dictionary['player_base_frame_widget']

			dictionary['player_base_frame_widget'].configure(bg='#39658f')
			#all_player_frames[player]['player_frame'].configure(bg='#39658f')


	else:
		print('It''s either not your turn or something''s wrong!')
		print(f'client user: {client_board_state.username}')
		print('active player: ' + client_board_state.board_state['player_picking_team'])
		print('# of selected players: ' + str(len(client_board_state.selected_players)))
		#print('full team size list: ' + str(client_board_state.board_state['team_size']))
		#print('round: ' + str(client_board_state.board_state['round']))
		print('team size to select: ' + str(client_board_state.board_state['team_size'][client_board_state.board_state['round']-1]))



def approve_succeed_button(all_player_frames=None):

	if client_board_state.board_state['phase'] == 'voting_phase':
		client_board_state.client_queue.append(['!VOTE', client_board_state.username, 'approve'])
		print(client_board_state.client_queue)
		print('approving')

	if client_board_state.board_state['phase'] == 'mission_phase' and client_board_state.username in client_board_state.board_state['team_selected']:
		client_board_state.client_queue.append(['!MISSION', client_board_state.username, 'pass'])
		print('passing')

def reject_fail_button(all_player_frames=None):

	if client_board_state.board_state['phase'] == 'voting_phase':
		client_board_state.client_queue.append(['!VOTE', client_board_state.username, 'reject'])
		print('rejecting')

	if client_board_state.board_state['phase'] == 'mission_phase' and client_board_state.username in client_board_state.board_state['team_selected']:
		client_board_state.client_queue.append(['!MISSION', client_board_state.username, 'fail'])
		print('failing')




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
		print(f'Not enough roles for game to start.')
		client_board_state.message_from_server = 'Not enough roles for game to start.'





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


#function for setting the player frames to the correct color and text after game start. Takes in player objects from board state,
#updates the background of the widget, and returns a string to be displayed
def playerframetext(player, player_base_frame, username, user_info):
	display_text = player['name']


	#user_role = client_board_state.board_state['players']
	# print(f'user_info:    {user_info}')
	# print(f'characters.character_dictionary:   {characters.character_dictionary}')
	# print(f'user role: {characters.character_dictionary[user_info["role"]]}')


	try:
		user_role = characters.character_dictionary[user_info['role']]
		#print(f'TESTING user_role!!!!!!!:   {user_role}\r\n')

		player_role = player['role']
		#player_role = characters.character_dictionary[player['role']]
		#print(f'TESTING player_role!!!!!!!:   {player_role}\r\n')

		#set background to red if evil
		if player_role in user_role[1]:
			bg = '#cf2121'
			player_base_frame.configure(bg = bg)

		else:
			bg = '#39658f'
			player_base_frame.configure(bg = bg)

		if player['name'] == username and user_role[0] == 'evil':
			bg = '#cf2121'
			player_base_frame.configure(bg = bg)

		#if player_role in characters.character_dictionary[player.role.lower()]

		#print(player['name'])
		#print('username: '+username)
		if user_info['role'] == 'Percival' and player_role in user_role[2]:
			display_text += '\r\n'
			display_text += 'Merlin?'

		if user_info['role'] == 'Sister' and player_role in user_role[2]:
			display_text += '\r\n'
			display_text += 'Sister'

		if player['name'] == username:
			display_text += '\r\n'
			display_text += player['role']

		return display_text

	except:
		return "You're not in the game!"



def update_voter_frame(widget_frame, widget_dictionary, approve_color, reject_color, board_state=None):

	if board_state is None:
		board_state = client_board_state.board_state

	#round = board_state['round']
	#turn = board_state['turn']


	#print('TESTING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	# print('client board state', client_board_state.board_state)
	# print('input boardstate', board_state)
	# print(board_state['players'])


	#[['approve', 'reject'], ['approve', 'reject']]
	for player in board_state['players']:

		name = player['name']
		votes = player['votes']
		on_team = player['on_team']
		made_team = player['made_team']

		#print(name, votes, on_team, made_team)
		#'players': [{'name': 'Frankie', 'role': 'Assassin', 'votes': [['approve']], 'on_team': [[]], 'made_team': [[]]},

		round_number = 0
		for round in player['votes']:
			
			vote_number = 0
			for vote in round:

				#config widget color depending on approve/reject
				#config widget text depending if on team or not
				#config widget depending on made team or not
				widget_index = round_number*5+vote_number

				if vote == 'approve':
					widget_dictionary[name][widget_index].configure(bg=approve_color)

				if vote == 'reject':
					widget_dictionary[name][widget_index].configure(bg=reject_color)



				vote_number += 1
			round_number += 1

	pass