import tkinter as tk
import requests
#import client

#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#https://python-textbok.readthedocs.io/en/latest/Introduction_to_GUI_Programming.html


def main_page():

	def format_response(weather):
		try:
			name = weather['name']
			desc = weather['weather'][0]['description']
			temp = weather['main']['temp']

			final_str = 'City: %s \nConditions: %s \nTemperature (°F): %s' % (name, desc, temp)
		except:
			final_str = 'There was a problem retrieving that information'

		return final_str

	def get_weather(city):
		weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
		url = 'https://api.openweathermap.org/data/2.5/weather'
		params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
		response = requests.get(url, params=params)
		weather = response.json()

		label['text'] = format_response(weather)



	def send_to_client():
		return('test')

	def press_button2():
		print('button2 pressed!!')


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

	button = tk.Button(top_frame, text="Get Weather", font=40, command=lambda: get_weather(entry.get()))
	button.grid(row=0, column=1)


	lower_frame = tk.LabelFrame(main_frame, bg='#80c1ff', bd=10)
	lower_frame.grid(row=1, column=0)

	label = tk.Label(lower_frame)
	label.grid(row=0, column=0)

	button2 = tk.Button(lower_frame, text="Meow", font=40, command=lambda: press_button2())   #command=lambda: client.send("hello!!!")
	button2.grid(row=1, column=1)




	##############################################################
	#finished

	root.mainloop()


##############################################################
##############################################################

if __name__ == "__main__":
	main_page()















