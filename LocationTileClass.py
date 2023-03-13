# Caiden Wilson
# 3/2/2023
# CIS131
# Final Project: Location Tile Class

import textwrap
from PlayerClass import Player
from CombatEncounterClass import CombatEncounter
from tabulate import tabulate

invalidChoice = "\n" + \
    tabulate([["I'm sorry, that is not a valid choice."]]) + "\n"


class Tile:
    def __init__(self, name="", description="", directions={"north": "", "east": "", "south": "", "west": ""}, combatEncounter=CombatEncounter()):
        self._name = name
        self._description = description
        self._directions = directions
        self._combatEncounter = combatEncounter

    # getters
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return "\n\n".join(self._description)

    @property
    def directions(self):
        return self._directions

    @property
    def combatEncounter(self):
        return self._combatEncounter

    # setters
    @name.setter
    def name(self, name):
        self._name = name

    @description.setter
    def description(self, description):
        self._description = description

    @directions.setter
    def directions(self, directions):
        self._directions = directions

    @combatEncounter.setter
    def combatEncounter(self, combatEncounter):
        self._combatEncounter = combatEncounter

    # sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
            if key == "_description":
                for count, paragraph in enumerate(self._description):
                    self._description[count] = textwrap.fill(
                        self._description[count], 100)
            if key == "_combatEncounter":
                a = CombatEncounter()
                a.reader(self._combatEncounter)
                self._combatEncounter = a

    def tileMenu(self, turn=0, player=Player(), destinationTileName=""):
        save = ""
        noGo = tabulate([["You can't go that way."]], tablefmt="fancy_outline")
        while True:
            # print tile description
            print(tabulate(
                [[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid"))
            print(player)  # print player status

            # displays choice menu, gets player choice
            try:
                choice = int(input(tabulate([["What would you like to do?"], ["1: Go North"], ["2: Go East"], ["3: Go South"], [
                             "4: Go West"], ["5: Open Inventory"], ["6: Exit Game"]], headers="firstrow", tablefmt="fancy_outline") + "\n? "))
                print("")
            except:
                print(invalidChoice)
                continue
            match choice:
                case 1:
                    if self._directions["north"] != "":
                        destinationTileName = self._directions["north"]
                        turn = self._combatEncounter.passive_actions(
                            turn, player)
                        break
                    else:
                        print(noGo)
                        continue
                case 2:
                    if self._directions["east"] != "":
                        destinationTileName = self._directions["east"]
                        turn = self._combatEncounter.passive_actions(
                            turn, player)
                        break
                    else:
                        print(noGo)
                        continue
                case 3:
                    if self._directions["south"] != "":
                        destinationTileName = self._directions["south"]
                        turn = self._combatEncounter.passive_actions(
                            turn, player)
                        break
                    else:
                        print(noGo)
                        continue
                case 4:
                    if self._directions["west"] != "":
                        destinationTileName = self._directions["west"]
                        turn = self._combatEncounter.passive_actions(
                            turn, player)
                        break
                    else:
                        print(noGo)
                        continue
                case 5:
                    player.openInventory()
                    continue
                case 6:
                    while True:
                        save = input(
                            "Would you like to save your progress? (yes/no): ")
                        if save == "yes":
                            break
                        elif save == "no":
                            save = input("Are you sure? (yes/no): ")
                            if save == "yes":
                                print(
                                    "\n" + tabulate([["Thank you for playing."]], tablefmt="fancy_outline") + "\n")
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
        return turn, destinationTileName, choice, save
