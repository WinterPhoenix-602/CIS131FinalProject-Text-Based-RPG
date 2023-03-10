#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Player Class

class Player:
    #initialization method
    def __init__(self, name = "Player", health = 100, maxHealth = 100, mana = 50, maxMana = 50, damage = 1, defense = 1, shieldDuration = 0, inventory = {}):
        self._name = name
        self._health = health
        self._maxHealth = maxHealth
        self._mana = mana
        self._maxMana = maxMana
        self._damage = damage
        self._defense = defense
        self._shieldDuration = shieldDuration
        self._inventory = inventory

    #getters
    def get_name(self):
        return self._name
    def get_health(self):
        return self._health
    def get_maxHealth(self):
        return self._maxHealth
    def get_mana(self):
        return self._mana
    def get_maxMana(self):
        return self._maxMana
    def get_damage(self):
        return self._damage
    def get_defense(self):
        return self._defense
    def get_shieldDuration(self):
        return self._shieldDuration
    def get_inventory(self):
        return self._inventory
    
    #setters
    def set_name(self, name):
        self._name = name
    def set_health(self, health):
        self._health = health
    def set_maxHealth(self, maxHealth):
        self._maxHealth = maxHealth
    def set_mana(self, mana):
        self._mana = mana
    def set_maxMana(self, maxMana):
        self._maxMana = maxMana
    def set_damage(self, damage):
        self._damage = damage
    def set_defense(self, defense):
        self._defense = defense
    def set_shieldDuration(self, shieldDuration):
        self._shieldDuration = shieldDuration
    def set_inventory(self, inventory):
        self._inventory = inventory

    #sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
    
    #adds/subtracts value to health, displays appropriate message
    def modify_health(self, change):
        if change >= 1 and self._health + change <= self._maxHealth:
            self._health += change
            print(f"You are healed for {change} health points.")
        elif change < 1:
            self._health += change
        elif self._health + change > self._maxHealth:
            if self._maxHealth - self._health == 1:
                print(f"You are healed for {self._maxHealth - self._health} health point. Overspent a bit there.")
            else:
                print(f"You are healed for {self._maxHealth - self._health} health points. Overspent a bit there.")
            self._health += (self._maxHealth - self._health)

    #adds/subtracts value to mana, displays appropriate message
    def modify_mana(self, change):
        if change > 1 and self._mana + change < 50:
            self._mana += change
            print(f"Your mana regenerates {change} points.\n")
        elif change < 1:
            self._mana += change
            print(f"You expend {change} mana.")
        elif self._mana != 50:
            print(f"Your mana regenerates {50 - self._mana} points.\n")
            self._mana += (50 - self._mana)

    #attacks input target
    def attack(self, target, attackType):
        match attackType:
            case "melee":
                target.modify_health(-(self._inventory["equipped"]["Weapon"]["damage"]))
                print(f"You hit {target.get_name()} and deal {self._inventory['equipped']['Weapon']['damage']} damage!")
            case "fireball":
                target.modify_health(-8)
                print(f"The fire engulfs {target.get_name()} and deals 8 damage!")
            case _:
                print("Invalid attack type.")

    #adds/subtracts turns to shield duration
    def modify_shieldDuration(self, turns):
        if turns > 0 and self._shieldDuration > 0:
            print("Your mana flows out to reinforce your protection.")
        elif turns > 0:
            print("Your mana surges out into a shining shield, protecting you from harm.")
        self._shieldDuration += turns
        if self._shieldDuration > 0:
            self._defense = 2
        else:
            self._defense = 1

    #returns formatted inventory representation
    def inventory_string(self):
        inventoryString = f"Equipped Items:\nSlot:\tName\t\tStats\n"
        for item in self._inventory["equipped"]:
            inventoryString += f"{item}:\t{self._inventory['equipped'][item]['name']}\t{self._inventory['equipped'][item]['stats']}"
        return inventoryString
    
    #returns formatted string representation
    def __str__(self):
        if self._shieldDuration > 0:
            return f"{self._name}\t{self._health}\t{self._mana}\t{self._inventory['equipped']['Weapon']['damage']} ({self._inventory['equipped']['Weapon']['name']}) = {self._damage + self._inventory['equipped']['Weapon']['damage']}\nShielded turns remaining: {self._shieldDuration}"
        else:
            return f"{self._name}\t{self._health}\t{self._mana}\t{self._inventory['equipped']['Weapon']['damage']} ({self._inventory['equipped']['Weapon']['name']}) = {self._damage + self._inventory['equipped']['Weapon']['damage']}"

x = Player()

print(x.inventory_string())