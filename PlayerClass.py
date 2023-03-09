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
        if change > 1 and self.mana + change < 50:
            self.mana += change
            print(f"Your mana regenerates {change} points.\n")
        elif change < 1:
            self.mana += change
            print(f"You expend {change} mana.\n")
        elif self.mana != 50:
            print(f"Your mana regenerates {50 - self.mana} points.\n")
            self.mana += (50 - self.mana)

    def attack(self, target, attackType):
        match attackType:
            case "melee":
                target.modify_health(-(self.damage + self.inventory["equipped"]["damage"]))
                print(f"You hit {target.name} and deal {self.damage + self.inventory['equipped']['damage']} damage!")
            case "fireball":
                target.modify_health(-8)
                print(f"The fire engulfs {target.name} and deals 8 damage!")
            case _:
                print("Invalid attack type.")

    def shield_turns(self, turns):
        if turns > 0 and self.shield > 0:
            print("Your mana flows out to reinforce your protection.\n")
        elif turns > 0:
            print("Your mana surges out into a shining shield, protecting you from harm.\n")
        self.shield += turns
        if self.shield > 0:
            self.defense = 2
        else:
            self.defense = 1
    
    def print_stats(self):
        print(f"{self.name}\t{self.health}\t{self.mana}\t{self.damage} + {self.inventory['equipped']['damage']} ({self.inventory['equipped']['name']}) = {self.damage + self.inventory['equipped']['damage']}")
        if self.shield > 0:
            print(f"Shielded turns remaining: {self.shield}")
