class CommandWords:
    
    def __init__(self):
        pass

    VALID_COMMANDS = ["go", "quit", "help", 'look', 'back', 'take', 'drop', 'bag', 'eat', 'open', 'activate', 'talk']

    def isCommand(self, aString):
        return aString in self.VALID_COMMANDS