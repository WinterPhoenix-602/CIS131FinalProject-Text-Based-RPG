#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Player Class

from random import randint

class Player:
    maxHealth = 100
    maxMana = 100

    def __init__(self, name = "Player", health = 100, mana = 50, damage = 1, defense = 1, shield = 0, inventory = {"equipped":{"name":"Iron Sword", "damage":5}}):
        self._name = name
        self._health = health
        self._mana = mana
        self._damage = damage
        self._defense = defense
        self._shield = shield
        self._inventory = inventory

    #getters
    def get_name(self):
        return self._name
    def get_health(self):
        return self._health
    def get_mana(self):
        return self._mana
    def get_damage(self):
        return self._damage
    def get_defense(self):
        return self._defense
    def get_shield(self):
        return self._shield
    def get_inventory(self):
        return self._inventory
    
    #setters
    def set_name(self, name):
        self._name = name
    def set_health(self, health):
        self._health = health
    def set_mana(self, mana):
        self._mana = mana
    def set_damage(self, damage):
        self._damage = damage
    def set_defense(self, defense):
        self._defense = defense
    def set_shield(self, shield):
        self._shield = shield
    def set_inventory(self, inventory):
        self._inventory = inventory

    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
    
    def modify_health(self, change):
        if change >= 1 and self.health + change < 100:
            self.health += change
            print(f"You are healed for {change} health points.")
        elif change < 1:
            self.health += change
        elif self.health != 100:
            if 100 - self.health == 1:
                print(f"You are healed for {100 - self.health} health point. Overspent a bit there.")
            else:
                print(f"You are healed for {100 - self.health} health points. Overspent a bit there.")
            self.health += (100 - self.health)

    def modify_mana(self, change):
        if change > 1 and self.mana + change < 50:
            self.mana += change
            print(f"Your mana regenerates {change} points.\n")
        elif change < 1:
            self.mana += change
            print(f"You expend {change} mana.")
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
            print("Your mana flows out to reinforce your protection.")
        elif turns > 0:
            print("Your mana surges out into a shining shield, protecting you from harm.")
        self.shield += turns
        if self.shield > 0:
            self.defense = 2
        else:
            self.defense = 1
    
    def __str__(self):
        if self.shield > 0:
            return f"{self.name}\t{self.health}\t{self.mana}\t{self.damage} + {self.inventory['equipped']['damage']} ({self.inventory['equipped']['name']}) = {self.damage + self.inventory['equipped']['damage']}\nShielded turns remaining: {self.shield}"
        else:
            return f"{self.name}\t{self.health}\t{self.mana}\t{self.damage} + {self.inventory['equipped']['damage']} ({self.inventory['equipped']['name']}) = {self.damage + self.inventory['equipped']['damage']}"
