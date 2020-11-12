import requests


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
    return('hello')