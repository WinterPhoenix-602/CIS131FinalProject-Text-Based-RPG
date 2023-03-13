# Caiden Wilson
# 3/12/2023
# CIS131
# Final Project: Entity classes (Player, Enemy)

import abc
from random import randint
from ItemClass import Item
from tabulate import tabulate
from SlowPrint import slowLinePrint

invalidChoice = "\n" + \
    tabulate([["I'm sorry, that is not a valid choice."]],
             tablefmt="fancy_outline") + "\n"

# abstract base class


class Entity(abc.ABC):
    def __init__(self, name="", level=0, levelProgress=0, nextLevel=0, levelTable=[0, 0, 0, 0, 0, 0, 0, 0], health=0, maxHealth=0, mana=0, maxMana=0, damage=0, defense=0, accuracy=0, inventory={}, equippedWeapon=Item(), equippedShield=Item()):
        self._name = name
        self._level = level
        self._levelProgress = levelProgress
        self._nextLevel = nextLevel
        self._levelTable = levelTable
        self._health = health
        self._maxHealth = maxHealth
        self._mana = mana
        self._maxMana = maxMana
        self._damage = damage
        self._defense = defense
        self._accuracy = accuracy
        self._inventory = inventory
        self._equippedWeapon = equippedWeapon
        self._equippedShield = equippedShield

    # getters
    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def levelProgress(self):
        return self._levelProgress

    @property
    def nextLevel(self):
        return self._nextLevel

    @property
    def levelTable(self):
        return self._levelTable

    @property
    def health(self):
        return self._health

    @property
    def maxHealth(self):
        return self._maxHealth

    @property
    def mana(self):
        return self._mana

    @property
    def maxMana(self):
        return self._maxMana

    @property
    def damage(self):
        return self._damage

    @property
    def defense(self):
        return self._defense

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def inventory(self):
        return self._inventory

    @property
    def equippedWeapon(self):
        return self._equippedWeapon

    @property
    def equippedShield(self):
        return self._equippedShield

    # setters
    @name.setter
    def name(self, name=""):
        self._name = name

    @level.setter
    def level(self, level=0):
        self._level = level

    @levelProgress.setter
    def levelProgress(self, levelProgress=0):
        self._levelProgress = levelProgress

    @nextLevel.setter
    def nextLevel(self, nextLevel=0):
        self._nextLevel = nextLevel

    @levelTable.setter
    def levelTable(self, levelTable=[]):
        self._levelTable = levelTable

    @health.setter
    def health(self, health=0):
        self._health = health

    @maxHealth.setter
    def maxHealth(self, maxHealth=0):
        self._maxHealth = maxHealth

    @mana.setter
    def mana(self, mana=0):
        self._mana = mana

    @maxMana.setter
    def maxMana(self, maxMana=0):
        self._maxMana = maxMana

    @damage.setter
    def damage(self, damage):
        self._damage = damage

    @defense.setter
    def defense(self, defense=0):
        self._defense = defense

    @accuracy.setter
    def accuracy(self, accuracy=0):
        self._accuracy = accuracy

    @inventory.setter
    def inventory(self, inventory={}):
        self._inventory = inventory

    @equippedWeapon.setter
    def equippedWeapon(self, equippedWeapon=Item()):
        self._equippedWeapon = equippedWeapon

    @equippedShield.setter
    def equippedShield(self, equippedShield=Item()):
        self._equippedShield = equippedShield

    # sets attributes from input dictionary
    def reader(self, input_dict={}):
        for key in input_dict:
            try:
                if key != "quantity":
                    setattr(self, key, input_dict[key])
            except:
                slowLinePrint(
                    "No such attribute, please consider adding it in init.")
                continue
        self.level_up(level=self.level)
        for itemType in self._inventory:
            if itemType != "Equipped":
                for item in self._inventory[itemType]:
                    if type(self._inventory[itemType][item]) != Item:
                        self._inventory[itemType][item] = Item(
                            itemType, item, self._inventory[itemType][item]["stats"], self._inventory[itemType][item]["quantity"])
        self._equippedWeapon = self._inventory["Weapon"][self._inventory["Equipped"]["Weapon"]]
        self._equippedShield = self._inventory["Shield"][self._inventory["Equipped"]["Shield"]]

    # sets stats based on level
    def level_up(self, exp=0, level=0):
        levelChange = 0
        if level > 0:
            exp = 25 * ((level + self._level) - 1) * (level - self._level)
        if exp > 0:
            self._levelProgress += exp
            while self._levelProgress >= self._nextLevel:
                self._levelProgress = self._levelProgress - self._nextLevel
                self._level += 1
                levelChange += 1
        self._nextLevel = self._level * 50
        self._maxHealth = self._levelTable[0] + \
            (self._levelTable[1] * (self._level - 1))
        self._maxMana = self._levelTable[2] + \
            (self._levelTable[3] * (self._level - 1))
        self._damage = self._levelTable[4] + \
            (self._levelTable[5] * (self._level - 1))
        self._defense = self._levelTable[6] + \
            (self._levelTable[7] * (self._level - 1))
        return exp, levelChange

    # modify specified attribute by adding/subtracting given value
    def modify_attribute(self, attribute="", change=0):
        if attribute == "health":
            if change >= 1 and self._health + change <= self._maxHealth:
                self._health += change
            elif change < 1:
                self._health += change
            elif self._health + change > self._maxHealth:
                self._health += (self._maxHealth - self._health)
        if attribute == "mana":
            if change > 1 and self._mana + change <= self._maxMana:
                self._mana += change
            elif change < 1:
                self._mana += change
            elif self._mana != 50:
                self._mana += (50 - self._mana)

    # uses a melee attack on input target
    def melee_attack(self, target):
        attempt = randint(1, 100)
        damage = self.compute_damage(target)
        if attempt <= self._accuracy and damage > 0:
            target.modify_attribute("health", -damage)
        return attempt, damage

    # finds damage done by an attack
    def compute_damage(self, target):
        damage = self._damage + self._equippedWeapon.stats["Damage"]
        defense = target.defense + target._equippedShield.stats["Defense"]
        return max(damage - defense, 0)


# player class
class Player(Entity):
    def __init__(self, name="Newbie", level=0, levelProgress=0, nextLevel=0, levelTable=[100, 50, 50, 25, 5, 5, 2, 2], health=100, maxHealth=100, mana=50, maxMana=50, damage=5, defense=2, accuracy=100, equippedWeapon=Item(), equippedShield=Item(), shieldDuration=0, inventory={}):
        super().__init__(name, level, levelProgress, nextLevel, levelTable, health,
                         maxHealth, mana, maxMana, damage, defense, accuracy, equippedWeapon, equippedShield)
        self._shieldDuration = shieldDuration
        self._inventory = inventory

    @property
    def shieldDuration(self):
        return self._shieldDuration

    @property
    def inventory(self):
        return self._inventory

    @shieldDuration.setter
    def shieldDuration(self, shieldDuration):
        self._shieldDuration = shieldDuration

    @inventory.setter
    def inventory(self, inventory):
        self._inventory = inventory

    def level_up(self, exp=0, level=0):
        exp, levelChange = super().level_up(exp, level)
        if exp > 0:
            slowLinePrint(
                tabulate([[f"You gained {exp} experience."]], tablefmt="fancy_outline"))
            if levelChange > 0:
                slowLinePrint(tabulate(
                    [[f"You leveled up! {self._level - levelChange} -> {self._level}"]], tablefmt="fancy_outline"))

    # modify specified attribute by adding/subtracting given value
    def modify_attribute(self, attribute, change):
        super().modify_attribute(attribute, change)
        # displays appropriate messages
        if attribute == "health":
            if change >= 1 and self._health + change <= self._maxHealth:
                slowLinePrint(tabulate(
                    [[f"You are healed for {change} health points."]], tablefmt="fancy_outline"))
            elif self._health + change > self._maxHealth:
                if self._maxHealth - self._health == 1:
                    slowLinePrint(tabulate(
                        [[f"You are healed for {self._maxHealth - self._health} health point. Overspent a bit there."]], tablefmt="fancy_outline"))
                else:
                    slowLinePrint(tabulate(
                        [[f"You are healed for {self._maxHealth - self._health} health points. Overspent a bit there."]], tablefmt="fancy_outline"))
        if attribute == "mana":
            if change > 1 and self._mana + change <= self._maxMana:
                slowLinePrint(tabulate(
                    [[f"Your mana regenerates {change} points.\n"]], tablefmt="fancy_outline"))
            elif change < 1:
                slowLinePrint(
                    tabulate([[f"You expend {change} mana."]], tablefmt="fancy_outline"))
            elif self._mana != 50:
                slowLinePrint(tabulate(
                    [[f"Your mana regenerates {50 - self._mana} points."]], tablefmt="fancy_outline") + "\n")

    # displays appropriate message
    def melee_attack(self, target):
        attempt, damage = super().melee_attack(target)
        if attempt <= self._accuracy and damage > 0:
            slowLinePrint(tabulate(
                [[f"You hit {target.name} and deal {damage} damage!"]], tablefmt="fancy_outline"))
        elif attempt <= self._accuracy and (damage - target.defense) > 0:
            slowLinePrint(tabulate(
                [[f"You attempt to attack with your {self._equippedWeapon.name}, but it glances off of their {target.equippedShield.name}!"]], tablefmt="fancy_outline"))

    # casts fireball on input target
    def cast_fireball(self, target):
        target.modify_attribute("health", -int((self._damage * 0.75) // 1))
        slowLinePrint(tabulate(
            [[f"The fire engulfs {target.name} and deals {int((self._damage * 0.75) // 1)} damage!"]], tablefmt="fancy_outline"))

    # adds/subtracts turns to shield duration
    def modify_shieldDuration(self, turns):
        if turns > 0 and self._shieldDuration > 0:
            slowLinePrint(tabulate(
                [["Your mana flows out to reinforce your protection."]], tablefmt="fancy_outline"))
        elif turns > 0:
            slowLinePrint(tabulate(
                [["Your mana surges out into a shining shield, helping to protect you from harm."]], tablefmt="fancy_outline"))
            self._defense = self._defense * 2
        self._shieldDuration += turns
        if self._shieldDuration == 0:
            slowLinePrint(tabulate([["Your shield flickers and dies."]],
                                   tablefmt="fancy_outline"))
            self._defense = self._defense / 2

    # equips selected item
    def equip_item(self, selected=Item()):
        if selected != self._equippedWeapon and selected != self._equippedShield:
            if selected.itemType == "Weapon":
                if selected.name != "Fists" and self._equippedWeapon.name != "Fists":
                    slowLinePrint(tabulate(
                        [[f"You stow away your {self._equippedWeapon.name} and equip your {selected.name}."]], tablefmt='fancy_outline') + "\n")
                elif self._equippedWeapon.name != "Fists":
                    slowLinePrint(tabulate(
                        [[f"You stow away your {self._equippedWeapon.name}."]], tablefmt="fancy_outline") + "\n")
                else:
                    slowLinePrint(tabulate(
                        [[f"You equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                self._equippedWeapon = selected
            if selected.itemType == "Shield":
                if selected.name != "Fists" and self._equippedShield.name != "Fists":
                    slowLinePrint(tabulate(
                        [[f"You stow away your {self._equippedShield} and equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                elif self._equippedShield.name != "Fists":
                    slowLinePrint(tabulate(
                        [[f"You stow away your {self._equippedShield.name}."]], tablefmt="fancy_outline") + "\n")
                else:
                    slowLinePrint(tabulate(
                        [[f"You equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                self._equippedShield = selected
        else:
            slowLinePrint(tabulate(
                [[f"You decided what you have is good enough for now."]], tablefmt="fancy_outline") + "\n")

    # opens player inventory
    def openInventory(self):
        while True:
            # displays full inventory
            slowLinePrint(self.inventory_table("Full"))
            try:
                # displays player options
                slowLinePrint(tabulate([["What would you like to do?"], ["1: Equip Weapon"], ["2: Equip Shield"], [
                    "3: Use Item"], ["4: Go Back"]], headers="firstrow", tablefmt="fancy_outline"))
                inventoryChoice = int(input("? "))
                print("")
            except:
                slowLinePrint(invalidChoice)
                continue
            match inventoryChoice:
                case 1:  # case 1 is equip weapon
                    # prints available weapons
                    slowLinePrint(
                        tabulate([["Which weapon would you like to equip?"]], tablefmt="fancy_grid"))
                    slowLinePrint(self.inventory_table("Weapon"))
                    try:
                        # gets player selection
                        weaponChoice = int(input("? "))
                        print("")
                    except:
                        slowLinePrint(invalidChoice)
                        continue
                    if weaponChoice > len(self._inventory["Weapon"]) + 1:
                        slowLinePrint(invalidChoice)
                        continue
                    # equips selected weapon
                    for count, weapon in enumerate(self._inventory["Weapon"]):
                        if count + 1 == weaponChoice:
                            self.equip_item(self._inventory["Weapon"][weapon])
                            continue
                    slowLinePrint(tabulate(
                        [[f"You decided what you have is good enough for now."]], tablefmt="fancy_outline") + "\n")
                case 2:  # case 2 is equip shield
                    # prints available shields
                    slowLinePrint(
                        tabulate([["Which shield would you like to equip?"]], tablefmt="fancy_grid"))
                    slowLinePrint(self.inventory_table("Shield"))
                    try:
                        # gets player selection
                        shieldChoice = int(input("? "))
                        print("")
                    except:
                        slowLinePrint(invalidChoice)
                        continue
                    if shieldChoice > len(self._inventory["Shield"]) + 1:
                        slowLinePrint(invalidChoice)
                        continue
                    # equips selected shield
                    for count, shield in enumerate(self._inventory["Shield"]):
                        if count + 1 == shieldChoice:
                            self.equip_item(self._inventory["Shield"][shield])
                            continue
                    slowLinePrint(tabulate(
                        [[f"You decided what you have is good enough for now."]], tablefmt="fancy_outline") + "\n")
                case 3:  # case 3 is use item
                    # prints available items
                    slowLinePrint(
                        tabulate([["Which item would you like to use?"]], tablefmt="fancy_grid"))
                    slowLinePrint(self.inventory_table("Consumable"))
                    try:
                        itemChoice = int(input("? "))  # gets player selection
                        slowLinePrint("")
                    except:
                        slowLinePrint(invalidChoice)
                        continue
                    if itemChoice > len(self._inventory["Consumable"]) + 1:
                        slowLinePrint(invalidChoice)
                        continue
                    # uses selected item
                    for count, item in enumerate(list(self._inventory["Consumable"].keys())):
                        if count + 1 == itemChoice:
                            self.use_item(self._inventory["Consumable"][item])
                            continue
                    slowLinePrint(
                        tabulate([["You decided against using anything."]], tablefmt="fancy_outline"))
                case 4:
                    break

    # uses selected item
    def use_item(self, item=Item()):
        if item.name in self._inventory["Consumable"]:
            if "Potion" in item.name:
                slowLinePrint(tabulate(
                    [[f"You pop the cork from the vial, and down the {item.name} within."]], tablefmt="fancy_outline") + "\n")
            else:
                slowLinePrint(tabulate(
                    [[f"You quickly scarf down the {item.name}."]], tablefmt="fancy_outline") + "\n")
            item.quantity = item.quantity - 1
            if item.quantity == 0:
                del self._inventory["Consumable"][item.name]

    # returns formatted inventory table representation
    def inventory_table(self, invType):
        equippedTable = []
        weaponTable = []
        shieldTable = []
        consumableTable = []
        if invType == "Full":
            for itemType in self._inventory:
                if itemType == "Equipped":
                    equippedTable.append([f"Equipment Slot", "Name", "Stats"])
                    equippedTable.append(
                        ["Weapon", self._equippedWeapon.name, f"+{self._equippedWeapon.stats['Damage']} Damage"])
                    equippedTable.append(
                        ["Shield", self._equippedShield.name, f"+{self._equippedShield.stats['Defense']} Defense"])
                elif itemType == "Weapon":
                    weaponTable.append([f"{itemType} Name", "Stats", "Amount"])
                    for item in self._inventory[itemType]:
                        if self._inventory[itemType][item].quantity > 0:
                            weaponTable.append(
                                [item, f"+{self._inventory[itemType][item].stats[list(self._inventory[itemType][item].stats.keys())[0]]} {list(self._inventory[itemType][item].stats.keys())[0]}", self._inventory[itemType][item].quantity])
                elif itemType == "Shield":
                    shieldTable.append([f"{itemType} Name", "Stats", "Amount"])
                    for item in self._inventory[itemType]:
                        if self._inventory[itemType][item].quantity > 0:
                            shieldTable.append(
                                [item, f"+{self._inventory[itemType][item].stats[list(self._inventory[itemType][item].stats.keys())[0]]} {list(self._inventory[itemType][item].stats.keys())[0]}", self._inventory[itemType][item].quantity])
                elif itemType == "Consumable":
                    consumableTable.append(
                        [f"{itemType} Name", "Effect", "Amount"])
                    for item in self._inventory[itemType]:
                        if self._inventory[itemType][item].quantity > 0:
                            consumableTable.append(
                                [item, f"+{self._inventory[itemType][item].stats[list(self._inventory[itemType][item].stats.keys())[0]]} {list(self._inventory[itemType][item].stats.keys())[0]}", self._inventory[itemType][item].quantity])
            return f"{tabulate(equippedTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}\n{tabulate(weaponTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}\n{tabulate(shieldTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}\n{tabulate(consumableTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}"
        elif invType == "Weapon":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].quantity > 0:
                    weaponTable.append(
                        [f"{count + 1}: {item}", f"{list(self._inventory[invType][item].stats.keys())[0]}: {self._inventory[invType][item].stats[list(self._inventory[invType][item].stats.keys())[0]]}"])
                if count + 1 == len(self._inventory[invType]):
                    weaponTable.append([f"{count + 2}: Go Back"])
            return tabulate(weaponTable, tablefmt="fancy_outline")
        elif invType == "Shield":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].quantity > 0:
                    shieldTable.append(
                        [f"{count + 1}: {item}", f"{list(self._inventory[invType][item].stats.keys())[0]}: {self._inventory[invType][item].stats[list(self._inventory[invType][item].stats.keys())[0]]}"])
                if count + 1 == len(self._inventory[invType]):
                    shieldTable.append([f"{count + 2}: Go Back"])
            return tabulate(shieldTable, tablefmt="fancy_outline")
        elif invType == "Consumable":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].quantity > 0:
                    consumableTable.append(
                        [f"{count + 1}: {item}", f"{list(self._inventory[invType][item].stats.keys())[0]}: {self._inventory[invType][item].stats[list(self._inventory[invType][item].stats.keys())[0]]}", self._inventory[invType][item].quantity])
                if count + 1 == len(self._inventory[invType]):
                    consumableTable.append([f"{count + 2}: Go Back"])
            return tabulate(consumableTable, tablefmt="fancy_outline")

    # returns formatted list representation
    def __str__(self):
        table = [["Name", "Level", "Health", "Mana", "Damage", "Defense"], [self._name, f"{self._level} {self._levelProgress}/{self._nextLevel}", f"{self._health}/{self._maxHealth}", f"{self._mana}/{self._maxMana}",
                                                                            f"{self._damage} + {self._equippedWeapon.stats['Damage']} ({self._equippedWeapon.name})", f"{self._defense} + {self._equippedShield.stats['Defense']} ({self._equippedShield.name})"]]
        if self._shieldDuration > 0:
            table[0].append("Enhance Shield")
            table[1].append(f"{self._shieldDuration} turns left")
            table[1][5] = f"{self._equippedShield.stats['Defense'] * 2} ({self._equippedShield.name} * 2)"
        return tabulate(table, headers='firstrow', tablefmt="fancy_outline", colalign=["left", "center"])


# enemy class
class Enemy(Entity):
    def __init__(self, name="", level=0, levelProgress=0, nextLevel=0, levelTable=[0, 0, 0, 0, 0, 0, 0, 0], health=0, maxHealth=0, mana=0, maxMana=0, damage=0, defense=0, accuracy=0, inventory={}, equippedWeapon=Item(), equippedShield=Item()):
        super().__init__(name, level, levelProgress, nextLevel, levelTable, health,
                         maxHealth, mana, maxMana, damage, defense, accuracy, inventory, equippedWeapon, equippedShield)

    def level_up(self, exp=0, level=0):
        super().level_up(exp, level)
        self._health = self._maxHealth
        self._mana = self._maxMana

    # modify specified attribute by adding/subtracting given value
    def modify_attribute(self, attribute, change):
        super().modify_attribute(attribute, change)
        # displays appropriate messages
        if attribute == "health":
            if change >= 1 and self._health + change < self._maxHealth:
                slowLinePrint(tabulate(
                    [[f"{self._name} is healed for {change} health points."]], tablefmt="fancy_outline"))
            elif change >= 1 and self._health != self._maxHealth:
                if self._maxHealth - self._health == 1:
                    slowLinePrint(tabulate(
                        [[f"{self._name} is healed for {self._maxHealth - self._health} health point."]], tablefmt="fancy_outline"))
                else:
                    slowLinePrint(tabulate(
                        [[f"{self._name} is healed for {self._maxHealth - self._health} health points."]], tablefmt="fancy_outline"))
        if attribute == "mana":
            if change > 1 and self._mana + change <= self._maxMana:
                slowLinePrint(tabulate(
                    [[f"{self._name}'s mana regenerates {change} points.\n"]], tablefmt="fancy_outline"))
            elif change < 1:
                slowLinePrint(tabulate(
                    [[f"{self._name}'s expends {change} mana."]], tablefmt="fancy_outline"))
            elif self._mana != 50:
                slowLinePrint(tabulate(
                    [[f"{self._name}'s mana regenerates {50 - self._mana} points."]], tablefmt="fancy_outline") + "\n")

    # displays appropriate message
    def melee_attack(self, target):
        attempt, damage = super().melee_attack(target)
        if attempt <= self._accuracy and damage > 0:
            slowLinePrint(tabulate(
                [[f"{self._name} hits you and deals {((self._damage + self._equippedWeapon.stats['Damage']) - (target.defense + target._equippedShield.stats['Defense']))} damage!"]], tablefmt="fancy_outline"))
        elif attempt <= self._accuracy and ((self._damage + self._equippedWeapon.stats["Damage"]) - target.defense) > 0:
            slowLinePrint(tabulate(
                [[f"{self._name} attempts to attack with its {self._equippedWeapon.name}, but you deflect it with your {target.equippedShield.name}!"]], tablefmt="fancy_outline"))
        else:
            slowLinePrint(tabulate(
                [[f"{self._name} tries to attack you, but misses."]], tablefmt="fancy_outline"))

    # displays death message, delete self from encounter
    def death(self, encounter):
        slowLinePrint(tabulate(
            [[f"{self._name} falls on the floor, dead."]], tablefmt="fancy_outline"))
        del encounter.enemies_dict[self._name]

    # returns formatted list representation
    def get_stats_list(self):
        table = [self._name, self._level, f"{self._health}/{self._maxHealth}", f"{self._mana}/{self._maxMana}",
                 f"{self._damage} + {self._equippedWeapon.stats['Damage']} ({self._equippedWeapon.name})", f"{self._defense} + {self._equippedShield.stats['Defense']} ({self._equippedShield.name})"]
        return table


"""# Testing
a = Player("Bobert")
a.reader({"_name": "Newbie", "_level": 5, "_levelProgress":0, "_nextLevel":100, "_health": 100, "_mana": 50, "_damage": 5, "_defense": 2, "_shield": 0, "_inventory": {"Equipped": {"Weapon": "Fists", "Shield": "Fists"}, "Weapon": {"Fists": {"stats": {"Damage": 0}, "quantity": 1}, "Wooden Sword": {"stats": {"Damage": 5}, "quantity": 1}}, "Shield": {"Fists": {"stats": {"Defense": 0}, "quantity": 1}, "Wooden Shield": {"stats": {"Defense": 2}, "quantity": 1}}, "Consumable": {"Burrito": {"stats": {"Health": 15}, "quantity": 3}, "Block of Cheese": {"stats": {"Health": 5}, "quantity": 1}}}})
b = Enemy("Gobbo")
c = Enemy("Reman")
b.reader({"_level":1, "_levelProgress":0, "_nextLevel":0, "_levelTable":[20, 10, 0, 0, 3, 3, 1, 1], "_health": 0, "_maxHealth": 0, "_mana":0, "_maxMana":0, "_damage": 0, "_accuracy": 0, "_inventory": {"Equipped": {"Weapon": "Fists", "Shield": "Fists"}, "Weapon": {"Fists": {"stats": {"Damage": 0}, "quantity": 1}, "Wooden Sword": {"stats": {"Damage": 5}, "quantity": 1}}, "Shield": {"Fists": {"stats": {"Defense": 0}, "quantity": 1}, "Wooden Shield": {"stats": {"Defense": 2}, "quantity": 1}}}, "quantity": 0})
c.reader({"_level":3, "_levelProgress":0, "_nextLevel":0, "_levelTable":[20, 10, 0, 0, 3, 3, 1, 1], "_health": 0, "_maxHealth": 0, "_mana":0, "_maxMana":0, "_damage": 0, "_accuracy": 0, "_inventory": {"Equipped": {"Weapon": "Fists", "Shield": "Fists"}, "Weapon": {"Fists": {"stats": {"Damage": 0}, "quantity": 1}, "Wooden Sword": {"stats": {"Damage": 5}, "quantity": 1}}, "Shield": {"Fists": {"stats": {"Defense": 0}, "quantity": 1}, "Wooden Shield": {"stats": {"Defense": 2}, "quantity": 1}}}, "quantity": 0})

slowLinePrint(a.__str__())
slowLinePrint(tabulate([["Name", "Level", "Health", "Mana", "Damage", "Defense"], b.get_stats_list(), c.get_stats_list()], headers="firstrow", tablefmt="fancy_outline"))"""
