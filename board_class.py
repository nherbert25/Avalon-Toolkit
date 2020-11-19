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

	top_frame = tk.LabelFrame(main_frame, bg='#80c1ff', bd=5)
	top_frame.grid(row=0, column=0)

	entry = tk.Entry(top_frame, font=40)
	entry.grid(row=0, column=0)

	button = tk.Button(top_frame, text="Get Weather", font=40, command=lambda: main_helper.hello())  #command=lambda self: self.get_weather(entry.get()))
	button.grid(row=0, column=1)


	lower_frame = tk.LabelFrame(main_frame, bg='#80c1ff', bd=10)
	lower_frame.grid(row=1, column=0)

	label = tk.Label(lower_frame)
	label.grid(row=0, column=0)


	#button2 = tk.Button(lower_frame, text="Meow", font=40, command=lambda : press_button2())   #command=lambda: client.send("hello!!!")
	button2 = tk.Button(lower_frame, text="Meow", font=40, command=lambda : main_helper.meow())   #command=lambda: client.send("hello!!!")
	button2.grid(row=1, column=1)

	##############################################################
	#functions

	def format_response(self, weather):
		try:
			name = weather['name']
			desc = weather['weather'][0]['description']
			temp = weather['main']['temp']

			final_str = 'City: %s \nConditions: %s \nTemperature (°F): %s' % (name, desc, temp)
		except:
			final_str = 'There was a problem retrieving that information'

		return final_str

	def get_weather(self, city):
		weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
		url = 'https://api.openweathermap.org/data/2.5/weather'
		params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
		response = requests.get(url, params=params)
		weather = response.json()

		self.label['text'] = self.format_response(weather)



	def send_to_client(self):
		return('test')

	def press_button2(self, b):
		if b is None:
			b = self.press_button2_helper()
		print('button2 pressed!!')


	def press_button2_helper(self):
		pass
		return 5


	##############################################################
	#finished

	#root.mainloop()
	def main_loop(self):
		self.root.update_idletasks()
		self.root.update()



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















