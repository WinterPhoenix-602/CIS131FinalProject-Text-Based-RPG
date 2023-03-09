#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Player Class

from random import randint

class Player:
    maxHealth = 100
    maxMana = 100

    def __init__(self, name = "Player", health = 100, mana = 50, damage = 1, defense = 1, shield = 0, inventory = {"equipped":{"name":"Iron Sword", "damage":5}}):
        self.name = name
        self.health = health
        self.mana = mana
        self.damage = damage
        self.defense = defense
        self.shield = shield
        self.inventory = inventory

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
        print(f"Your mana regenerated {change} points.")
        if self.mana > self.maxMana:
            self.mana = self.maxMana

    def attack(self, target, attackType):
        match attackType:
            case "melee":
                target.modify_health(-(self.damage + self.inventory["equipped"]["damage"]))
                print(f"You hit {target.name} and deal {self.damage + self.inventory['equipped']['damage']} damage!")
            case "fireball":
                target.modify_health(-8)
                print(f"The fire engulfed {target.name} and dealt 8 damage!")
            case _:
                print("Invalid attack type.")

    def shield_turns(self, turns):
        self.shield += turns
        if self.shield > 0:
            self.defense = 2
        else:
            self.defense = 1
    
    def print_stats(self):
        print(f"{self.name}\t{self.health}\t{self.mana}\t{self.damage} + {self.inventory['equipped']['damage']} ({self.inventory['equipped']['name']}) = {self.damage + self.inventory['equipped']['damage']}")
        if self.shield > 0:
            print(f"Shielded turns remaining: {self.shield}")
