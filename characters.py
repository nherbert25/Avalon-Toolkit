

#[ allienment  ,    known,     percival noteds      ]

character_dictionary = {

    'Merlin': ['good', ['Assassin', 'Morgana', 'Spy', 'Oberon']],
    'Percival': ['good', [],   ['Merlin', 'Morgana']          ],
    'Sister': ['good', [],   ['Sister']          ],
    'Resistance': ['good', []       ],
    'Morgana': ['evil', ['Assassin', 'Morgana', 'Mordred', 'Spy']],
    'Assassin': ['evil', ['Assassin', 'Morgana', 'Mordred', 'Spy']],
    'Mordred': ['evil', ['Assassin', 'Morgana', 'Mordred', 'Spy']],
    'Spy': ['evil', ['Assassin', 'Morgana', 'Spy']],
    'Oberon': ['evil', []],


}





class Character:
    

    
    def __init__(self):
        #known = None
        #noted = None
        pass

    def base(self):
        print("base class")




class Merlin(Character):
    def __init__(self):
        self.name = 'merlin'
        self.known = ['assassin', 'morgana', 'spy']
        self.noted = []
        self.team = 'good'

class Percival(Character):

    def __init__(self):
        self.name = 'merlin'
        self.known = []
        self.noted = ['merlin', 'morgana']

class Resistance(Character):
    
    def __init__(self):
        self.name = 'resistance'
        self.known = []
        self.noted = []

class Morgana(Character):
    
    def __init__(self):
        self.name = 'morgana'
        self.known = ['morgana', 'assassin', 'mordred', 'spy']
        self.noted = []

class Assassin(Character):
    
    def __init__(self):
        self.name = 'assassin'
        self.known = ['morgana', 'assassin', 'mordred', 'spy']
        self.noted = []

class Mordred(Character):
    
    def __init__(self):
        self.name = 'mordred'
        self.known = ['morgana', 'assassin', 'mordred', 'spy']
        self.noted = []

class Spy(Character):
    
    def __init__(self):
        self.name = 'spy'
        self.known = ['morgana', 'assassin', 'mordred', 'spy']
        self.noted = []

class Oberon(Character):
    
    def __init__(self):
        self.name = 'oberon'
        self.known = []
        self.noted = []