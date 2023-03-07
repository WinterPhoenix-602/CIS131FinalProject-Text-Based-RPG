#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Player Class

from random import randint

class Player:
    maxHealth = 100
    maxMana = 100

    def __init__(self, name = "Player", health = 100, mana = 50, damage = 5, defense = 1):
        self.name = name
        self.health = health
        self.mana = mana
        self.damage = damage
        self.defense = defense

    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
    
    def modify_health(self, change):
        self.health += change
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def modify_mana(self, change):
        self.mana += change
        if self.mana > self.maxMana:
            self.mana = self.maxMana

    def attack(self, target):
        target.health -= self.damage
        print(f"You hit {target.name} and dealt {self.damage} damage!")
    
    def print_stats(self):
        print(f"{self.name}\t{self.health}\t{self.mana}\t{self.damage}")
