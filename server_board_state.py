

#players = ['Nate','Frankie', 'Jeff']
players = []



votes = {
    'Nate':[[1, 1, 0],[0, 1]],
    'Frankie':[[1, 1, 0],[0, 1]],
    'Jeff':[[1, 1, 0],[0, 1]]
    }

votes = {}

mission = [1, 0, 0]  #boolean success/fail

mission = []

#game_state = None #votes (calculate who's turn), mission success/fail

player_picking_team = 'Nate'




lobby_phase = True
picking_phase = False, player_picking_team
voting_phase = False
mission_phase = False
assassination_phase = False
game_over_phase = False






'''
def gamestate(players, votes, mission):
    gamestate = {
        'players': players,
        'votes': votes,
        'mission': mission
    }
    return gamestate
'''

def game_state(players=players, votes=votes, mission=mission):

    players = [x.encode('utf-8') for x in players]

    gamestate = {
        'players': players,
        'votes': votes,
        'mission': mission
    }
    return gamestate


def player_state(players=players):

    # initialize an empty string 
    player_string = " " 
    
    # return string   
    return (player_string.join(players)) 





    #players = [x.encode('utf-8') for x in players]
#items =  [u'a', u'b', u'c']
#[x.encode('utf-8') for x in items]
#return [[x.encode('utf-8') for x in i] for i in a]
