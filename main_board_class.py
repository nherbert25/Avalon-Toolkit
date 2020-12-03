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

	root = tk.Tk()
	root.title("Avalon")
	

	list_of_players = []
	#game_phase = 'lobby_phase'

	
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
		self.game_phase = client_board_state.board_state['phase']
		self.lock = lock #threading lock object   lock.release()     lock.acquire()

		self.root.protocol('WM_DELETE_WINDOW', self.crash_gui)  # root is your root window
		self.main_frame = tk.LabelFrame(self.root)
		self.main_frame.grid(row=0, column=0)

		self.top_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=5, text="Top Frame", pady=10, padx=5)
		self.top_frame.grid(row=0, column=0)

		
		
		
		self.player_frame = self.generate_player_list(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)

		#print('TESTING!!!!!!!!!!!\r\n',client_board_state.board_state)
		#time.sleep(3)
		#print('TESTING!!!!!!!!!!!\r\n',client_board_state.board_state)


		lock.acquire()
		#print(f'hello??? {client_board_state.board_state}')
		#print(client_board_state.board_state['phase'])
		#print(lock.locked())
		if client_board_state.board_state['phase'] == 'lobby_phase':
			self.rules_frame = self.generate_rules_config()
		lock.release()
		self.generate_voting_frame()

	##############################################################
	#functions


	def generate_player_list(self, top_frame, list_of_players):

		config_base_frame = tk.LabelFrame(self.top_frame, bg='#80c1ff', bd=10, text="Player Frame")
		config_base_frame.grid(row=1, column=0)

		count = 0
		player_frames = {}


		for player in list_of_players:
			player_frames[player] = tk.LabelFrame(config_base_frame, bg='#80c1ff', bd=5, text="player_frame", pady=10)
			player_frames[player].grid(row=0, column=count)

			player = tk.Label(player_frames[player], font=40, text=player)
			player.grid(row=0, column=0)

			count += 1


		return config_base_frame












	def generate_game_started_player_frame(self, top_frame, board_state, username):

		user_info = []
		for player in client_board_state.board_state['players']:
			if username == player['name']:
				user_info = player

		#print(f'\r\nshould be the logged in persons information...: {user_info}\r\n')
		#print(f'client username:  {client_board_state.username}')
		#print(f'board state in generate_game_started_player_frame method: {board_state}')

		config_base_frame = tk.LabelFrame(self.top_frame, bg='#80c1ff', bd=10, text="Player Frame")
		config_base_frame.grid(row=1, column=0)

		count = 0

		#player_name: player frame
		all_player_frames = {}


		for player in board_state['players']:

			player_base_frame = tk.LabelFrame(config_base_frame, bg='#80c1ff', bd=5, pady=10)  #text="player_frame"
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


		config_base_frame_submit = tk.LabelFrame(self.top_frame, bg='#80c1ff', bd=10, text="Submit Frame")
		config_base_frame_submit.grid(row=2, column=0)


		submit_button = tk.Button(config_base_frame_submit, text='Submit!', bg='#0052cc', fg='#ffffff', font=('Helvetica', '12'), command=lambda: main_board_helper.submit_team(all_player_frames))
		submit_button.grid(row=0, column=0)


		return config_base_frame















	def generate_rules_config(self):

		config_base_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=10, text="Lower Frame")
		config_base_frame.grid(row=1, column=0)

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





	def generate_voting_frame(self):
		config_base_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=10, text="Voting Frame")
		config_base_frame.grid(row=2, column=0)

		for j in range(len(client_board_state.players)):

			count = 0
			for i in range(25):

				votebox = tk.Label(config_base_frame, text='x', font=12)
				votebox.grid(row=j, column=count)

				count += 1






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
		if client_board_state.board_state['phase'] == 'lobby_phase' and Main_Page.list_of_players != client_board_state.players:
			#print(f'widget list: {Main_Page.list_of_players}\nclient list: {client_board_state.players}')
			Main_Page.list_of_players = client_board_state.players
			self.player_frame = self.generate_player_list(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)

		if client_board_state.board_state['phase'] != 'lobby_phase' and self.game_phase == 'lobby_phase':
			self.game_phase == client_board_state.board_state['phase']
			main_board_helper.game_started(self.rules_frame)

		if client_board_state.board_state['phase'] != 'lobby_phase' and Main_Page.board_state != client_board_state.board_state:
			#print(f'widget list: {Main_Page.list_of_players}\nclient list: {client_board_state.players}')
			Main_Page.list_of_players = client_board_state.players
			Main_Page.board_state = client_board_state.board_state

			#print(Main_Page.list_of_players == client_board_state.players)
			#print(client_board_state.board_state['phase'] != 'lobby_phase' and Main_Page.board_state != client_board_state.board_state)

			self.player_frame.destroy()
			self.player_frame = self.generate_game_started_player_frame(top_frame=self.top_frame, board_state=client_board_state.board_state, username=client_board_state.username)
		self.lock.release()
		
		self.root.update_idletasks()
		self.root.update()





if __name__ == "__main__":
	Main_Board = Main_Page(threading.Lock())
	while True:
		Main_Board.main_loop()






