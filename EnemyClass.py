#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Enemy Class

from random import randint #enables use of random numbers

class Enemy:
    def __init__(self, name = "", health = 0, damage = 0, accuracy = 50):
        self._name = name
        self._health = health
        self._damage = damage
        self._accuracy = accuracy

    #getters
    def get_name(self):
        return self._name
    def get_health(self):
        return self._health
    def get_damage(self):
        return self._damage
    def get_accuracy(self):
        return self._accuracy
    
    #setters
    def set_name(self, name):
        self._name = name
    def set_health(self, health):
        self._health = health
    def set_damage(self, damage):
        self._damage = damage
    def set_accuracy(self, accuracy):
        self._accuracy = accuracy

    def modify_health(self, change):
        self.health += change

    def attack(self, target):
        if randint(1, 100) < self.accuracy:
            target.modify_health(-self.damage // target.defense)
            print(f"{self.name} hits you and deals {self.damage // target.defense} damage!")
        else:
            print(f"{self.name} tries to hit you, but misses.")

    def death(self):
        print(f"{self.name} falls on the floor, dead.")
    
    def __str__(self):
        if not "Troll" in self.name:
            return f"{self.name}\t{self.health}\t{self.damage}"
        else:
            return f"{self.name}\t\t{self.health}\t{self.damage}"
