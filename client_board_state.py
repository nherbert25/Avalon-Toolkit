
USERNAME = 'Nate'
USERNAME = input('Enter your name: ')



#username of the player connected to this client instance
username = ''

#roles in the game
roles = []

#selected players for when picking a team
selected_players = []

#players that are in the game
players = []

#pre-queue list of instructions to be sent to the queue
client_queue = []

#pre-queue list of instructions to be sent to the queue
message_from_server = 'Waiting on game to start. Select roles for the game and press "Start!".'#\r\nIf there are more roles than players, roles will be selected randomly from the list.'


#original board state
board_state = {
    'players': [],
    'player_picking_team': '',
    'mission' : [],
    'phase' : 'lobby_phase'
    }



board_state = {
    'player_order': [],
    'players': [],
    'player_picking_team': '',
    'mission' : [],
    'phase' : 'lobby_phase',
    'team_selected': [],
    'team_size': [],
    'round': 0,
    'turn': 0,
    'team_selected': []
    }



"""
lobby_phase = True
picking_phase = False  #, player_picking_team
voting_phase = False
mission_phase = False
assassination_phase = False
game_over_phase = False
"""


#TESTING CONFIG OPTIONS
players = ['Nate','Frankie', 'Jeff']
players.append(USERNAME)

