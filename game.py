from room import Room
from items import Item, Comestible, transportador, mision
from player import Player
from npc import npc
from stack import Stack, inverse
from parser_commands import Parser





class Game:
    def __init__(self):
        self.createRooms()
        self.player = Player('jugador 1', 20)
        self.parser = Parser()
        self.stack = Stack()

    def createRooms(self):
        recepcion = Room("en la recepcion del hospital")
        juegos = Room("en la habitacion de juegos")
        cocina = Room("en la cocina del hospital")
        salamedica = Room("en la sala medica")
        quirofano = Room("en el quirofano")
        terapia = Room("en terapia intensiva")
        baños = Room("en los baños")
        sotano = Room("en el sotano")
        techo = Room("en el techo")
        patio = Room("en el patio")

        recepcion.setExits(None, cocina, salamedica, juegos, None, sotano, None)
        juegos.setExits(None, recepcion, quirofano, None, techo, None, None)
        cocina.setExits(None, None, terapia, recepcion, None, None, patio)
        salamedica.setExits(recepcion, None, baños, quirofano, None, None, None)
        quirofano.setExits(juegos, salamedica, None, None, None, None, None)
        terapia.setExits(cocina, None, None, None, None, None, None)
        baños.setExits(salamedica, None, None, None, None, None, None)
        sotano.setExits(None, None, None, None, recepcion, None, None)
        techo.setExits(None, None, None, None, None, juegos, None)
        patio.setExits(None, None, None, None, None, None, cocina)

        bisturi = Item('bisturi', 'esto es un bisturi viejo', 19)
        zapatillas = Item('zapatilla', 'esto es un par de zapatillas viejas..', 0.87)
        silla = Item('silla', 'una silla para descansar', 2)
        ropero = Item('ropero', 'un ropero antiguo', 15, picked_up=False)
        bag = Item('mochila', 'una mochila', 1)
        llaveantigua = mision('llaveantigua', 'llave magica para hablar con john', 0.2)
        transport = transportador('transportador', 'un transportador magico', 1)
        cookie = Comestible('cookie', 'esto es una gallleta magica', 0.1, 5, 'max_weight')
        john = npc('john', 'tienes una mision!')
        
        recepcion.setItem(bisturi)
        recepcion.setItem(transport)
        recepcion.setItem(zapatillas)
        recepcion.setItem(ropero)
        cocina.setItem(silla)
        cocina.setItem(llaveantigua)
        recepcion.setItem(cookie)
        recepcion.setnpc(john)
        
        self.currentRoom = recepcion
        
        return

    def play(self):
        self.printWelcome()
        
        finished = False
        while(not finished):
            command = self.parser.getCommand()
            finished = self.processCommand(command)
        print("Thank you for playing.  Good bye.")
            
        

    def printWelcome(self):
        print()
        print("Welcome to the World of Zuul!")
        print("World of Zuul is a new, incredibly boring adventure game.")
        print("Type 'help' if you need help.")
        print("")
        self.currentRoom.print_location_information()
        print()

    def processCommand(self, command):
        wantToQuit = False

        if(command.isUnknown()):
            print("I don't know what you mean...")
            return False
        
        commandWord = command.getCommandWord()
        if(commandWord == "help"):
            self.printHelp()
        elif(commandWord == "go"):
            self.goRoom(command)
        elif(commandWord == "quit"):
            wantToQuit = self.quit(command)
        elif(commandWord == "look"):
            self.look_items()
        elif(commandWord == "bag"):
            self.bag_items()
        elif(commandWord == "back"):
            self.goBack()
        elif(commandWord == "take"):
            self.takeItem(command)
        elif(commandWord == "drop"):
            self.dropItem(command)
        elif(commandWord == "eat"):
            self.eatItem(command)
        elif(commandWord == "activate"):
            self.activatetransport(command)
        elif(commandWord == "open"):
            self.opentransport(command)
        elif(commandWord == "talk"):
            self.talknpc(command)
        

        return wantToQuit

    def printHelp(self):
        print("You are lost. You are alone. You wander")
        print("around at the university.")
        print()
        print("Your command words are:")
        print("   go quit help")

    def goRoom(self,command):
        if(not command.hasSecondWord()):
            print("Go where?")
            return
        
        direction = command.getSecondWord()
        nextRoom = self.currentRoom.get_exit(direction)

        if(nextRoom == None):
            print("There is no door!")
        else:
            self.currentRoom = nextRoom
            self.currentRoom.print_location_information()
            self.stack.push(direction)
            print()
            
    def takeItem(self, command):
        if(not command.hasSecondWord()):
            print("Take what?")
            return

        item_name = command.getSecondWord()
        item = self.currentRoom.getItem(item_name)
       
        if(item is None):
            print("There is not item in the room with this name!")
        else:
            if(item.picked_up):
                if(self.player.can_picked_up_new_item(item.weight)):
                    self.player.setItem(item)
                else:
                    print("no puedes levantar tanto peso..")
                    self.currentRoom.setItem(item)
            else:
                print ("este item puede ser levantado")
                self.currentRoom.setItem(item)
    def dropItem(self, command):
        if(not command.hasSecondWord()):
            print("Drop what?")
            return

        item_name = command.getSecondWord()
        item = self.player.getItem(item_name)
       
        if(item is None):
            print("There is not item in the player bag with this name!")
        else:
            self.currentRoom.setItem(item)

    def eatItem(self, command):
        if(not command.hasSecondWord()):
            print("Eat what?")
            return

        item_name = command.getSecondWord()
        item = self.player.getItem(item_name)
       
        if(item is None):
            print("There is not item in the player bag with this name!")
        else:
            if(isinstance(item, Comestible)):
                response = item.comer(self.player)
                if(not response):
                    self.player.setItem(item)
            else:
                print('este item no es comestible')
                self.player.setItem(item)
                
    def activatetransport(self, command):
        if(not command.hasSecondWord()):
            print("activate what?")
            return

        item_name = command.getSecondWord()
        item = self.player.getItem(item_name)

        if(item is None):
            print("There is not item in the player bag with this name!")
        else:
            if(isinstance(item, transportador)):
                if(item.is_active()):
                    print('transportandome')
                    self.currentRoom = item.room_back
                    self.createRooms.print_location_information()
                else:
                    print('el transportador no fue abierto todavia')
                    self.player.setItem(item)
            else:
                print('este item no es del tipo transportador y no se puede activar')
                self.player.setItem(item)

    def opentransport(self, command):
        if(not command.hasSecondWord()):
            print("Eat what?")
            return

        item_name = command.getSecondWord()
        item = self.player.getItem(item_name)

        if(item is None):
            print("Rhere is not item in the player bag with this name!")
        else:
            if(isinstance(item, transportador)):
                print('room set to back is', self.currentRoom.description)
                item.room_back = self.currentRoom
            else:
                print("este item no es del tipo transportador y no se puede abrir")

            self.player.setItem(item)
    
    def talknpc(self, command):
        if(not command.hasSecondWord()):
            print("Talk what?")
            return
        item_name = command.getSecondWord()
        item = self.player.getItem(item_name)
       
        if(item is None):
            print("There is not item in the player bag with this name!")
        else:
            if(isinstance(item,transportador)):
                print('teletransportando')
                self.currentRoom = item.room_volver
            else:
                print("el teletransportador no se abrió todavia")
                self.player.setItem(item)

    
    def look_items(self):
        self.currentRoom.print_items_information()

    def bag_items(self):
        self.player.print_items_information()
    
    def goBack(self):
        direction = self.stack.pop()
        if(direction):
            nextRoom = self.currentRoom.get_exit(direction)
       
            if(nextRoom is None):
                print("There is no door! to go", direction)
                self.stack.push(inverse[direction])
            else:
                self.currentRoom = nextRoom
                self.currentRoom.print_location_information()
                print()
        else:
            print('you are in the initial position, can not go back')
        

    def quit(self, command):
        if(command.hasSecondWord()):
            print("Quit what?")
            return False
        else:
            return True

g = Game()
g.play()