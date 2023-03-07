#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Enemy Class

from random import randint #enables use of random numbers
from PlayerClass import Player

class Enemy:
    def __init__(self, name = "", health = 0, damage = 0, accuracy = 50):
        self.name = name
        self.health = health
        self.damage = damage
        self.accuracy = accuracy

    def modify_health(self, change):
        self.health += change

    def attack(self, target):
        if randint(1, 100) < self.accuracy:
            target.health -= self.damage / target.defense
            print(f"{self.name} hit you and dealt {self.damage / target.defense}!")
        else:
            print(f"{self.name} tried to hit you, but missed!")
    
    def print_stats(self):
        print(f"{self.name}\t{self.health}\t{self.damage}")
