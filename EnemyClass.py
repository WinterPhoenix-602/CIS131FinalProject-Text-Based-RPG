#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Enemy Class

class Enemy:
    def __init__(self, name = '', health = 0, magic = 0, damage = 0, defense = 0, quantity = 0):
        self.name = name
        self.health = health
        self.magic = magic
        self.damage = damage
        self.defense = defense
        self.quantity = quantity

    def modify_health(self, change):
        self.health += change

    def modify_magic(self, change):
        self.magic += change
    
    def print_stats(self):
        print(f'____________________\n{self.name}\nHealth: {self.health}\nMagic: {self.magic}\nDamage: {self.damage}\nDefense: {self.defense}')
