username = None
roles = []

players = ['Nate','Frankie', 'Jeff']
#players = []



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




client_queue = []

