# {
# 'player_order': ['Frankie', 'cat', 'Jeff', 'Nate'], 
# 'players': [
#     {'name': 'Frankie', 'role': 'Assassin', 'votes': [[]], 'on_team': [[]], 'made_team': [[]]}, 
#     {'name': 'cat', 'role': 'Percival', 'votes': [[]], 'on_team': [[]], 'made_team': [[]]}, 
#     {'name': 'Jeff', 'role': 'Resistance', 'votes': [[]], 'on_team': [[]], 'made_team': [[]]}, 
#     {'name': 'Nate', 'role': 'Merlin', 'votes': [[]], 'on_team': [[]], 'made_team': [[]]}
#     ], 
# 'player_picking_team': 'Frankie', 
# 'mission': [], 
# 'phase': 'picking_phase',
# 'team_size': [2, 3, 2, 3, 3],
# 'round': 1,
# 'turn': 1,
# 'team_selected': ['Nate', 'Jeff']
# }


"""
lobby_phase = True
picking_phase = False  #, player_picking_team
voting_phase = False
mission_phase = False
assassination_phase = False
game_over_phase = False
"""


team_size = {
    1: [2, 3, 2, 3, 3],
    2: [2, 3, 2, 3, 3],
    3: [2, 3, 2, 3, 3],
    4: [2, 3, 2, 3, 3],
    5: [2, 3, 2, 3, 3],
    6: [2, 3, 4, 3, 4],
    7: [2, 3, 3, 4, 4],
    8: [3, 4, 4, 5, 5],
    9: [3, 4, 4, 5, 5],
    10: [3, 4, 4, 5, 5]
}



players = ['Nate','Frankie', 'Jeff']
roles = []
#players = []
votes = []
mission = []




board_state = {
    'player_order': [],
    'players': [],
    'player_picking_team': '',
    'mission' : [],
    'phase' : 'lobby_phase',
    'team_selected': []
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

    board_state['player_order'] = players

    for player in players:
        my_player = player_creation(player)
        my_player['role'] = roles.pop(0)
        board_state['players'].append(my_player)
    
    board_state['player_picking_team'] = board_state['players'][0]['name']
    return(board_state)




def start_game(board_state):

    number_of_players = len(players)

    board_state['team_size'] = team_size[number_of_players]
    board_state['round'] = 0
    board_state['turn'] = 1
    
    next_round(board_state)





def next_round(board_state):
    for player in board_state['players']:
        player['votes'].append([])
        player['on_team'].append([])
        player['made_team'].append([])

    moved_player = board_state['player_order'].pop(0)
    board_state['player_order'].append(moved_player)

    board_state['round'] += 1
    board_state['turn'] = 1

    #score point!!!!


def next_turn(board_state):

    moved_player = board_state['player_order'].pop(0)
    board_state['player_order'].append(moved_player)

    board_state['turn'] += 1

    #if last round force vote!
    if board_state['turn'] == 5:
        pass





#server_board_state.board_state['waiting_on_votes']
#not being used
def check_if_voted(board_state):

    round = board_state['round']
    turn = board_state['turn']

    for player in board_state['players']:
        pass




def calculate_votes(board_state=board_state):

    round = board_state['round']
    turn = board_state['turn']


    for vote in board_state['votes_cast']:

        for player in board_state['players']:

            if player['name'] == vote[0]:
                player['votes'][round-1].append(vote[1])





def calculate_mission_votes(board_state=board_state):

    round = board_state['round']
    turn = board_state['turn']

    number_of_fails = 0

    for vote in board_state['mission_votes_cast']:

        if vote[1] == 'fail':
            number_of_fails += 1

    if number_of_fails > 0:
        board_state['mission'].append('fail')
        return(f'Mission {round} failed with {number_of_fails} fails!')

    else:
        board_state['mission'].append('success')
        return(f'Mission {round} passed!')






def get_list_of_player_names(board_state):
    
    list_of_players = []

    for player in board_state['players']:
        list_of_players.append(player['name'])

    return list_of_players


# 'round': 1,
# 'turn': 1,
# 'team_selected': ['Nate', 'Jeff']



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



