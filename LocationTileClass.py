#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Location Tile Class

from EnemyClass import Enemy

class Tile:
    def __init__(self, name='', description='', enemy='', directions=[]):
        self.name = name
        self.description = description
        self.enemy = enemy
        self.directions = directions
        
    def reader(self, input_dict, *kwargs):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
                if self.enemy == 'goblin':
                    self.enemy = Enemy('Goblin', 20, 0, 2, 1)
            except:
                print("No such attribute, please consider adding it in init.")
                continue
