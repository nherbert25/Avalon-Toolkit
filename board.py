import tkinter as tk
import requests
import client

def main_page():
	HEIGHT = 500
	WIDTH = 600

	def test_function(entry):
		print("This is the entry:", entry)

	# api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
	# a4aa5e3d83ffefaba8c00284de6ef7c3

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



	root = tk.Tk()
	root.title("Avalon")

	canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
	canvas.grid(row=0, column=0)


	background_image = tk.PhotoImage(file='landscape.png')

	background_label = tk.Label(root, image=background_image)
	background_label.grid(row=0, column=0)


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

	button2 = tk.Button(lower_frame, text="Meow", font=40, command=lambda: client.send("hello!!!"))
	button2.grid(row=1, column=1)


	root.mainloop()



main_page()















