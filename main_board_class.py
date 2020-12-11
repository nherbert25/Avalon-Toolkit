import tkinter as tk
import requests
import time
import threading

import main_board_helper
import client_board_state
import watcher

#import client

#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#https://python-textbok.readthedocs.io/en/latest/Introduction_to_GUI_Programming.html




Board_state_watcher = watcher.Watcher(client_board_state.board_state)





class Main_Page():

	
	running = True
	HEIGHT = 500
	WIDTH = 600
	
	NEUTRAL_BLUE = '#80c1ff'
	GOOD_BLUE = '#0052cc'
	GOOD_BLUE_TEXT_COLOR = '#ffffff' #white
	EVIL_RED = '#cf2121'
	COOL_BLUE = '#39658f'
	SELECT_YELLOW = '#ecf719'

	root = tk.Tk()
	root.title("Avalon")
	

	list_of_players = []
	#game_phase = 'lobby_phase'
	message_from_server = ''
	
	board_state = {}
	



	##############################################################
	#menubar
	menubar = tk.Menu(root)
	filemenu = tk.Menu(menubar)
	filemenu.add_command(label="Open")
	filemenu.add_command(label="Save")
	filemenu.add_command(label="Exit", command=root.quit)

	menubar.add_cascade(label="File", menu=filemenu)
	root.config(menu=menubar)

	##############################################################
	#canvas/background

	canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
	canvas.grid(row=0, column=0)


	background_image = tk.PhotoImage(file='landscape.png')
	background_label = tk.Label(root, image=background_image)
	background_label.grid(row=0, column=0)

	##############################################################

	def __init__(self, lock):

		self.lock = lock #threading lock object. Commands: lock.acquire(), lock.release()
		self.lock.acquire()

		self.game_phase = 'lobby_phase'
		#self.game_phase = client_board_state.board_state['phase']



		self.root.protocol('WM_DELETE_WINDOW', self.crash_gui)  # root is your root window
		self.main_frame = tk.LabelFrame(self.root, bd=10, bg=self.NEUTRAL_BLUE)
		self.main_frame.grid(row=0, column=0)

		self.player_name_widget = self.generate_player_name_widget(self.main_frame)
		self.player_name_widget.grid(row=0, column=2, sticky='EW')


		self.top_frame = tk.LabelFrame(self.main_frame, bg=self.NEUTRAL_BLUE, bd=5, pady=10, padx=5)#, text="Top Frame")
		self.top_frame.grid(row=0, column=0, sticky='EW')
		#self.top_frame.grid_rowconfigure(0, weight=1)
		#https://stackoverflow.com/questions/45847313/what-does-weight-do-in-tkinter
		#self.top_frame.grid_columnconfigure(0, weight=1)
		
		self.player_lobby_widget, self.player_frame_widget_dictionary = self.generate_player_lobby_widget(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
		#self.player_lobby_widget.grid(row=0, column=0, sticky='EW')

		self.server_message_frame = self.generate_server_message_frame()



		self.rules_frame = self.generate_rules_config()
		self.lock.release()


	##############################################################
	#functions


	#creates a widget housing a 'player' widget for each player in the lobby
	def generate_player_lobby_widget(self, top_frame, list_of_players):

		config_base_frame = tk.LabelFrame(top_frame, bg=self.NEUTRAL_BLUE, bd=1)#, text="Player Frame")
		config_base_frame.grid(row=0, column=0, sticky='EW')
		#config_base_frame.grid_columnconfigure(0, weight=1)

		column_num = 0
		row_num = 0
		player_frame_widget_dictionary = {}

		#create individual widgets for each player and append to the base widget
		for player_name in list_of_players:
			#config_base_frame.grid_columnconfigure(column_num, weight=1)
			#GOOD_BLUE    NEUTRAL_BLUE 
			player_base_frame_widget = tk.LabelFrame(config_base_frame, bg=self.NEUTRAL_BLUE, bd=5, padx=10, pady=10)
			player_base_frame_widget.grid(row=row_num, column=column_num)#, sticky='EW')
			#player_base_frame_widget.grid_columnconfigure(column_num, weight=1)

			player_text_widget = tk.Label(player_base_frame_widget, font=40, text=player_name, height=5, width=10)
			player_text_widget.grid(row=0, column=0, sticky='EW')
			#ZZZ

			player_frame_widget_dictionary[player_name] = {'player_base_frame_widget': player_base_frame_widget, 'player_text_widget': player_text_widget}
			column_num += 1

			if column_num >= 6:
				column_num = 0
				row_num += 1

		#print(f"\r\n\r\n{player_frame_widget_dictionary}\r\n\r\n\r\n")
		return config_base_frame, player_frame_widget_dictionary





	def generate_rules_config(self):

		config_base_frame = tk.LabelFrame(self.main_frame, bg=self.NEUTRAL_BLUE, bd=10)#, text="Rules Frame")
		config_base_frame.grid(row=1, column=0, sticky='EW')

		characters_widget = tk.Label(config_base_frame, font=40, text=main_board_helper.list_of_characters, pady=2)

		count = 0
		for character in main_board_helper.list_of_characters:

			def f_factory(character = character):
				#return character, character is now a *local* variable of f_factory and can't ever change
				add_char_button = tk.Button(config_base_frame, text=character, font=40, command=lambda : main_board_helper.char_add(character, characters_widget))
				add_char_button.grid(row=0, column=count)
				remove_char_button = tk.Button(config_base_frame, text=character, font=40, command=lambda : main_board_helper.char_remove(character, characters_widget))
				remove_char_button.grid(row=1, column=count)

			f_factory()
			count += 1
		
		characters_widget.grid(row=2, columnspan=count)
		start_game_button = tk.Button(config_base_frame, text='Start!', font=40, command=lambda: main_board_helper.start_game(config_base_frame, start_game_button, main_board_helper.list_of_characters))
		start_game_button.grid(row=3, columnspan=count, pady=5)

		return config_base_frame



	def update_player_lobby_widget_to_start_game(self, top_frame, player_frame_widget_dictionary, board_state, username):
	#player_frame_widget_dictionary[player_name] = {'player_base_frame_widget': player_base_frame_widget, 'player_text_widget': player_text_widget}

		user_board_state_info = {}
		for player in board_state['players']:
			if username == player['name']:
				user_board_state_info = player

		# print(f"username: {username}")
		# print(f"user_board_state_info: {user_board_state_info}")
		# print(f"\r\nBroken here:\r\n{player_frame_widget_dictionary}\r\n\r\n\r\n")

		#update all player widgets to match user information
		for player_name, player_widget_dictionary in player_frame_widget_dictionary.items():
			
			player_base_frame_widget = player_widget_dictionary['player_base_frame_widget']
			player_text_widget = player_widget_dictionary['player_text_widget']
			
			for player in board_state['players']:
				if player['name'] == player_name:
					player_board_state_info = player
					player_widget_dictionary['player_board_state_info'] = player_board_state_info
					break
			#player_board_state_info = board_state['players'][player_name]

			if player_name == username:
				client_user = True
			else:
				client_user = False

			#update widget base frame color to good or evil
			player_base_frame_widget.config(bg=main_board_helper.update_player_widget_background_color(player_base_frame_widget, player_board_state_info, username, user_board_state_info, self.COOL_BLUE, self.EVIL_RED))

			#update widget text (currently this updates the base widget color as well, trying to seperate this)
			player_text_widget.configure(text=main_board_helper.playerframetext(player_base_frame_widget, player_board_state_info, username, user_board_state_info))

			#create select button and add to the widget frame
			if 'select_player_button' not in player_frame_widget_dictionary[player_name].keys():

				def create_select_player_button(player_frame=player_base_frame_widget, player_name=player_board_state_info['name'], player_role=player_board_state_info['role']):

					select_player_button = tk.Button(player_base_frame_widget, text='Select!', bg=self.GOOD_BLUE, fg=self.GOOD_BLUE_TEXT_COLOR, font=('Helvetica', '8'), command=lambda: main_board_helper.select_player(player_frame, player_name, player_role, user_board_state_info, username))
					select_player_button.grid(row=3, column=0, pady=5)

					return select_player_button

				select_player_button = create_select_player_button()
				player_frame_widget_dictionary[player_name]['select_player_button'] = select_player_button


		#create Submit frame widget
		config_base_frame_submit = tk.LabelFrame(top_frame, bg=self.NEUTRAL_BLUE, bd=0)#, text="Submit Frame")
		config_base_frame_submit.grid(row=1, column=0)

		submit_button = tk.Button(config_base_frame_submit, text='Submit!', bd=5, bg=self.GOOD_BLUE, fg=self.GOOD_BLUE_TEXT_COLOR, font=('Helvetica', '12'), command=lambda: main_board_helper.submit_team(player_frame_widget_dictionary, username, self.COOL_BLUE, self.EVIL_RED))
		submit_button.grid(row=0, column=0, pady=(10,10))

		#create Vote Buttons frame widget
		config_base_frame_vote = tk.LabelFrame(top_frame, bg=self.NEUTRAL_BLUE, bd=0)#, text="config_base_frame_vote")#, sticky='NSEW')
		config_base_frame_vote.grid(row=2, column=0, sticky='NSEW')
		config_base_frame_vote.columnconfigure(0, weight=1)
		#config_base_frame_vote.rowconfigure(0, weight=1)
		#config_base_frame_vote.rowconfigure(1, weight=1)
		config_base_frame_vote.columnconfigure(1, weight=1)
		#config_base_frame_vote.grid_columnconfigure(0, weight=1)
		#config_base_frame_vote.grid_columnconfigure(1, weight=1)
		#config_base_frame_vote.grid(row=0, column=0, sticky='EW')

		#ZZZ   NEUTRAL_BLUE   GOOD_BLUE
		approve_button_labelframe_widget = tk.LabelFrame(config_base_frame_vote, bg=self.NEUTRAL_BLUE, bd=0)#, text='omg')#, padx=10, pady=10)
		approve_button_labelframe_widget.grid(row=0, column=0, sticky='NSEW')
		approve_button_labelframe_widget.grid_columnconfigure(0, weight=1)

		reject_button_labelframe_widget = tk.LabelFrame(config_base_frame_vote, bg=self.NEUTRAL_BLUE, bd=0)#, text='bruh')#, padx=10, pady=10)
		reject_button_labelframe_widget.grid(row=0, column=1, sticky='NSEW')
		reject_button_labelframe_widget.grid_columnconfigure(1, weight=1)
		#config_base_frame_vote.grid(row=0, column=0, sticky='EW')

		approve_succeed_button = tk.Button(approve_button_labelframe_widget, width= 10, text='Approve\r\nSucceed', bd=5, relief="raised", bg=self.GOOD_BLUE, fg=self.GOOD_BLUE_TEXT_COLOR, font=('Helvetica', '12'), command=lambda: main_board_helper.approve_succeed_button())
		approve_succeed_button.grid(row=0, column=0)#, sticky='nsew') #padx=(0, 20), 
		approve_succeed_button.grid_columnconfigure(0, weight=1)
		#approve_succeed_button.grid(row=0, column=0, sticky='EW')
		#player_text_widget.grid(row=0, column=0, sticky='EW')

		reject_fail_button = tk.Button(reject_button_labelframe_widget, width= 10,text='Reject\r\nFail', bd=5, bg=self.EVIL_RED, fg=self.GOOD_BLUE_TEXT_COLOR, font=('Helvetica', '12'), command=lambda: main_board_helper.reject_fail_button())
		reject_fail_button.grid(row=0, column=1)#, sticky='nsew')#padx=(20, 0), 
		reject_fail_button.grid_columnconfigure(1, weight=1)

		return player_frame_widget_dictionary


	def generate_team_score_widget(self, top_frame, team_size):
		"""team_widget_list = [[team_frame_widget, team_number_text_widget], [team_frame_widget, team_number_text_widget], [team_frame_widget, team_number_text_widget]]
		'team_size': [[3, 4, 4, 5, 5], [False,False,False,True,False]]"""

		team_widget_list = []
		config_base_frame = tk.LabelFrame(top_frame, bg=self.NEUTRAL_BLUE, bd=0, pady=15, padx=5)
		
		column_num = 0
		#team_number = team_size[0]
		#two_fail_bool_list = team_size[1]

		print(team_size)
		for team, two_fail in zip(team_size[0], team_size[1]):

			# config_base_frame.grid_columnconfigure(column_num, weight=1)
			if two_fail:
				team = str(team) + "*"

			team_frame_widget = tk.Label(config_base_frame, bg=self.NEUTRAL_BLUE, bd=5, padx=6, pady=3, relief="raised", text=team, font='Helvetica 18 bold')
			team_frame_widget.grid(row=0, column=column_num)#, sticky='EW')
			team_frame_widget.grid_columnconfigure(column_num, weight=1)

			team_number_text_widget = tk.Label(team_frame_widget, text=team, font='Helvetica 18 bold', bg=self.NEUTRAL_BLUE)#, height=1, width=1)
			#team_number_text_widget.grid(row=0, column=0)#, sticky='EW')


			team_widget_list.append(team_frame_widget)#, team_number_text_widget])
			column_num += 1

		return config_base_frame, team_widget_list


	def update_team_score_widget(self, team_score_widget, team_widget_list, score, GOOD_BLUE, EVIL_RED):
		#score = board_state['mission']

		try:
			for count, widget in enumerate(team_widget_list):
				if score[count] == "success":
					widget.configure(bg = GOOD_BLUE)
				elif score[count] == "fail":
					widget.configure(bg = EVIL_RED)
		except:
			pass



	def generate_server_message_frame(self, message_from_server = client_board_state.message_from_server):
		
		#config_base_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=10)#, text="Lower Frame")
		
		config_base_frame = tk.Label(self.main_frame, bg=self.NEUTRAL_BLUE, font=40, bd=10, text=message_from_server, pady=2)
		config_base_frame.grid(row=4, column=0, sticky='nsew')

		return config_base_frame


	def generate_voting_frame(self):
		config_base_frame = tk.LabelFrame(self.main_frame, bg=self.NEUTRAL_BLUE, bd=0)#, text="Voting Frame")
		config_base_frame.grid(row=2, column=0) #, fill=tk.X)


		vcount = 0
		xcount = 1
		for i in range(1,6):
			round_title = tk.Label(config_base_frame, text=f'Round {i}', font="Helvetica 14 bold italic", bd=1, relief='raised')#, font=12)  bg=self.NEUTRAL_BLUE, 
			round_title.grid(row=vcount, column=xcount, columnspan=5, sticky='ew')
			xcount += 5


		player_vote_dictionary = {}

		vcount += 1
		xcount = 0

		for player in client_board_state.board_state['player_order']:

			#if player=='Frankie':
			player_name = tk.Label(config_base_frame, text=player, font="Helvetica 12 bold", bd=0, bg=self.NEUTRAL_BLUE, relief='raised')
			player_name.grid(row=vcount, column=xcount, sticky='ew')

			player_vote_dictionary[player] = []

			for i in range(25):

				xcount += 1
				votebox = tk.Label(config_base_frame, text="✔", fg="white", font="BOLD 12", relief="solid", bd=3, bg='white')#, borderwidth=2)#,, highlightbackground="#37d3ff", highlightthickness=4)
				
				if (i + 1) % 5 == 0:
					 votebox.config(padx=2)
				votebox.grid(row=vcount, column=xcount)
				if (i + 1) % 5 == 0:
					 votebox.grid(padx=(0, 3))
				player_vote_dictionary[player].append(votebox)
				

			vcount += 1
			xcount = 0

		#print(player_vote_dictionary)  {'Nate': [widget_object, widget_object, widget_object], 'Frankie': [widget_object, widget_object, widget_object]}
		return config_base_frame, player_vote_dictionary

	#creates the player name widget AUTO UPDATES CLIENT USERNAME
	def generate_player_name_widget(self, parent_widget):

		def submit(): 
			client_board_state.username = player_name_entry.get()
			self.forget(config_base_frame)
			#client_board_state.board_state['phase'] = 'lobby_phase'
			self.game_phase = 'lobby_phase'
			main_board_helper.login(client_board_state.username)

		config_base_frame = tk.LabelFrame(parent_widget, bg=self.NEUTRAL_BLUE, bd=10)#, text="Voting Frame")

		text_label = tk.Label(config_base_frame, text = "Please enter username:")
		player_name_entry = tk.Entry(config_base_frame)
		submit_button = tk.Button(config_base_frame, text="submit", command=submit)
		player_name_entry.focus_set()

		player_name_entry.bind('<Return>', submit)

		text_label.grid(row=0, columnspan=2)
		player_name_entry.grid(row=1, column=0)
		submit_button.grid(row=1, column=1)

		return config_base_frame



	def forget(self, widget): 
		"""This will remove the widget from toplevel without deleting it (as opposed to the destroy() method)
		it just becomes invisible and loses its position 
		can be retrieve by calling the grid() method of the widget again"""
		widget.grid_forget()

	def crash_gui(self, root=root):
		Main_Page.running = False
		root.destroy()



















	##############################################################
	#finished

	#root.mainloop()
	def main_loop(self):

		self.lock.acquire()
		#print(f'client username:  {client_board_state.username}')


		#continually update player list in lobby
		if client_board_state.board_state['phase'] == 'lobby_phase' and Main_Page.list_of_players != client_board_state.players:
			#print(f'widget list: {Main_Page.list_of_players}\nclient list: {client_board_state.players}')
			Main_Page.list_of_players = client_board_state.players
			self.player_lobby_widget, self.player_frame_widget_dictionary = self.generate_player_lobby_widget(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
			#self.player_lobby_widget.grid(row=0, column=0, sticky='EW')
			self.player_lobby_widget.grid_rowconfigure(0, weight=1)





		#if game starts, or you reconnect and we're not in the lobby phase, run the following..... delete the rules widget, delete the lobby player widget, update internal board state, generate game board
		# print(client_board_state.board_state['phase'])
		# print(self.game_phase)
		# time.sleep(1)

		if client_board_state.board_state['phase'] != 'lobby_phase' and self.game_phase == 'lobby_phase':
			self.game_phase = client_board_state.board_state['phase']

			main_board_helper.game_started(self.rules_frame)
			Main_Page.list_of_players = client_board_state.players


			#Main_Page.board_state = client_board_state.board_state
			#self.player_lobby_widget.destroy()
			#self.player_lobby_widget = self.generate_game_started_player_frame(top_frame=self.top_frame, board_state=client_board_state.board_state, username=client_board_state.username)


			#update player_lobby_widget to include role information, add approve/reject and select buttons
			self.player_lobby_widget, self.player_frame_widget_dictionary = self.generate_player_lobby_widget(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
			self.player_frame_widget_dictionary = self.update_player_lobby_widget_to_start_game(top_frame=self.top_frame, player_frame_widget_dictionary=self.player_frame_widget_dictionary, board_state=client_board_state.board_state, username=client_board_state.username)

			#create and update team score frame
			self.team_score_widget, self.team_widget_list = self.generate_team_score_widget(self.top_frame, client_board_state.board_state['team_size'])
			self.update_team_score_widget(self.team_score_widget, self.team_widget_list, client_board_state.board_state['mission'], self.GOOD_BLUE, self.EVIL_RED)
			self.team_score_widget.grid(row=3, column=0)
			# 	self.team_score_widget.columnconfigure(count, weight=1)


			#create and update voter frame
			self.voting_frame, self.player_vote_dictionary = self.generate_voting_frame()
			main_board_helper.update_voter_frame(self.voting_frame, self.player_vote_dictionary, Main_Page.GOOD_BLUE, Main_Page.EVIL_RED)



		#when phase of game changes update board state
		if client_board_state.board_state['phase'] != self.game_phase:
			self.game_phase = client_board_state.board_state['phase']
			main_board_helper.update_voter_frame(self.voting_frame, self.player_vote_dictionary, Main_Page.GOOD_BLUE, Main_Page.EVIL_RED)
			self.update_team_score_widget(self.team_score_widget, self.team_widget_list, client_board_state.board_state['mission'], self.GOOD_BLUE, self.EVIL_RED)




		#display message from server
		if client_board_state.message_from_server != Main_Page.message_from_server:
			Main_Page.message_from_server = client_board_state.message_from_server
			self.server_message_frame.configure(text=Main_Page.message_from_server)



		#	self.player_lobby_widget.destroy()
		#	self.player_lobby_widget = self.generate_game_started_player_frame(top_frame=self.top_frame, board_state=client_board_state.board_state, username=client_board_state.username)






		self.lock.release()
		self.root.update_idletasks()
		self.root.update()










#################################################################


if __name__ == "__main__":
	Main_Board = Main_Page(threading.Lock())
	while True:
		Main_Board.main_loop()






