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


def login(username):
	client_board_state.client_queue.append(['!INITIAL_CONNECT', username])



def select_player(player_frame, player_name, player_role, user_board_state_info, username):

	print('You are ' + username + ', It is currently ' + client_board_state.board_state['player_picking_team'] + 's turn')
	print(f'Before pressing, these players are selected: {client_board_state.selected_players}')

	if client_board_state.board_state['phase'] != 'picking_phase' or username == '':
		return None

	#if your turn, you may select players
	if client_board_state.username == client_board_state.board_state['player_picking_team']:

		max_players = client_board_state.board_state['team_size'][0][client_board_state.board_state['round']-1]

		if player_name in (client_board_state.selected_players):
			client_board_state.selected_players.remove(player_name)
			
			#set background to red if evil
			user_role = characters.character_dictionary[user_board_state_info['role']]

			#print('userrole', user_role)
			#print('\r\n\r\n\r\n\r\n\r\nplaer role', player_role)

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



def submit_team(all_player_frames, username, COOL_BLUE, EVIL_RED):

	if client_board_state.board_state['phase'] != 'picking_phase' or username == '':
		return None

	#if active player and # of selected players equals # of players for a team this round
	if client_board_state.username == client_board_state.board_state['player_picking_team'] and len(client_board_state.selected_players) == client_board_state.board_state['team_size'][0][client_board_state.board_state['round']-1]:
		
		#send a voting command to the server
		client_board_state.client_queue.append(['!TEAMSELECT', client_board_state.selected_players])

		#remove selected players from selected players list
		client_board_state.selected_players = []

		#return original color to players
		#XXXX CURRENTLY SETTING EVERYONE TO BLUE!!!! SHOULD PUT BACK ORIGINAL COLOR
		user_board_state_info = all_player_frames[username]['player_board_state_info']

		for dictionary in all_player_frames.values():
			#dictionary['player_base_frame_widget'].configure(bg='#39658f')

			dictionary['player_base_frame_widget'].configure(bg=update_player_widget_background_color(dictionary['player_base_frame_widget'], dictionary['player_board_state_info'], username, user_board_state_info, COOL_BLUE, EVIL_RED))

		return all_player_frames
			#player_base_frame_widget.config(bg=main_board_helper.update_player_widget_background_color(player_base_frame_widget, player_board_state_info, username, user_board_state_info, self.COOL_BLUE, self.EVIL_RED))

#def update_player_widget_background_color(player_base_frame, player_info, username, user_info, GOOD_BLUE, EVIL_RED):




#ALL PLAYER INFORMATION FOR WIDGET     XXXX player_widget_dictionary['player_board_state_info']

	else:
		print('It''s either not your turn or something''s wrong!')
		print(f'client user: {client_board_state.username}')
		print('active player: ' + client_board_state.board_state['player_picking_team'])
		print('# of selected players: ' + str(len(client_board_state.selected_players)))
		#print('full team size list: ' + str(client_board_state.board_state['team_size']))
		#print('round: ' + str(client_board_state.board_state['round']))
		print('team size to select: ' + str(client_board_state.board_state['team_size'][0][client_board_state.board_state['round']-1]))

	return all_player_frames

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
	"""when receiving !GAMESTART from the server, start the game
	run  config_base_frame.grid_forget()
	run  function to create voting widget
	get list of players from the server/update players to sit in order
	reveal information to players
	update game board to show who's turn it is"""
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


def update_player_widget_background_color(player_base_frame, player_info, username, user_info, GOOD_BLUE, EVIL_RED):
	try:

		user_role = characters.character_dictionary[user_info['role']]
		player_role = player_info['role']

		#print(f'TESTING user_role!!!!!!!:   {user_role}\r\n')
		#player_role = characters.character_dictionary[player['role']]
		#print(f'TESTING player_role!!!!!!!:   {player_role}\r\n')


		#set background to red if player is known evil to you or if this is you and you are evil
		if player_role in user_role[1] or (player_info['name'] == username and user_role[0] == 'evil'):
			bg = EVIL_RED
			player_base_frame.configure(bg = bg)

		else:
			bg = GOOD_BLUE
			player_base_frame.configure(bg = bg)

		# #This is you. Even if your character doesn't see this character, you know YOU. (Oberon)
		# if player_info['name'] == username and user_role[0] == 'evil':
		# 	bg = EVIL_RED
		# 	player_base_frame.configure(bg = bg)
		return bg

	except:
		print("Something went wrong in update_player_widget_background_color.")
		bg = GOOD_BLUE
		return bg


#function for setting the player frames to the correct color and text after game start. Takes in player objects from board state,
#updates the background of the widget, and returns a string to be displayed
def playerframetext(player_base_frame, player_info, username, user_info):
	display_text = player_info['name']


	#user_role = client_board_state.board_state['players']
	# print(f'user_info:    {user_info}')
	# print(f'characters.character_dictionary:   {characters.character_dictionary}')
	# print(f'user role: {characters.character_dictionary[user_info["role"]]}')

	try:
		user_role = characters.character_dictionary[user_info['role']]
		#print(f'TESTING user_role!!!!!!!:   {user_role}\r\n')

		player_role = player_info['role']
		#player_role = characters.character_dictionary[player['role']]
		#print(f'TESTING player_role!!!!!!!:   {player_role}\r\n')

		#Percival Text
		if user_info['role'] == 'Percival' and player_role in user_role[2]:
			display_text += '\r\n'
			display_text += 'Merlin?'

		#Sister Text (omit self from being known)
		if user_info['role'] == 'Sister' and player_info['name'] != username and player_role in user_role[2]:
			display_text += '\r\n'
			display_text += 'Sister'

		#Display your own role
		if player_info['name'] == username:
			display_text += '\r\n'
			display_text += player_info['role']

		return display_text

	except:
		return display_text



def update_voter_frame(widget_frame, widget_dictionary, approve_color, reject_color, board_state=None):


	#U+2714
	#From the list of unicodes, replace “+” with “000”. For example – “U+1F600” will become “U0001F600” and prefix the unicode with “\” and print it.
	#check_mark_unicode = r"\U0002714"


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
		votes = player['votes']  #'votes': [['reject', 'reject', 'approve'], ['approve'], ['approve']]
		on_team = player['on_team']  #'on_team': [[True, True, True], [True], [True]]
		made_team = player['made_team']  #'made_team': [[False, True, False], [False], [True]]

		print(f"{votes}, {on_team}, {made_team}")

		for round, (vote_round_list, on_team_bool_round_list, made_team_bool_round_list) in enumerate(zip(votes, on_team, made_team)):

			for turn, (vote, on_team_bool, made_team_bool) in enumerate(zip(vote_round_list, on_team_bool_round_list, made_team_bool_round_list)):

				print(round, turn, vote, on_team_bool, made_team_bool)

			# for vote in round:
				widget_index = round*5+turn
				
				#config widget border depending on made team or not
				if made_team_bool:
					widget_dictionary[name][widget_index].configure(bd=3)

				#config widget color depending on approve/reject
				if vote == 'approve':
					widget_dictionary[name][widget_index].configure(bg=approve_color, fg=approve_color)
				if vote == 'reject':
					widget_dictionary[name][widget_index].configure(bg=reject_color, fg=reject_color)

				#config widget text depending if on team or not
				if on_team_bool:
					widget_dictionary[name][widget_index].configure(text="✔", fg="white", font="BOLD 12")


	pass