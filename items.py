class Item:
    
    def __init__(self, name, description, weight, picked_up=True):
        self.name = name
        self.description = description
        self.weight = weight
        self.picked_up = picked_up
    
class Comestible(Item):
        
    def __init__(self, name, description, weight, incremet, atribute, picked_up=True):
        super().__init__(name, description, weight, picked_up)
        self.increment = incremet
        self.atribute = atribute
    
    def comer(self, player):
        if(self.atribute in player.__dict__):
            print('current', self.atribute, player.__dict__[self.atribute])
            print('el jugador se ha comido', self.name)
            player.__dict__[self.atribute] += self.increment
            print('new', self.atribute, player.__dict__[self.atribute])
            return True
        else:
            print('el jugador no tiene atributo', self.atribute)
            return False


class Equipamineto(Item):
    
    def __init__(self, name, description, weight, type, incremento, picked_up=True):
        super().__init__(name, description, weight, picked_up=picked_up)

class transportador(Item):

    def __init__(self, name, description, weight, picked_up=True):
        super().__init__(name, description, weight, picked_up=picked_up)
        self.room_back = None
    
    def is_active(self):
        return self.room_back is not None

class mision(Item):
    def __init__(self, name, description, weight, picked_up=True):
        super().__init__(name, description, weight, picked_up=picked_up)
        print('llave necesaria para hablar con john', self.name)
    def show_description(self):
        print ("")


