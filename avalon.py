import logging
import threading
import time

import client_board_state
import client
import main_board_class as board


def main():

    #logging.basicConfig(filename='AVALON.log', level=logging.INFO)
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logging.info('Started')

    # create a socket connection object
    my_client, my_queue, lock = client.main()

    logging.debug('Client loaded successfully.')

    # create a main board GUI object

    #Main_Board = threading.Thread(target = my_client.to_server_queue, args =(board.Main_Page, lock))
    # Main_Board.start()

    time.sleep(1)

    Main_Board = board.Main_Page(lock)

    logging.debug('Main_Board loaded successfully.')

    while Main_Board.running:
        Main_Board.main_loop()

    # disconnect from the server
    disconnect_successful = my_client.send(my_client.DISCONNECT_MESSAGE)
    if disconnect_successful == '!NONE':
        logging.info("Server registered client disconnect.")
        logging.info('Avalon exited gracefully.')

    else:
        logging.info("Server did not respond to disconnect call.")


if __name__ == '__main__':
    main()
