#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Enemy Class

class Enemy:
    def __init__(self, name, health, magic, damage, defense):
        self.name = name
        self.health = health
        self.magic = magic
        self.damage = damage
        self.defense = defense

    def modifyHealth(self, change):
        self.health += change

    def modifyMagic(self, change):
        self.magic += change
    
    def printStats(self):
        print(f'____________________\n{self.name}\nHealth: {self.health}\nMagic: {self.magic}\nDamage: {self.damage}\nDefense: {self.defense}')
