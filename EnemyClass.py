#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Enemy Class

from random import randint #enables use of random numbers
from PlayerClass import Player
from tabulate import tabulate

class Enemy:
    #initialization method
    def __init__(self, name = "", health = 0, maxHealth = 0, damage = 0, accuracy = 50):
        self._name = name
        self._health = health
        self._maxHealth = maxHealth
        self._damage = damage
        self._accuracy = accuracy

    #getters
    def get_name(self):
        return self._name
    def get_health(self):
        return self._health
    def get_maxHealth(self):
        return self._maxHealth
    def get_damage(self):
        return self._damage
    def get_accuracy(self):
        return self._accuracy
    
    #setters
    def set_name(self, name):
        self._name = name
    def set_health(self, health):
        self._health = health
    def set_maxHealth(self, maxHealth):
        self._maxHealth = maxHealth
    def set_damage(self, damage):
        self._damage = damage
    def set_accuracy(self, accuracy):
        self._accuracy = accuracy

    #sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                if key != "quantity":
                    setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
    
    #adds/subtracts value to health, displays appropriate message
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

    #attacks input target
    def attack(self, target = Player()):
        attempt = randint(1, 100)
        if attempt <= self._accuracy and (self._damage - target.get_defense()) > 0:
            target.modify_health(-self._damage + target.get_defense())
            print(tabulate([[f"{self._name} hits you and deals {self._damage - target.get_defense()} damage!"]], tablefmt="fancy_outline"))
        elif attempt <= self._accuracy:
            print(tabulate([[f"{self._name} attacks, and you deflect the blow with your {target.get_equippedShield().get_name()}!"]], tablefmt="fancy_outline"))
        else:
            print(tabulate([[f"{self._name} tries to attack you, but misses."]], tablefmt="fancy_outline"))

    #displays death message
    def death(self, encounter):
        print(tabulate([[f"{self._name} falls on the floor, dead."]], tablefmt="fancy_outline"))
        del encounter.get_enemies_dict()[self._name]
    
    #returns formatted list representation
    def get_stats_list(self):
        table = [self._name, self._health, self._damage]
        return table