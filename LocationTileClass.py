#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Location Tile Class

from EnemyClass import Enemy

class Tile:
    def __init__(self, name = "", description = "", enemies = {"enemyName":{"health":0, "damage":0, "quantity":0}}):
        self._name = name
        self._description = description
        self._enemies = enemies
        self._enemies_dict = {}
        
    #getters
    def get_name(self):
        return self._name
    def get_description(self):
        return self._description
    def get_enemies(self):
        return self._enemies
    def get_enemies_dict(self):
        return self._enemies_dict

    #setters
    def set_name(self, name):
        self._name = name
    def set_description(self, description):
        self._description = description
    def set_enemies(self, enemies):
        self._enemies = enemies
    def set_enemies_dict(self, enemies_dict):
        self._enemies_dict = enemies_dict

    #sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
        for enemy in self._enemies:
            for quantity in range(self._enemies[enemy]["quantity"]):
                self._enemies_dict[enemy + str(quantity + 1)] = Enemy(f"{enemy} {str(quantity + 1)}", self._enemies[enemy]["health"], self._enemies[enemy]["maxHealth"], self._enemies[enemy]["damage"])

    #displays enemies present on the tile
    def display_enemies(self):
        print(f"Enemy Name\tHealth\tDamage")
        for enemy in self._enemies_dict:
            print(self._enemies_dict[enemy].__str__())
        print(f"__________________________________________________")
