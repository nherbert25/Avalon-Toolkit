import requests
import client
import threading


players = None


my_client = client.Client()






def format_response(weather):
	pass


def get_weather(city):
	pass





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

	#print('before send')
	my_client.send('!USERNAME '+username)
	#print('after send')
	return(username)




def board_state():
	my_client.send('!PLAYERSTATE')




def threaded_server_connection():
  threading.Timer(5.0, threaded_server_connection).start()

  string_players = my_client.send('!PLAYERSTATE')
  players = string_players.split(" ")
  print(f'players: {players}')



username = initial_connect(my_client)
threaded_server_connection()