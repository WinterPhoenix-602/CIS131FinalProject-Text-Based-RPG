#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Location Tile Class

import textwrap
from PlayerClass import Player
from CombatEncounterClass import CombatEncounter
from tabulate import tabulate

invalidChoice = "I'm sorry, that is not a valid choice.\n"

class Tile:
    def __init__(self, name = "", description = "", directions = {"north":"", "east":"", "south":"", "west":""}, combatEncounter = {"_name":"", "_startDescription":[""], "_enemies":{}, "_endDescription":[""], "_triggerChance":[0, 0]}):
        self._name = name
        self._description = description
        self._directions = directions
        self._combatEncounter = combatEncounter
        
    #getters
    def get_name(self):
        return self._name
    def get_description(self):
        return "\n\n".join(self._description)
    def get_directions(self):
        return self._directions
    def get_combatEncounter(self):
        return self._combatEncounter

    #setters
    def set_name(self, name):
        self._name = name
    def set_description(self, description):
        self._description = description
    def set_directions(self, directions):
        self._directions = directions
    def set_combatEncounter(self, enemies):
        self._combatEncounter = enemies

    #sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
                if key == "_description":
                    for count, paragraph in enumerate(self._description):
                        self._description[count] = textwrap.fill(self._description[count], 100)
                if key == "_combatEncounter":
                    a = CombatEncounter()
                    a.reader(self._combatEncounter)
                    self._combatEncounter = a
            except:
                print("No such attribute, please consider adding it in init.")
                continue

    def tileMenu(self, turn = 0, player = Player(), destinationTileName = ""):
        save = ""
        noGo = "You can't go that way."
        while True:
            print(tabulate([[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid")) #print tile description
            print(player) #print player status
            print("") #adds newline between player status and choice menu

            #displays choice menu, gets player choice
            try:
                choice = int(input("What would you like to do?\n1: Go North\n2: Go East\n3: Go South\n4: Go West\n5: Open Inventory\n6: Exit Game\n? "))
                print("")
                match choice:
                    case 1:
                        if self._directions["north"] != "":
                            destinationTileName = self._directions["north"]
                            turn = self._combatEncounter.passive_actions(turn, player)
                            break
                        else:
                            print(noGo)
                            continue
                    case 2:
                        if self._directions["east"] != "":
                            destinationTileName = self._directions["east"]
                            turn = self._combatEncounter.passive_actions(turn, player)
                            break
                        else:
                            print(noGo)
                            continue
                    case 3: 
                        if self._directions["south"] != "":
                            destinationTileName = self._directions["south"]
                            turn = self._combatEncounter.passive_actions(turn, player)
                            break
                        else:
                            print(noGo)
                            continue
                    case 4:
                        if self._directions["west"] != "":
                            destinationTileName = self._directions["west"]
                            turn = self._combatEncounter.passive_actions(turn, player)
                            break
                        else:
                            print(noGo)
                            continue
                    case 5:
                        player.openInventory()
                        continue
                    case 6:
                        while True:
                            save = input("Would you like to save your progress? (yes/no): ")
                            if save == "yes":
                                break
                            elif save == "no":
                                save = input("Are you sure? (yes/no): ")
                                if save == "yes":
                                    print("\nThank you for playing.\n")
                                    save = "no"
                                    return turn, destinationTileName, choice, save
                                elif save == "no":
                                    continue
                                else:
                                    print(invalidChoice)
                            else:
                                    print(invalidChoice)
                        break
                    case _:
                        print(invalidChoice)
                        continue
            except:
                print(invalidChoice)
                continue
        return turn, destinationTileName, choice, save