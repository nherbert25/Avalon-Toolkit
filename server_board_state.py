
# [{'phase': 'picking_phase',
# 'player_order': ['Jeff', 'cat', 'Frankie', 'Nate'],
#
# 'players': [
#  {'name': 'Frankie', 'role': 'Assassin', 'votes': [['approve'], []], 'on_team': [[], []],'made_team': [[], []]},
#  {'name': 'Nate', 'role': 'Morgana', 'votes': [['approve'], []], 'on_team': [[], []], 'made_team': [[], []]},
# {'name': 'Jeff', 'role': 'Resistance', 'votes': [['approve'], []], 'on_team': [[], []], 'made_team': [[], []]},
# {'name': 'cat', 'role': 'Mordred', 'votes': [['approve'], []], 'on_team': [[], []], 'made_team': [[], []]}],

#    'player_picking_team': 'Jeff',
#    'mission': ['success'],
#    'team_size': [2, 3, 2, 3, 3],
#    'round': 2, 'turn': 1, 'team_selected': [], 'waiting_on_votes': [], 'votes_cast': [],
#       'mission_votes_cast': [['Jeff', 'approve'], ['Nate', 'approve']]},
#        ['Jeff', 'cat', 'Frankie', 'Nate'], 'Waiting on Jeff to pick a team.']]


"""
lobby_phase = True
picking_phase = False  #, player_picking_team
voting_phase = False
mission_phase = False
assassination_phase = False
game_over_phase = False
"""


team_size = {
    1: [[1, 1, 1, 1, 1], [False, False, False, False, False]],
    2: [[1, 2, 1, 2, 1], [False, True, False, True, False]],
    3: [[2, 3, 2, 3, 3], [False, False, False, False, False]],
    4: [[2, 3, 2, 3, 3], [False, False, False, False, False]],
    5: [[2, 3, 2, 3, 3], [False, False, False, False, False]],
    6: [[2, 3, 4, 3, 4], [False, False, False, False, False]],
    7: [[2, 3, 3, 4, 4], [False, False, False, True, False]],
    8: [[3, 4, 4, 5, 5], [False, False, False, True, False]],
    9: [[3, 4, 4, 5, 5], [False, False, False, True, False]],
    10: [[3, 4, 4, 5, 5], [False, False, False, True, False]],
    11: [[3, 4, 4, 5, 5], [False, False, False, True, False]],
    12: [[4, 4, 5, 6, 6], [False, False, False, True, False]],
    13: [[3, 4, 4, 5, 5], [False, False, False, True, False]],
    14: [[3, 4, 4, 5, 5], [False, False, False, True, False]]
}


roles = []
players = []
votes = []
mission = []


board_state = {
    'phase': 'lobby_phase',
    'player_order': [],
    'players': [],
    'player_picking_team': '',
    'mission': [],
    'number_of_mission_fails': [],
    'team_size': [],
    'round': 0,
    'turn': 0,
    'score': [],
    'team_selected': [],
    'votes_cast': [],
    'mission_votes_cast': []
}


# xxx take in the initial connect and create this if doesn't exist?
def player_creation(name):
    player = {
        'name': name,
        'role': '',  # class object?
        'votes': [],
        'on_team': [],
        'made_team': []
    }
    return player


# returns list of strings ['Assassin', 'Morgana']
def create_roles_list(roles_dic):
    roles = []
    for role_name in roles_dic:
        number_of_roles = roles_dic[role_name]
        for i in range(number_of_roles):
            roles.append(role_name)
    return roles


# XXX REMOVE DEFAULT
# xxx remove player_creation from game start
def create_board_state(players, board_state):

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


def next_turn(board_state):
    print('running next_turn_funciton')
    print(f"board_state['player_order']: {board_state['player_order']}")
    moved_player = board_state['player_order'].pop(0)
    board_state['player_order'].append(moved_player)
    board_state['player_picking_team'] = board_state['player_order'][0]

    board_state['turn'] += 1

    # if last round force vote!
    # XXX
    if board_state['turn'] == 5:
        pass

    return board_state


def next_round(board_state):
    for player in board_state['players']:
        player['votes'].append([])
        player['on_team'].append([])
        player['made_team'].append([])

    board_state = next_turn(board_state)

    board_state['round'] += 1
    board_state['turn'] = 1

    return board_state

    # score point!!!!


# #server_board_state.board_state['waiting_on_votes']
# #not being used
# def check_if_voted(board_state):

#     round = board_state['round']
#     turn = board_state['turn']

#     for player in board_state['players']:
#         pass


# XXX REMOVE DEFAULT
# calculate if vote passes or fails
# append queued votes to player
# sets board_state['votes_cast'] to empty list
def calculate_votes(board_state):

    round = board_state['round']
    turn = board_state['turn']

    approve_count = 0
    reject_count = 0

    #vote = ['Nate', 'reject']
    for vote in board_state['votes_cast']:
        for player in board_state['players']:

            if player['name'] == vote[0]:
                player['votes'][round-1].append(vote[1])

    # calculate if we go to next round or not
    for vote in board_state['votes_cast']:
        if vote[1] == 'approve':
            approve_count += 1
        elif vote[1] == 'reject':
            reject_count += 1

    board_state['votes_cast'] = []

    if approve_count > reject_count:
        # go to next phase
        board_state['phase'] = 'mission_phase'
        to_return = 'approved'

    else:
        # go to next team selection
        board_state['phase'] = 'picking_phase'
        board_state['team_selected'] = []
        board_state = next_turn(board_state)
        to_return = 'rejected'

    return board_state, f'Calculated votes! Team {to_return}.'


# XXX REMOVE DEFAULT
# appends success/failure to board_state['mission'], calculates and changes phase to next round or assassination phase. Runs next_round() if applicable. Returns a string meant for players ('Mission {round} failed with {number_of_fails} fail(s)!')
def calculate_mission_votes(board_state):

    round = board_state['round']
    turn = board_state['turn']
    team_size = board_state['team_size']
    # boolean, 'requires 2 fails to fail mission?'
    number_of_fails_to_fail_mission = team_size[1]

    number_of_fails = 0

    #vote = ['Nate', 'fail']
    for vote in board_state['mission_votes_cast']:
        if vote[1] == 'fail':
            number_of_fails += 1

    # if two or more fails, fail mission
    if number_of_fails >= 2:
        board_state['mission'].append('fail')
        to_return = f'Mission {round} failed with {number_of_fails} fails!'

    # if it's not a mission that requires 2+ fails, fail mission
    elif number_of_fails >= 1 and not number_of_fails_to_fail_mission[round-1]:
        board_state['mission'].append('fail')
        to_return = f'Mission {round} failed with {number_of_fails} fail!'

    else:
        board_state['mission'].append('success')
        to_return = f'Mission {round} passed!'

    board_state['number_of_mission_fails'].append(number_of_fails)
    board_state['phase'] = 'picking_phase'
    # if 3 success or 3 failure, change game state, game over
    success_count = 0
    fail_count = 0

    for i in board_state['mission']:
        if i == 'success':
            success_count += 1
            if success_count >= 3:
                board_state['phase'] = 'assassination_phase'

        if i == 'fail':
            fail_count += 1
            if fail_count >= 3:
                board_state['phase'] = 'game_over_phase'

    if board_state['phase'] == 'picking_phase':
        board_state = next_round(board_state)

    return board_state, to_return


def get_list_of_player_names(board_state):

    list_of_players = []

    for player in board_state['players']:
        list_of_players.append(player['name'])

    return list_of_players


def message_to_client(board_state):

    message = ''

    if board_state['phase'] == 'picking_phase':
        message = f'Waiting on {board_state["player_picking_team"]} to pick a team.'

        # if the last team failed append number of fails to message
        if board_state['number_of_mission_fails'] != []:

            # if number of fails from last round >= 2, mission failed
            if board_state['number_of_mission_fails'][board_state['round']-2] >= 2:
                message += f"\r\nMission {board_state['round']-1} failed with {board_state['number_of_mission_fails'][board_state['round']-2]} fails!"

            # if number of fails from last round = 1 AND team didn't require two fails, mission failed
            elif board_state['number_of_mission_fails'][board_state['round']-2] == 1 and not board_state['team_size'][1][board_state['round']-2]:
                message += f"\r\nMission {board_state['round']-1} failed with {board_state['number_of_mission_fails'][board_state['round']-2]} fail!"

            # otherwise mission succeeded
            else:
                message += f"\r\nMission {board_state['round']-1} succeeded!"

    if board_state['phase'] == 'voting_phase':
        team_selected = ', '.join([str(elem)
                                  for elem in board_state['team_selected']])
        waiting_on = ', '.join([str(elem)
                               for elem in board_state['waiting_on_votes']])
        message = f"The team selected is: {team_selected}\r\nWaiting on votes from: {waiting_on}"

    if board_state['phase'] == 'mission_phase':
        waiting_on = ', '.join([str(elem)
                               for elem in board_state['team_selected']])
        message = f"Waiting on mission results from: {waiting_on}"

    if board_state['phase'] == 'assassination_phase':
        waiting_on = ', '.join([str(elem)
                               for elem in board_state['team_selected']])
        message = f"WHO WE SHOOTIN', BOYS?!"

# eff', 'mission': [], 'team_size': [2, 3, 2, 3, 3], 'round': 1, 'turn': 1, 'score': [], 'team_selected': ['Jeff', 'Frankie'], 'waiting_on_votes': ['Nate', 'Jeff', 'Frankie'],

    return message

#' '.join([str(elem) for elem in s])


"""
lobby_phase = True
picking_phase = False  #, player_picking_team
voting_phase = False
mission_phase = False
assassination_phase = False
game_over_phase = False
"""


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


# player1 = {
# 'name': 'Frankie',
# 'role': 'merlin',  #class object?
# 'votes': [[1, 1, 0],[0, 1]],
# 'on_team': [[1, 1, 0],[0, 1]],
# 'made_team': [[1, 0, 0],[1, 0]]
# }

# player2 = {
# 'name': 'Nate',
# 'role': 'assassin',  #class object?
# 'votes': [[1, 1, 0],[0, 1]],
# 'on_team': [[1, 1, 0],[0, 1]],
# 'made_team': [[0, 1, 0],[0, 1]]
# }

# player3 = {
# 'name': 'Jeff',
# 'role': 'morgana',  #class object?
# 'votes': [[1, 1, 0],[0, 1]],
# 'on_team': [[1, 1, 0],[0, 1]],
# 'made_team': [[0, 0, 1],[0, 0]]
# }


# sample_board_state = {
# 'players': [player1, player2, player3],
# 'player_picking_team': 'Nate',
# 'mission' : [1, 0, 0],
# 'phase' : 'lobby_phase'
# }


'''
def gamestate(players, votes, mission):
    gamestate = {
        'players': players,
        'votes': votes,
        'mission': mission
    }
    return gamestate
'''


########################
# TESTING GAME CONFIGS

players = []
#players = ['Nate','Frankie', 'Jeff']
#players = ['nate','cat']
#players = ['Nate','Jeff', 'Frankie', 'Phillip', "Robert", 'cat', 'bork', 'oof', 'small PP', '10', 'asdf', 'errrr']


# two player game start
board_state = {'phase': 'picking_phase', 'player_order': ['1', '2'], 'players': [{'name': '2', 'role': 'Merlin', 'votes': [[]], 'on_team': [[]], 'made_team': [[]]}, {'name': '1', 'role': 'Morgana', 'votes': [[]], 'on_team': [[]], 'made_team': [
    []]}], 'player_picking_team': '1', 'mission': [], 'number_of_mission_fails': [], 'team_size': [[1, 2, 1, 2, 1], [False, True, False, True, False]], 'round': 1, 'turn': 1, 'score': [], 'team_selected': [], 'votes_cast': [], 'mission_votes_cast': []}
players = ['1', '2']


# players = ['nate', 'jeff', 'frankie', 'cat',
#           'robert', 'phillip', 'oof', 'bork']


# just before people start voting
# board_state = {'phase': 'voting_phase', 'player_order': ['errrr', 'small PP', 'bork', 'Robert', 'Phillip', 'cat', 'Frankie', 'oof', '10', 'Nate', 'Jeff', 'asdf'], 'players': [{'name': 'asdf', 'role': 'Resistance', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'errrr', 'role': 'Assassin', 'votes': [[]], 'on_team': [[True]], 'made_team': [[True]]}, {'name': 'small PP', 'role': 'Percival', 'votes': [[]], 'on_team': [[True]], 'made_team': [[False]]}, {'name': 'bork', 'role': 'Spy', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Robert', 'role': 'Resistance', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Phillip', 'role': 'Percival', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'cat', 'role': 'Merlin', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Frankie', 'role': 'Sister', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'oof', 'role': 'Mordred', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': '10', 'role': 'Morgana', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Nate', 'role': 'Oberon', 'votes': [[]], 'on_team': [[True]], 'made_team': [[False]]}, {'name': 'Jeff', 'role': 'Sister', 'votes': [[]], 'on_team': [[True]], 'made_team': [[False]]}], 'player_picking_team': 'errrr', 'mission': [], 'number_of_mission_fails': [], 'team_size': [[4, 4, 5, 6, 6], [False, False, False, True, False]], 'round': 1, 'turn': 1, 'score': [], 'team_selected': ['errrr', 'small PP', 'Nate', 'Jeff'], 'waiting_on_votes': ['asdf', 'errrr', 'small PP', 'bork', 'Robert', 'Phillip', 'cat', 'Frankie', 'oof', '10', 'Nate', 'Jeff'], 'votes_cast': [], 'mission_votes_cast': []}
# players = ['errrr', 'small PP', 'bork', 'Robert', 'Phillip', 'cat', 'Frankie', 'oof', '10', 'Nate', 'Jeff', 'asdf']

# voting phase (people already started voting, doubt state is broken)
# board_state =  {'phase': 'voting_phase', 'player_order': ['errrr', 'small PP', 'bork', 'Robert', 'Phillip', 'cat', 'Frankie', 'oof', '10', 'Nate', 'Jeff', 'asdf'], 'players': [{'name': 'asdf', 'role': 'Resistance', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'errrr', 'role': 'Assassin', 'votes': [[]], 'on_team': [[True]], 'made_team': [[True]]}, {'name': 'small PP', 'role': 'Percival', 'votes': [[]], 'on_team': [[True]], 'made_team': [[False]]}, {'name': 'bork', 'role': 'Spy', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Robert', 'role': 'Resistance', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Phillip', 'role': 'Percival', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'cat', 'role': 'Merlin', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Frankie', 'role': 'Sister', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'oof', 'role': 'Mordred', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': '10', 'role': 'Morgana', 'votes': [[]], 'on_team': [[False]], 'made_team': [[False]]}, {'name': 'Nate', 'role': 'Oberon', 'votes': [[]], 'on_team': [[True]], 'made_team': [[False]]}, {'name': 'Jeff', 'role': 'Sister', 'votes': [[]], 'on_team': [[True]], 'made_team': [[False]]}], 'player_picking_team': 'errrr', 'mission': [], 'number_of_mission_fails': [], 'team_size': [[4, 4, 5, 6, 6], [False, False, False, True, False]], 'round': 1, 'turn': 1, 'score': [], 'team_selected': ['errrr', 'small PP', 'Nate', 'Jeff'], 'waiting_on_votes': ['asdf', 'small PP', 'bork',
# 'Robert', 'Phillip', 'cat', 'Frankie', 'oof', '10', 'Jeff'], 'votes_cast': [['errrr', 'approve'], ['Nate', 'approve']], 'mission_votes_cast': []}
# players =  ['errrr', 'small PP', 'bork', 'Robert', 'Phillip', 'cat', 'Frankie', 'oof', '10', 'Nate', 'Jeff', 'asdf']
