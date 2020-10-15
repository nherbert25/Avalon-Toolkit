class Character:
    
    known = None
    noted = None
    
    def __init__(self):
        pass

    def base(self):
        print("base class")



class Merlin(Character):

    known = ['assassin', 'morgana', 'spy']
    noted = None

class Percival(Character):

    known = None
    noted = ['merlin', 'morgana']

class Resistance(Character):

    known = None
    noted = None

class Morgana(Character):

    known = ['morgana', 'assassin', 'mordred', 'spy']
    noted = None

class Assassin(Character):

    known = ['morgana', 'assassin', 'mordred', 'spy']
    noted = None

class Mordred(Character):

    known = ['morgana', 'assassin', 'mordred', 'spy']
    noted = None

class Spy(Character):

    known = ['morgana', 'assassin', 'mordred', 'spy']
    noted = None

class Oberon(Character):

    known = None
    noted = None













merlin = Merlin()
print(merlin.known)