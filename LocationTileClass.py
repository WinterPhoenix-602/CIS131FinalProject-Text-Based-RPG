#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Location Tile Class

from EnemyClass import Enemy

class Tile:
    def __init__(self, name = "", description = "", enemies = {"enemyName":{"health":0, "damage":0, "quantity":0}}):
        self.name = name
        self.description = description
        self.enemies = enemies
        self.enemies_dict = {}
        
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
        for enemy in self.enemies:
            for quantity in range(self.enemies[enemy]["quantity"]):
                self.enemies_dict[enemy + str(quantity + 1)] = Enemy(f"{enemy} {str(quantity + 1)}", self.enemies[enemy]["health"], self.enemies[enemy]["damage"])

    def display_enemies(self):
        print(f"Enemy Name\tHealth\tDamage")
        for enemy in self.enemies_dict:
            print(self.enemies_dict[enemy].__str__())
        print(f"__________________________________________________")
