import requests
import client
import threading
import queue
import time



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




#def board_state():
#	my_client.send('!PLAYERSTATE')






'''
#https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
def threaded_server_connection():
  threading.Timer(1.0, threaded_server_connection).start()

  string_players = my_client.send('!PLAYERSTATE')
  players = string_players.split(" ")
  print(f'players: {players}')
'''




'''
from threading import Timer

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer	 = None
		self.interval   = interval
		self.function   = function
		self.args	   = args
		self.kwargs	 = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False


from time import sleep



def hello2(name):
	print("Hello %s!" % name)

print("starting...")
rt = RepeatedTimer(1, hello2, "World") # it auto-starts, no need of rt.start()
try:
	sleep(5) # your long-running job goes here...
finally:
	rt.stop() # better in a try/finally block to make sure the program ends!
'''

'''
def threaded_server_connection(que):

	print('starting threaded server')
	#threading.Timer(1.0, threaded_server_connection(que)).start()

	string_players = my_client.send('!PLAYERSTATE')
	players = string_players.split(" ")
	print(f'players: {players}')
	que.put(players)
'''


username = initial_connect(my_client)
players = username
#que = queue.Queue()
#threaded_server_connection(que)


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


def board_state():

	print('starting threaded server')
	#threading.Timer(1.0, threaded_server_connection(que)).start()

	string_players = my_client.send('!PLAYERSTATE')
	players = string_players.split(" ")
	print(f'players: {players}')
	return(players)


# A thread that produces data 
def producer(out_q): 
	while True: 
		# Produce some data 

		out_q.put(board_state())
		time.sleep(5)
		  
# A thread that consumes data 
def consumer(in_q):
	global players
	while True: 
		# Get some data 
		data = in_q.get() 
		# Process the data 
		print(data)
		players = data
		time.sleep(5)

		  
# Create the shared queue and launch both threads 
q = queue.Queue() 
t1 = threading.Thread(target = consumer, args =(q, )) 
t2 = threading.Thread(target = producer, args =(q, )) 
t1.start()
t2.start()