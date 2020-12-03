
#username of the player connected to this client instance
username = ''

#roles in the game
roles = []

#selected players for when picking a team
selected_players = []


#players that are in the game
players = ['Nate','Frankie', 'Jeff']
#players = []

#pre-queue list of instructions to be sent to the queue
client_queue = []


#original board state
board_state = {
    'players': [],
    'player_picking_team': '',
    'mission' : [],
    'phase' : 'lobby_phase'
    }


# def player_creation(name):
#     player = {
#     'name': name, 
#     'role': '',  #class object?
#     'votes': [],
#     'on_team': [],
#     'made_team': []
#     }
#     return player



# votes = {
#     'Nate':[[1, 1, 0],[0, 1]],
#     'Frankie':[[1, 1, 0],[0, 1]],
#     'Jeff':[[1, 1, 0],[0, 1]]
#     }

# votes = {}
# mission = [1, 0, 0]  #boolean success/fail
# mission = []
# #game_state = None #votes (calculate who's turn), mission success/fail
# player_picking_team = 'Nate'

# lobby_phase = True
# picking_phase = False, player_picking_team
# voting_phase = False
# mission_phase = False
# assassination_phase = False
# game_over_phase = False





