import tkinter as tk
import requests
import main_helper


#import client

#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#https://python-textbok.readthedocs.io/en/latest/Introduction_to_GUI_Programming.html


class Main_Page():

	HEIGHT = 500
	WIDTH = 600

	root = tk.Tk()
	root.title("Avalon")


	list_of_players = None


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
		self.main_frame = tk.LabelFrame(self.root)
		self.main_frame.grid(row=0, column=0)

		self.top_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=5, text="Top Frame")
		self.top_frame.grid(row=0, column=0)


		self.lower_frame = tk.LabelFrame(self.main_frame, bg='#80c1ff', bd=10, text="Lower Frame")
		self.lower_frame.grid(row=1, column=0)

		self.button2 = tk.Button(self.lower_frame, text="Meow", font=40, command=lambda : main_helper.meow())   #command=lambda: client.send("hello!!!")
		self.button2.grid(row=1, column=1)


		self.generate_rules_config(self.lower_frame)

	##############################################################
	#functions


	def generate_player_list(self, top_frame, list_of_players):
		
		count = 0
		player_frames = {}

		for player in list_of_players:
			player_frames[player] = tk.LabelFrame(top_frame, bg='#80c1ff', bd=5, text="player_frame")
			player_frames[player].grid(row=0, column=count)

			player = tk.Message(player_frames[player], font=40, text=player)
			player.grid(row=0, column=0)

			count += 1


	# def generate_rules_config(self, lower_frame):
	# 	pass



	def generate_rules_config(self, lower_frame):

		characters_widget = tk.Label(lower_frame, font=40, text=main_helper.list_of_characters)

		count = 0
		for character in main_helper.list_of_characters:

			def f_factory(character = character):
				#return character # i is now a *local* variable of f_factory and can't ever change

				button = tk.Button(lower_frame, text=character, font=40, command=lambda : main_helper.char_add(character, characters_widget))
				button.grid(row=0, column=count)
				button2 = tk.Button(lower_frame, text=character, font=40, command=lambda : main_helper.char_remove(character, characters_widget))
				button2.grid(row=1, column=count)

				
			f_factory()
			count += 1
		
		characters_widget.grid(row=2, columnspan=count)




	##############################################################
	#finished

	#root.mainloop()
	def main_loop(self):

		if Main_Page.list_of_players != main_helper.players:
			Main_Page.list_of_players = main_helper.players
			self.generate_player_list(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
			#print('finished updating???')
		self.root.update_idletasks()
		self.root.update()
		#print('finished updating222222???')



'''
	def close_window(self):
		global running
		running = False  # turn off while loop
		#print( "Window closed")

	#root = Tk()
#	root.protocol("WM_DELETE_WINDOW", close_window)


	print("module board_class loaded successfully.")




	def on_closing(self, root=root):
		if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
			root.destroy()

	root.protocol("WM_DELETE_WINDOW", on_closing)
'''

#main_page = Main_Page()



if __name__ == "__main__":
	Main_Board = Main_Page()
	while True:
		Main_Board.main_loop()






'''
	player_one = tk.Text(player_frame, font=40, width=40, height=30)
	player_one.grid(row=0, column=0)
	player_one.insert(tk.END, "playername")
'''








