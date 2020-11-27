import threading
import queue
import time
import requests
import client_board_state


list_of_characters = {'Merlin': 0, 'Percival': 0, 'Resistance': 0, 'Morgana': 0, 'Assassin': 0, 'Mordred': 0, 'Oberon': 0, 'Spy': 0}








def char_add(character, characters_widget, list_of_characters=list_of_characters):
	list_of_characters[character] += 1
	characters_widget.config(text=list_of_characters)
	return list_of_characters


def char_remove(character, characters_widget, list_of_characters=list_of_characters):
	if list_of_characters[character] > 0:
		list_of_characters[character] -= 1
		characters_widget.config(text=list_of_characters)
	return list_of_characters

#def board_state():
#	my_client.send('!PLAYERSTATE')



def start_game(widget, list_of_characters):
	#send !GAMESTART to the server


	#add to queue  !GAMESTART

	client_board_state.roles = list_of_characters
	client_board_state.client_queue.append('!GAMESTART')
	print('Starting game!')
	#widget.grid_forget()
	widget.destroy()


def game_started():
	#when receiving !GAMESTART from the server, start the game
	#run  config_base_frame.grid_forget()
	#run  function to create voting widget
	#get list of players from the server/update players to sit in order
	#reveal information to players
	#update game board to show who's turn it is
	pass





'''
import time
def threaded_server_connection_i_dunno():

	threading._start_new_thread( threaded_server_connection, que )

	starttime = time.time()
	while True:
		print("tick")
		#threading.Timer(1.0, threaded_server_connection(que)).start()
		threaded_server_connection(que)
		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
'''
