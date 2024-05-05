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
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")
            sys.exit(1)

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
            if direction in self.validDirections:
                print(f"There's no way to go {direction}.")
            elif direction not in self.validDirections:
                print('Please enter a valid direction')
            

    def look(self):
        print(f"> {self.currentRoom["name"]}\n\n{self.currentRoom["desc"]}")
        if self.currentRoom['name'] == 'outside':
            self.quit()
        if 'items' in self.currentRoom and len(self.currentRoom['items'])>0:
            print("\nItems: ",end="")
            present_items = ""
            for item in self.currentRoom['items']:
                present_items += f'{item}, '
            print(present_items.strip()[0:-1])
        try:
            exits = ' '.join(self.currentRoom['exits'].keys())
            print(f"\nExits: {exits}\n")
        except:
            pass

    def get(self,str):
        if str in self.currentRoom['items']:
            self.collectedItems.append(str)
            self.currentRoom['items'].remove(str)
            print(f"You pick up the {str}.")

        else:
            print(f"There's no {str} anywhere.")

    def inventory(self):
        if len(self.collectedItems)==0:
            print("You're not carrying anything.")
        else:    
            print('Inventory: ')
            for items in self.collectedItems:
                print('  ',items)      
        
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
                            print("Sorry, you need to 'go' somewhere.\n")    
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
            except KeyboardInterrupt:
                print("\n  ...")
                print('KeyboardInterrupt')
                sys.exit()



if __name__ == "__main__":
    if len(sys.argv) != 2:    
        print("Usage: python adventure.py [map file]")
        sys.exit(1)
        
    map_file = sys.argv[1]
    if(map_file=='mansion.map'):
        asciiArtFile = open('mansion_art.txt','r')
        content = asciiArtFile.read()
        print(content)
    game = Adventure(map_file)
    game.startAdventure()