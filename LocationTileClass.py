#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Location Tile Class

from EnemyClass import Enemy

class Tile:
    def __init__(self, name='', description='', enemy=''):
        self.name = name
        self.description = description
        self.enemy = enemy
        
    def reader(self, input_dict, *kwargs):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
                if self.enemy == 'goblin':
                    self.enemy = Enemy('Goblin', 20, 0, 2, 1)
            except:
                print("No such attribute, please consider adding it in init.")
                continue

    def offerDirections(self):
        print(f'1: Go North\n2: Go East\n3: Go South\n4: Go West')
