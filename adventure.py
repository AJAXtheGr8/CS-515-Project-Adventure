# Ukarsh Shanker (ushanker@stevens.edu) 
import sys
import json
import inspect

class Adventure:
    
    def __init__(self,filename):
        self.collectedItems = []
        self.map = self.loadMap(filename)
        self.validDirections = ['north', 'south', 'east', 'west', 'northwest', 'northeast', 'southwest', 'southeast','upstairs','downstairs']
        self.changeRoom(self.map['start'])
        self.previousRoom = {}
        self.gameStopped = False

    def loadMap(self,filename):
        try:
            with open (filename, 'r') as f:
                mapJSON =  json.load(f)
                assert self.checkMapValidity(mapJSON)
                return mapJSON
        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")
            sys.exit(1)
        # except AssertionError:
        #     print("Error: Invalid Map")
        #     sys.exit(1)

    def checkMapValidity(self,mapJSON):

        roomNames = set()

        if 'rooms' not in mapJSON or 'start' not in mapJSON:
            return False
            # print('False 1')
        
        for room in mapJSON['rooms']:
            if not isinstance(room['name'],str) or not isinstance(room['desc'],str) or not isinstance(room['exits'],dict):
                return False
                # print('False 2')
            
        for room in mapJSON['rooms']:
            roomNames.add(room['name'])
        
        if len(mapJSON['rooms']) > len(roomNames):
            return False
            # print('False 3')        
        for room in mapJSON['rooms']:
            for exit in room['exits']:
                if room['exits'][exit] not in roomNames:
                    # print(room['name'],room['exits'][exit])
                    return False
                    # print('False 4')
        return True

    def changeRoom(self, str):
        for room in self.map['rooms']:
            if str == room["name"]:
                self.currentRoom = room

    def go(self,direction):
        if direction in self.currentRoom['exits']:
            if self.currentRoom['exits'][direction] == 'LOCKED':
                print(f"You can't go {direction} as it is LOCKED")

            else:    
                self.changeRoom(self.currentRoom['exits'][direction])
                print(f'You go {direction}.\n')
                self.look()
        else:
            print(f"There's no way to go {direction}.")

            

    def look(self):
        print(f'> {self.currentRoom["name"]}\n\n{self.currentRoom["desc"]}')
        if self.currentRoom['name'] == 'outside':
            self.quit()
        if 'items' in self.currentRoom and len(self.currentRoom['items'])>0:
            print("\nItems: ",end="")
            present_items = ""
            for item in self.currentRoom['items']:
                present_items += f'{item}, '
            print(present_items.strip()[0:-1])
        try:
            if not self.currentRoom['name'] == 'outside':
                exits = ' '.join(self.currentRoom['exits'].keys())
                print(f"\nExits: {exits}\n")
        except:
            pass

    def get(self,str):
        if 'items' in self.currentRoom and str in self.currentRoom['items']:
            self.collectedItems.append(str)
            self.currentRoom['items'].remove(str)
            print(f"You pick up the {str}.")

        else:
            print(f"There's no {str} anywhere.")

    def inventory(self):
        if len(self.collectedItems)==0:
            print("You're not carrying anything.")
        else:    
            print('Inventory:')
            for items in self.collectedItems:
                print(' ',items)      
        
    def quit(self):
        print("Goodbye!")
        self.gameStopped = True

    def unlock(self):
        if self.currentRoom['name'] == "banquet hall":
            if ("black-key" in self.collectedItems and "white-key" in self.collectedItems) or ("black-key" in self.collectedItems and "2-paper-clips" in self.collectedItems) or ("white-key" in self.collectedItems and "2-paper-clips" in self.collectedItems):
                self.currentRoom['exits']['north'] = 'outside'
                print('You have unlocked the red door')
            else:
                print('You have items missing in order to unlock the red door')
        else:
            print("There's nothing to unlock")

    def drop(self,item):
        try:
            self.collectedItems.remove(item)
            self.currentRoom['items'].append(item)
            print(f'You drop the {item}')
        except:
            print(f'You do not have {item} in your inventory')
        

    
    def getUserInput(self,str):
        output = str.lower().strip().split(" ")
        return output

    def help(self,):
        attributes = dir(Adventure)
        my_functions = [i for i in attributes if not i.startswith("__")]
        my_functions.remove('loadMap')
        my_functions.remove('startAdventure')
        my_functions.remove('getUserInput')
        my_functions.remove('changeRoom')
        print("You can run the following commands:")
        for func_name in my_functions:
            func = getattr(Adventure, func_name)
            signature = inspect.signature(func)
            
            if len(signature.parameters) > 1:
                print(f" {func_name} ...")
            else:
                print(f" {func_name}")  

    def startAdventure(self):
        self.look()
        while not self.gameStopped:
            try:
                player_command = self.getUserInput(input('What would you like to do? '))
   
                if player_command[0] == 'quit':
                    self.quit()
                else:
                    if player_command[0] == 'go':
                        if len(player_command)>=2:
                            self.go(player_command[1])
                        else:
                            print("Sorry, you need to 'go' somewhere.")    
                    elif player_command[0] in self.validDirections:
                        self.go(player_command[0])
                    elif player_command[0] == 'look':
                        self.look()
                    elif player_command[0] == "help":
                        self.help()
                    elif player_command[0] == "inventory":
                        self.inventory()
                    elif player_command[0] == "get":
                        if len(player_command)>=2:
                            self.get(player_command[1])
                        else:
                            print("Sorry, you need to 'get' something.")
                    elif player_command[0] == "drop":
                        if len(player_command)>=2:
                            self.drop(player_command[1])
                        else:
                            print("Sorry, you need to 'drop' something.")
                    elif player_command[0] == "unlock":
                        self.unlock()
                    else:
                        print("Sorry, you need to enter a valid command.")
                   
            except EOFError:
                print("Use 'quit' to exit.")
                continue


if __name__ == "__main__":
    if len(sys.argv) != 2:    
        print("Usage: python adventure.py [map file]")
        sys.exit(1)
        
    map_file = sys.argv[1]
    if(map_file=='mansion.map'):
        try:
            asciiArtFile = open('mansion_art.txt','r')
            content = asciiArtFile.read()
            print(content)
        except:
            pass
    game = Adventure(map_file)
    game.startAdventure()
