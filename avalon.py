import logging
import threading
import time

import client_board_state
import client
import main_board_class as board




def main():

    #logging.basicConfig(filename='AVALON.log', level=logging.INFO)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info('Started')




    #create a socket connection object
    my_client, my_queue, lock = client.main()







    logging.debug('Client loaded successfully.')




    #create a main board GUI object

    #Main_Board = threading.Thread(target = my_client.to_server_queue, args =(board.Main_Page, lock))
    #Main_Board.start()


    time.sleep(1)
    
    Main_Board = board.Main_Page(lock)


    logging.debug('Main_Board loaded successfully.')


    while Main_Board.running:
        Main_Board.main_loop()





    #disconnect from the server
    disconnect_successful = my_client.send(my_client.DISCONNECT_MESSAGE)
    if disconnect_successful == '!NONE':
        logging.info("Server registered client disconnect.")
        logging.info('Avalon exited gracefully.')

    else:
        logging.info("Server did not respond to disconnect call.")



if __name__ == '__main__':
    main()



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



