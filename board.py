import tkinter as tk
import requests

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
#canvas.pack()
canvas.grid(row=0, column=0)


background_image = tk.PhotoImage(file='landscape.png')

background_label = tk.Label(root, image=background_image)
#background_label = tk.Label(root)


#background_label.place(relwidth=1, relheight=1)
background_label.grid(row=0, column=0)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
#frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
frame.grid(row=0, column=0)


entry = tk.Entry(frame, font=40)
#entry.place(relwidth=0.65, relheight=1)
entry.grid(row=0, column=0)

button = tk.Button(frame, text="Get Weather", font=40, command=lambda: get_weather(entry.get()))
#button.place(relx=0.7, relheight=1, relwidth=0.3)
button.grid(row=1, column=1)


lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
#lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
lower_frame.grid(row=1, column=0)


label = tk.Label(frame)
#label.place(relwidth=1, relheight=1)
lower_frame.grid(row=3, column=0)


lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
#lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
lower_frame.grid(row=1, column=0)

root.mainloop()