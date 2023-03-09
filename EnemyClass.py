#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Enemy Class

from random import randint #enables use of random numbers

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
            target.modify_health(-self.damage // target.defense)
            print(f"{self.name} hits you and deals {self.damage // target.defense} damage!")
        else:
            print(f"{self.name} tries to hit you, and misses!")

    def death(self):
        print(f"{self.name} falls on the floor, dead.")
    
    def print_stats(self):
        print(f"{self.name}\t{self.health}\t{self.damage}")
