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
	GOOD_BLUE_TEXT_COLOR = '#ffffff'
	EVIL_RED = '#cf2121'
	SELECTION_YELLOW = '#39658f'

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

	#background_label.place(x=0, y=0, relwidth=1, relheight=1)


	##############################################################

	def __init__(self, lock):

		self.lock = lock #threading lock object. Commands: lock.acquire(), lock.release()
		self.lock.acquire()

		self.game_phase = 'lobby_phase'
		#self.game_phase = client_board_state.board_state['phase']



		self.root.protocol('WM_DELETE_WINDOW', self.crash_gui)  # root is your root window
		self.main_frame = tk.LabelFrame(self.root)
		self.main_frame.grid(row=0, column=0)

		self.top_frame = tk.LabelFrame(self.main_frame, bg=self.NEUTRAL_BLUE, bd=10, pady=10, padx=5, text="Top Frame")
		self.top_frame.grid(row=0, column=0, sticky='EW')
		#self.top_frame.grid_rowconfigure(0, weight=1)
		#https://stackoverflow.com/questions/45847313/what-does-weight-do-in-tkinter
		self.top_frame.grid_columnconfigure(0, weight=1)
		
		self.player_lobby_widget, player_frames = self.generate_player_lobby_widget(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
		#self.player_lobby_widget.grid(row=0, column=0, sticky='EW')

		self.server_message_frame = self.generate_server_message_frame()



		self.rules_frame = self.generate_rules_config()
		self.lock.release()


	##############################################################
	#functions


	#creates a widget housing a 'player' widget for each player in the lobby
	def generate_player_lobby_widget(self, top_frame, list_of_players):

		config_base_frame = tk.LabelFrame(self.main_frame, bg=self.NEUTRAL_BLUE, bd=10)#, text="Player Frame")
		config_base_frame.grid(row=0, column=0, sticky='EW')
		#config_base_frame.grid_columnconfigure(0, weight=1)

		column_num = 0
		row_num = 0
		player_frames = {}

		#create individual widgets for each player and append to the base widget
		for player in list_of_players:
			config_base_frame.grid_columnconfigure(column_num, weight=1)
			player_frames[player] = tk.LabelFrame(config_base_frame, bg=self.NEUTRAL_BLUE, bd=5, padx=10, pady=10)#, height=2, width=2)#text="player_frame",)
			player_frames[player].grid(row=row_num, column=column_num)#, sticky='EW')
			player_frames[player].grid_columnconfigure(column_num, weight=1)

			player = tk.Label(player_frames[player], font=40, text=player, height=5, width=10)
			player.grid(row=0, column=0, sticky='EW')
			column_num += 1

			if column_num >= 6:
				column_num = 0
				row_num += 1

		return config_base_frame, player_frames





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










	def generate_game_started_player_frame(self, top_frame, board_state, username):

		user_info = []
		for player in client_board_state.board_state['players']:
			if username == player['name']:
				user_info = player

		#print(f'\r\nshould be the logged in persons information...: {user_info}\r\n')
		#print(f'client username:  {client_board_state.username}')
		#print(f'board state in generate_game_started_player_frame method: {board_state}')

		config_base_frame = tk.LabelFrame(self.top_frame, bg=self.NEUTRAL_BLUE, bd=10)#, text="Player Frame")
		config_base_frame.grid(row=1, column=0, sticky='EW')

		count = 0

		#player_name: player frame
		all_player_frames = {}


		for player in board_state['players']:

			player_base_frame = tk.LabelFrame(config_base_frame, bg=self.NEUTRAL_BLUE, bd=5, pady=10)  #text="player_frame"
			player_base_frame.grid(row=0, column=count)

			player_frame = tk.Label(player_base_frame, bg='#39658f', fg='#ffffff', font=('Helvetica', '20'), text=main_board_helper.playerframetext(player, player_base_frame, username, user_info))
			player_frame.grid(row=0, column=0)

			def create_select_player_button(player_frame=player_frame, player_name=player['name']):

				select_player_button = tk.Button(player_base_frame, text='Select!', bg='#0052cc', fg='#ffffff', font=('Helvetica', '8'), command=lambda: main_board_helper.select_player(player_frame, player_name))
				select_player_button.grid(row=3, column=0, pady=5)

				return select_player_button

			select_player_button = create_select_player_button()

			all_player_frames[player['name']] = {'name': player['name'], 'player_base_frame': player_base_frame, 'player_frame': player_frame, 'select_player_button': select_player_button}
			count += 1


		config_base_frame_submit = tk.LabelFrame(self.top_frame, bg=self.NEUTRAL_BLUE, bd=0)#, text="Submit Frame")
		config_base_frame_submit.grid(row=2, column=0)


		submit_button = tk.Button(config_base_frame_submit, text='Submit!', bg='#0052cc', fg='#ffffff', font=('Helvetica', '12'), command=lambda: main_board_helper.submit_team(all_player_frames))
		submit_button.grid(row=0, column=0, pady=(10,10))


		config_base_frame_vote = tk.LabelFrame(self.top_frame, bg=self.NEUTRAL_BLUE, bd=0)#, text="config_base_frame_vote")
		config_base_frame_vote.columnconfigure(0, weight=1)
		config_base_frame_vote.columnconfigure(1, weight=1)
		config_base_frame_vote.grid(row=3, column=0)

		approve_succeed_button = tk.Button(config_base_frame_vote, text='Approve/Succeed', bg='#0052cc', fg='#ffffff', font=('Helvetica', '12'), command=lambda: main_board_helper.approve_succeed_button(all_player_frames))
		approve_succeed_button.grid(row=0, column=0, padx=(0, 20), sticky='nsew')

		reject_fail_button = tk.Button(config_base_frame_vote, text='Reject/Fail', bg='#cf2121', fg='#ffffff', font=('Helvetica', '12'), command=lambda: main_board_helper.reject_fail_button(all_player_frames))
		reject_fail_button.grid(row=0, column=1, padx=(20, 0), sticky='nsew')

		return config_base_frame





	def generate_server_message_frame(self, message_from_server = client_board_state.message_from_server):
		
		#config_base_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=10)#, text="Lower Frame")
		
		config_base_frame = tk.Label(self.main_frame, bg=self.NEUTRAL_BLUE, font=40, bd=10, text=message_from_server, pady=2)
		config_base_frame.grid(row=4, column=0, sticky='nsew')

		return config_base_frame











	def generate_voting_frame(self):
		config_base_frame = tk.LabelFrame(self.main_frame, bg=self.NEUTRAL_BLUE, bd=10)#, text="Voting Frame")
		config_base_frame.grid(row=2, column=0) #, fill=tk.X)


		vcount = 0
		xcount = 1
		for i in range(1,6):
			round_title = tk.Label(config_base_frame, text=f'Round {i}', font=12)
			round_title.grid(row=vcount, column=xcount, columnspan=5)
			xcount += 5


		player_vote_dictionary = {}

		vcount += 1
		xcount = 0

		for player in client_board_state.board_state['player_order']:

			player_name = tk.Label(config_base_frame, text=player, font=12)
			player_name.grid(row=vcount, column=xcount)

			player_vote_dictionary[player] = []

			for i in range(25):

				xcount += 1
				votebox = tk.Label(config_base_frame, text='x', font=12, highlightthickness=1)
				votebox.grid(row=vcount, column=xcount)
				player_vote_dictionary[player].append(votebox)
				

			vcount += 1
			xcount = 0

		#print(player_vote_dictionary)  {'Nate': [widget_object, widget_object, widget_object], 'Frankie': [widget_object, widget_object, widget_object]}
		return config_base_frame, player_vote_dictionary






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
			self.player_lobby_widget, player_frames = self.generate_player_lobby_widget(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
			#self.player_lobby_widget.grid(row=0, column=0, sticky='EW')
			self.player_lobby_widget.grid_rowconfigure(0, weight=1)





		#if game starts, or you reconnect and we're not in the lobby phase, run the following..... delete the rules widget, delete the lobby player widget, update internal board state, generate game board
		if client_board_state.board_state['phase'] != 'lobby_phase' and self.game_phase == 'lobby_phase':
			self.game_phase = client_board_state.board_state['phase']

			#print(self.game_phase)
			#time.sleep(1)
			main_board_helper.game_started(self.rules_frame)

			Main_Page.list_of_players = client_board_state.players
			#Main_Page.board_state = client_board_state.board_state
			self.player_lobby_widget.destroy()
			self.player_lobby_widget = self.generate_game_started_player_frame(top_frame=self.top_frame, board_state=client_board_state.board_state, username=client_board_state.username)

			self.voting_frame, self.player_vote_dictionary = self.generate_voting_frame()


			main_board_helper.update_voter_frame(self.voting_frame, self.player_vote_dictionary, Main_Page.GOOD_BLUE, Main_Page.EVIL_RED)


		#if client_board_state.board_state['phase'] != 'lobby_phase':# and Main_Page.board_state != client_board_state.board_state:
			#print(f'widget list: {Main_Page.list_of_players}\nclient list: {client_board_state.players}')
			#Main_Page.list_of_players = client_board_state.players
			#Main_Page.board_state = client_board_state.board_state

			#print(Main_Page.list_of_players == client_board_state.players)
			#print(client_board_state.board_state['phase'] != 'lobby_phase' and Main_Page.board_state != client_board_state.board_state)


		if client_board_state.board_state['phase'] != self.game_phase:
			self.game_phase = client_board_state.board_state['phase']
			main_board_helper.update_voter_frame(self.voting_frame, self.player_vote_dictionary, Main_Page.GOOD_BLUE, Main_Page.EVIL_RED)




		#print(client_board_state.message_from_server, 'client board state')
		#print(Main_Page.message_from_server)




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






