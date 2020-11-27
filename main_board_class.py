import tkinter as tk
import requests
import main_board_helper
import client_board_state

#import client

#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#https://python-textbok.readthedocs.io/en/latest/Introduction_to_GUI_Programming.html


class Main_Page():

	
	running = True
	HEIGHT = 500
	WIDTH = 600

	root = tk.Tk()
	root.title("Avalon")
	

	list_of_players = []
	game_phase = 'picking_phase'
	



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
	#frames

	# main_frame = tk.LabelFrame(root)
	# main_frame.grid(row=0, column=0)

	# top_frame = tk.LabelFrame(main_frame, bg='#80c1ff', bd=5, text="Top Frame")
	# top_frame.grid(row=0, column=0)



	#player_list(self, top_frame=top_frame, list_of_players=['Nate', 'Frankie'])

	def __init__(self):
		self.root.protocol('WM_DELETE_WINDOW', self.crash_gui)  # root is your root window
		self.main_frame = tk.LabelFrame(self.root)
		self.main_frame.grid(row=0, column=0)

		self.top_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=5, text="Top Frame", pady=10, padx=5)
		self.top_frame.grid(row=0, column=0)

		
		
		
		self.player_frame = self.generate_player_list(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
		self.generate_rules_config()
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
		start_game_button = tk.Button(config_base_frame, text='Start!', font=40, command=lambda: main_board_helper.start_game(config_base_frame, main_board_helper.list_of_characters))
		start_game_button.grid(row=3, columnspan=count, pady=5)





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

		if Main_Page.list_of_players != client_board_state.players:
			#print(f'widget list: {Main_Page.list_of_players}\nclient list: {client_board_state.players}')
			Main_Page.list_of_players = client_board_state.players
			self.player_frame = self.generate_player_list(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)

			

		self.root.update_idletasks()
		self.root.update()





if __name__ == "__main__":
	Main_Board = Main_Page()
	while True:
		Main_Board.main_loop()






