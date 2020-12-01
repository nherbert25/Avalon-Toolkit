players = ['Nate','Frankie', 'Jeff']
roles = []
#players = []
votes = []
mission = []

board_state = {
    'players': [],
    'player_picking_team': '',
    'mission' : [],
    'phase' : 'lobby_phase'
    }





def player_creation(name):
    player = {
    'name': name, 
    'role': '',  #class object?
    'votes': [],
    'on_team': [],
    'made_team': []
    }
    return player


#returns list of strings ['Assassin', 'Morgana']
def create_roles_list(roles_dic):
    roles = []
    for role_name in roles_dic:
        number_of_roles = roles_dic[role_name]
        for i in range(number_of_roles):
            roles.append(role_name)
    return roles


def create_board_state(players, board_state = board_state):

    for player in players:
        my_player = player_creation(player)
        my_player['role'] = roles.pop(0)
        board_state['players'].append(my_player)
    
    board_state['player_picking_team'] = board_state['players'][0]['name']
    return(board_state)


def next_round(board_state):
    for player in board_state['players']:
        player['votes'].append([])
        player['on_team'].append([])
        player['made_team'].append([])



"""
lobby_phase = True
picking_phase = False  #, player_picking_team
voting_phase = False
mission_phase = False
assassination_phase = False
game_over_phase = False
"""

# def game_state(players=players, votes=votes, mission=mission):

#     gamestate = {
#         'players': players,
#         'votes': votes,
#         'mission': mission
#     }
#     return gamestate














player1 = {
'name': 'Frankie', 
'role': 'merlin',  #class object?
'votes': [[1, 1, 0],[0, 1]],
'on_team': [[1, 1, 0],[0, 1]],
'made_team': [[1, 0, 0],[1, 0]]
}

player2 = {
'name': 'Nate', 
'role': 'assassin',  #class object?
'votes': [[1, 1, 0],[0, 1]],
'on_team': [[1, 1, 0],[0, 1]],
'made_team': [[0, 1, 0],[0, 1]]
}

player3 = {
'name': 'Jeff', 
'role': 'morgana',  #class object?
'votes': [[1, 1, 0],[0, 1]],
'on_team': [[1, 1, 0],[0, 1]],
'made_team': [[0, 0, 1],[0, 0]]
}


sample_board_state = {
'players': [player1, player2, player3],
'player_picking_team': 'Nate',
'mission' : [1, 0, 0],
'phase' : 'lobby_phase'
}








def player_state(players=players): 
    #print(f'[player_state function] to return:   {players}')  
    return (players) 





######################################



# players = []



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









'''
def gamestate(players, votes, mission):
    gamestate = {
        'players': players,
        'votes': votes,
        'mission': mission
    }
    return gamestate
'''





# def game_state(players=players, votes=votes, mission=mission):

#     players = [x.encode('utf-8') for x in players]

#     gamestate = {
#         'players': players,
#         'votes': votes,
#         'mission': mission
#     }
#     return gamestate



