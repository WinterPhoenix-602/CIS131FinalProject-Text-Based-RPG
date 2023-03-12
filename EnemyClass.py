# Caiden Wilson
# 3/2/2023
# CIS131
# Final Project: Enemy Class

from random import randint # enables use of random numbers
from PlayerClass import Player
from tabulate import tabulate

class Enemy:
    # initialization method
    def __init__(self, name = "", health = 0, maxHealth = 0, damage = 0, accuracy = 50):
        self._name = name
        self._health = health
        self._maxHealth = maxHealth
        self._damage = damage
        self._accuracy = accuracy

    # getters
    @property
    def name(self):
        return self._name
    @property
    def health(self):
        return self._health
    @property
    def maxHealth(self):
        return self._maxHealth
    @property
    def damage(self):
        return self._damage
    @property
    def accuracy(self):
        return self._accuracy

    # setters
    @name.setter
    def name(self, name):
        self._name = name
    @health.setter
    def health(self, health):
        self._health = health
    @maxHealth.setter
    def maxHealth(self, maxHealth):
        self._maxHealth = maxHealth
    @damage.setter
    def damage(self, damage):
        self._damage = damage
    @accuracy.setter
    def accuracy(self, accuracy):
        self._accuracy = accuracy

    # sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                if key != "quantity":
                    setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
    
    # adds/subtracts value to health, displays appropriate message
    def modify_health(self, change):
        if change >= 1 and self._health + change < self._maxHealth:
            self._health += change
            print(tabulate([[f"{self._name} is healed for {change} health points."]], tablefmt="fancy_outline"))
        elif change < 1:
            self._health += change
        elif self._health != self._maxHealth:
            if self._maxHealth - self._health == 1:
                print(tabulate([[f"{self._name} is healed for {self._maxHealth - self._health} health point."]], tablefmt="fancy_outline"))
            else:
                print(tabulate([[f"{self._name} is healed for {self._maxHealth - self._health} health points."]], tablefmt="fancy_outline"))
            self._health += (self._maxHealth - self._health)

    # attacks input target
    def attack(self, target = Player()):
        attempt = randint(1, 100)
        if attempt <= self._accuracy and (self._damage - target.defense) > 0:
            target.modify_health(-self._damage + target.defense)
            print(tabulate([[f"{self._name} hits you and deals {self._damage - target.defense} damage!"]], tablefmt="fancy_outline"))
        elif attempt <= self._accuracy:
            print(tabulate([[f"{self._name} attacks, and you deflect the blow with your {target.equippedShield.name}!"]], tablefmt="fancy_outline"))
        else:
            print(tabulate([[f"{self._name} tries to attack you, but misses."]], tablefmt="fancy_outline"))

    # displays death message
    def death(self, encounter):
        print(tabulate([[f"{self._name} falls on the floor, dead."]], tablefmt="fancy_outline"))
        del encounter.enemies_dict()[self._name]
    
    # returns formatted list representation
    def get_stats_list(self):
        table = [self._name, self._health, self._damage]
        return table