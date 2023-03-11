#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Location Tile Class

import textwrap
from EnemyClass import Enemy
from tabulate import tabulate

class Tile:
    def __init__(self, name = "", description = "", combatEncounter = {"enemyName":{"_health":0, "_damage":0, "_quantity":0}}):
        self._name = name
        self._description = description
        self._combatEncounter = combatEncounter
        
    #getters
    def get_name(self):
        return self._name
    def get_description(self):
        return self._description
    def get_combatEncounter(self):
        return self._combatEncounter

    #setters
    def set_name(self, name):
        self._name = name
    def set_description(self, description):
        self._description = description
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
                    self._description = "\n\n".join(self._description)
            except:
                print("No such attribute, please consider adding it in init.")
                continue
        for enemy in self._combatEncounter:
            for quantity in range(self._combatEncounter[enemy]["quantity"]):
                self._combatEncounter_dict[enemy + str(quantity + 1)] = Enemy(f"{enemy} {quantity + 1}")
                self._combatEncounter_dict[enemy + str(quantity + 1)].reader(self._combatEncounter[enemy])
