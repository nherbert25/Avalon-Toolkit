import requests
import client


my_client = client.Client()






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


	#self.label['text'] = self.format_response(weather)


def hello():
	print('hellow world!!')
	my_client.send('testing hello message')
	return('hello')

def button2():
    pass


def meow():
	print('pressed meow button')






def initial_connect(my_client):
	username = input('Enter your name: ')
	print('!USERNAME',username)
	my_client.send('!USERNAME '+username)
	return(username)



username = initial_connect(my_client)