#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Enemy Class

class Enemy:
    def __init__(self, name = '', health = 0, damage = 0):
        self.name = name
        self.health = health
        self.damage = damage

    def modify_health(self, change):
        self.health += change

    def modify_magic(self, change):
        self.magic += change
    
    def print_stats(self):
        print(f'{self.name}\t{self.health}\t{self.damage}')
