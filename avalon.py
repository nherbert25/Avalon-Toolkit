import logging
import client
import board_class as board


running = True

#logging.basicConfig(filename='AVALON.log', level=logging.INFO)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info('Started')




#create a socket connection object
#my_client = client.Client()


#create a main board GUI object
#board.main_page()
Main_Board = board.Main_Page()

logging.debug('Main_Board loaded successfully.')



while running:
    Main_Board.main_loop()











#disconnect from the server
#my_client.send(my_client.DISCONNECT_MESSAGE)


logging.info('Avalon exited gracefully.')



#check user input yes/no
#check received stuff from server yes/no




#polling driven
#I'm doing my own thing, OS, you keep track of stuff, every once in a while I'll ask you, 'hey, did a thing happen?'



#nonblocking asencrunus networking (IO)
#I'm expecting I might receive data from the server. If I do, please put it in this variable.
#then go into UI and check if there is user input or not
#have I received infromation from the server?
#if the answer is no, then loop otherwise update.
#sleep 10 miliseconds



#interupt driven
#wake me up when an event happens, otherwise I'm going to sleep. 




#headers:
#the first int is how long the message is
#example, the first message is a string with a new line character at the end. It's a # with how many characters are after this
#the second message is the actual message


#'stop code' is the second way to handle this
#keep fetching until I get the keyboard ex: "!stop"



