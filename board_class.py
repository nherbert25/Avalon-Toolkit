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

	main_frame = tk.LabelFrame(root)
	main_frame.grid(row=0, column=0)

	top_frame = tk.LabelFrame(main_frame, bg='#80c1ff', bd=5, text="Top Frame")
	top_frame.grid(row=0, column=0)

	entry = tk.Entry(top_frame, font=40)
	entry.grid(row=0, column=0)

	button = tk.Button(top_frame, text="Get Weather", font=40, command=lambda: main_helper.hello())  #command=lambda self: self.get_weather(entry.get()))
	button.grid(row=0, column=1)


	#player_one = tk.LabelFrame(top_frame, text="Group", font=40, width=300, height=30)
	#player_one.grid(row=1, column=0)





	#player_one_frame = tk.LabelFrame(top_frame, bg='#80c1ff', bd=5, text="player_frame")
	#player_one_frame.grid(row=1, column=0)

	#player_one = tk.Message(player_one_frame, font=40, text="player one")
	#player_one.grid(row=0, column=0)


	#player_two_frame = tk.LabelFrame(top_frame, bg='#80c1ff', bd=5, text="player_frame")
	#player_two_frame.grid(row=1, column=1)

	#player_two = tk.Message(player_two_frame, font=40, text=main_helper.username)
	#player_two.grid(row=0, column=0)






	#player_list(self, top_frame=top_frame, list_of_players=['Nate', 'Frankie'])

	def __init__(self):
		#self.player_list(top_frame=self.top_frame, list_of_players=['Nate', 'Frankie'])
		#self.player_list(top_frame=self.top_frame, list_of_players=['Nate', 'Dog', 'cat', 'taylor'])
		pass





	lower_frame = tk.LabelFrame(main_frame, bg='#80c1ff', bd=10, text="Bottom Frame")
	lower_frame.grid(row=1, column=0)

	label = tk.Label(lower_frame)
	label.grid(row=0, column=0)


	#button2 = tk.Button(lower_frame, text="Meow", font=40, command=lambda : press_button2())   #command=lambda: client.send("hello!!!")
	button2 = tk.Button(lower_frame, text="Meow", font=40, command=lambda : main_helper.meow())   #command=lambda: client.send("hello!!!")
	button2.grid(row=1, column=1)

	##############################################################
	#functions


	def send_to_client(self):
		return('test')

	def press_button2(self, b):
		if b is None:
			b = self.press_button2_helper()
		print('button2 pressed!!')


	def press_button2_helper(self):
		pass
		return 5




	def player_list(self, top_frame, list_of_players):
		
		count = 0
		player_frames = {}

		for player in list_of_players:
			player_frames[player] = tk.LabelFrame(top_frame, bg='#80c1ff', bd=5, text="player_frame")
			player_frames[player].grid(row=0, column=count)

			player = tk.Message(player_frames[player], font=40, text=player)
			player.grid(row=0, column=0)

			count += 1




	##############################################################
	#finished

	#root.mainloop()
	def main_loop(self):

		if Main_Page.list_of_players != main_helper.players:
			Main_Page.list_of_players = main_helper.players
			self.player_list(top_frame=self.top_frame, list_of_players=Main_Page.list_of_players)
			print('finished updating???')
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








