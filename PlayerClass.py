# Caiden Wilson
# 3/2/2023
# CIS131
# Final Project: Player Class

from ItemClass import Item
from tabulate import tabulate

invalidChoice = "\n" + \
    tabulate([["I'm sorry, that is not a valid choice."]]) + "\n"


class Player:
    # initialization method
    def __init__(self, name="Player", level=1, levelProgress=0, nextLevel=100, health=100, maxHealth=100, mana=50, maxMana=50, damage=5, defense=2, shieldDuration=0, inventory={"itemType": {"itemName": Item()}}, equippedWeapon=Item(), equippedShield=Item()):
        self._name = name
        self._level = level
        self._levelProgress = levelProgress
        self._nextLevel = nextLevel
        self._health = health
        self._maxHealth = maxHealth
        self._mana = mana
        self._maxMana = maxMana
        self._damage = damage
        self._defense = defense
        self._shieldDuration = shieldDuration
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
    def shieldDuration(self):
        return self._shieldDuration

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
    def name(self, name):
        self._name = name

    @level.setter
    def level(self, level):
        self._level = level

    @health.setter
    def health(self, health):
        self._health = health

    @maxHealth.setter
    def maxHealth(self, maxHealth):
        self._maxHealth = maxHealth

    @mana.setter
    def mana(self, mana):
        self._mana = mana

    @maxMana.setter
    def maxMana(self, maxMana):
        self._maxMana = maxMana

    @damage.setter
    def damage(self, damage):
        self._damage = damage

    @defense.setter
    def defense(self, defense):
        self._defense = defense

    @shieldDuration.setter
    def shieldDuration(self, shieldDuration):
        self._shieldDuration = shieldDuration

    @inventory.setter
    def inventory(self, inventory):
        self._inventory = inventory

    @equippedWeapon.setter
    def equippedWeapon(self, equippedWeapon):
        self._equippedWeapon = equippedWeapon

    @equippedShield.setter
    def equippedShield(self, equippedShield):
        self._equippedShield = equippedShield

    # sets stats based on level
    def level_up(self, exp=0):
        if exp > 0:
            print(
                tabulate([[f"You gained {exp} experience."]], tablefmt="fancy_outline"))
            self._levelProgress += exp
            levelChange = 0
            while self._levelProgress >= self._nextLevel:
                self._levelProgress = self._levelProgress - self._nextLevel
                self._level += 1
                levelChange += 1
                self._nextLevel = self._level * 100
            if levelChange > 0:
                print(tabulate(
                    [[f"You leveled up! {self._level - levelChange} -> {self._level}"]], tablefmt="fancy_outline"))
        self._maxHealth = 100 + (50 * (self._level - 1))
        self._maxMana = 50 + (25 * (self._level - 1))
        self._damage = 5 + (5 * (self._level - 1))
        self._defense = 2 + (2 * (self._level - 1))

    # sets attributes from input dictionary, initializes inventory with item objects
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
        for itemType in self._inventory:
            if itemType != "Equipped":
                for item in self._inventory[itemType]:
                    self._inventory[itemType][item] = Item(
                        itemType, item, self._inventory[itemType][item]["stats"], self._inventory[itemType][item]["quantity"])
        self._equippedWeapon = self._inventory["Weapon"][self._inventory["Equipped"]["Weapon"]]
        self._equippedShield = self._inventory["Shield"][self._inventory["Equipped"]["Shield"]]

    # adds/subtracts value to health, displays appropriate message
    def modify_health(self, change):
        if change >= 1 and self._health + change <= self._maxHealth:
            self._health += change
            print(tabulate(
                [[f"You are healed for {change} health points."]], tablefmt="fancy_outline"))
        elif change < 1:
            self._health += change
        elif self._health + change > self._maxHealth:
            if self._maxHealth - self._health == 1:
                print(tabulate(
                    [[f"You are healed for {self._maxHealth - self._health} health point. Overspent a bit there."]], tablefmt="fancy_outline"))
            else:
                print(tabulate(
                    [[f"You are healed for {self._maxHealth - self._health} health points. Overspent a bit there."]], tablefmt="fancy_outline"))
            self._health += (self._maxHealth - self._health)

    # adds/subtracts value to mana, displays appropriate message
    def modify_mana(self, change):
        if change > 1 and self._mana + change <= self._maxMana:
            self._mana += change
            print(tabulate(
                [[f"Your mana regenerates {change} points.\n"]], tablefmt="fancy_outline"))
        elif change < 1:
            self._mana += change
            print(
                tabulate([[f"You expend {change} mana."]], tablefmt="fancy_outline"))
        elif self._mana != 50:
            print(tabulate(
                [[f"Your mana regenerates {50 - self._mana} points."]], tablefmt="fancy_outline") + "\n")
            self._mana += (50 - self._mana)

    # uses a melee attack on input target
    def melee_attack(self, target):
        target.modify_health(-(self._damage +
                             self._equippedWeapon.stats['Damage']))
        print(tabulate(
            [[f"You hit {target.name} and deal {self._damage + self._equippedWeapon.stats['Damage']} damage!"]], tablefmt="fancy_outline"))

    # casts fireball on input target
    def cast_fireball(self, target):
        target.modify_health(-8)
        print(tabulate(
            [[f"The fire engulfs {target.name} and deals 8 damage!"]], tablefmt="fancy_outline"))

    # adds/subtracts turns to shield duration
    def modify_shieldDuration(self, turns):
        if turns > 0 and self._shieldDuration > 0:
            print(tabulate(
                [["Your mana flows out to reinforce your protection."]], tablefmt="fancy_outline"))
        elif turns > 0:
            print(tabulate(
                [["Your mana surges out into a shining shield, helping to protect you from harm."]], tablefmt="fancy_outline"))
            self._defense = self._defense * 2
        self._shieldDuration += turns
        if self._shieldDuration == 0:
            print(tabulate([["Your shield flickers and dies."]],
                  tablefmt="fancy_outline"))
            self._defense = self._defense / 2

    # equips selected item
    def equip_item(self, selected=Item()):
        if selected != self._equippedWeapon and selected != self._equippedShield:
            if selected.itemType == "Weapon":
                if selected.name != "Fists" and self._equippedWeapon.name != "Fists":
                    print(tabulate(
                        [[f"You stow away your {self._equippedWeapon.name} and equip your {selected.name}."]], tablefmt='fancy_outline') + "\n")
                elif self._equippedWeapon.name != "Fists":
                    print(tabulate(
                        [[f"You stow away your {self._equippedWeapon.name}."]], tablefmt="fancy_outline") + "\n")
                else:
                    print(tabulate(
                        [[f"You equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                self._equippedWeapon = selected
            if selected.itemType == "Shield":
                if selected.name != "Fists" and self._equippedShield.name != "Fists":
                    print(tabulate(
                        [[f"You stow away your {self._equippedShield} and equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                elif self._equippedShield.name != "Fists":
                    print(tabulate(
                        [[f"You stow away your {self._equippedShield.name}."]], tablefmt="fancy_outline") + "\n")
                else:
                    print(tabulate(
                        [[f"You equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                self._equippedShield = selected
        else:
            print(tabulate(
                [[f"You decided what you have is good enough for now."]], tablefmt="fancy_outline") + "\n")

    # uses selected item
    def use_item(self, item=Item()):
        if item.name in self._inventory["Consumable"]:
            if "Potion" in item.name:
                print(tabulate(
                    [[f"You pop the cork from the vial, and down the {item.name} within."]], tablefmt="fancy_outline") + "\n")
            else:
                print(tabulate(
                    [[f"You quickly scarf down the {item.name}."]], tablefmt="fancy_outline") + "\n")
            item.quantity = item.quantity - 1
            if item.quantity == 0:
                del self._inventory["Consumable"][item.name]

    def openInventory(self):
        while True:
            print(self.inventory_table("Full"))
            try:
                inventoryChoice = int(input(tabulate([["What would you like to do?"], ["1: Equip Weapon"], ["2: Equip Shield"], [
                                      "3: Use Item"], ["4: Go Back"]], headers="firstrow", tablefmt="fancy_outline") + "\n? "))
                print("")
            except:
                print(invalidChoice)
                continue
            match inventoryChoice:
                case 1:
                    print(
                        tabulate([["Which weapon would you like to equip?"]], tablefmt="fancy_grid"))
                    print(self.inventory_table("Weapon"))
                    try:
                        weaponChoice = int(input("? "))
                        print("")
                    except:
                        print(invalidChoice)
                        continue
                    if weaponChoice > len(self._inventory["Weapon"]):
                        print(invalidChoice)
                        continue
                    for count, weapon in enumerate(self._inventory["Weapon"]):
                        if count + 1 == weaponChoice:
                            self.equip_item(self._inventory["Weapon"][weapon])
                            continue
                case 2:
                    print(
                        tabulate([["Which shield would you like to equip?"]], tablefmt="fancy_grid"))
                    print(self.inventory_table("Shield"))
                    try:
                        shieldChoice = int(input("? "))
                        print("")
                    except:
                        print(invalidChoice)
                        continue
                    if shieldChoice > len(self._inventory["Shield"]):
                        print(invalidChoice)
                        continue
                    for count, shield in enumerate(self._inventory["Shield"]):
                        if count + 1 == shieldChoice:
                            self.equip_item(self._inventory["Shield"][shield])
                            continue
                case 3:
                    print(
                        tabulate([["Which item would you like to use?"]], tablefmt="fancy_grid"))
                    print(self.inventory_table("Consumable"))
                    try:
                        itemChoice = int(input("? "))
                        print("")
                    except:
                        print(invalidChoice)
                        continue
                    if itemChoice > len(self._inventory["Consumable"]):
                        print(invalidChoice)
                        continue
                    for count, item in enumerate(list(self._inventory["Consumable"].keys())):
                        if count + 1 == itemChoice:
                            self.use_item(self._inventory["Consumable"][item])
                            continue
                case 4:
                    break

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
            return tabulate(weaponTable, tablefmt="fancy_outline")
        elif invType == "Shield":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].quantity > 0:
                    shieldTable.append(
                        [f"{count + 1}: {item}", f"{list(self._inventory[invType][item].stats.keys())[0]}: {self._inventory[invType][item].stats[list(self._inventory[invType][item].stats.keys())[0]]}"])
            return tabulate(shieldTable, tablefmt="fancy_outline")
        elif invType == "Consumable":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].quantity > 0:
                    consumableTable.append(
                        [f"{count + 1}: {item}", f"{list(self._inventory[invType][item].stats.keys())[0]}: {self._inventory[invType][item].stats[list(self._inventory[invType][item].stats.keys())[0]]}", self._inventory[invType][item].quantity])
            return tabulate(consumableTable, tablefmt="fancy_outline")

    # returns formatted list representation
    def __str__(self):
        table = [["Name", "Level", "Health", "Mana", "Damage", "Defense"], [self._name, f"{self._level} {self._levelProgress}/{self._nextLevel}", f"{self._health}/{self._maxHealth}", f"{self._mana}/{self._maxMana}",
                                                                            f"{self._damage} + {self._equippedWeapon.stats['Damage']} ({self._equippedWeapon.name})", f"{self._defense} + {self._equippedShield.stats['Defense']} ({self._equippedShield.name})"]]
        if self._shieldDuration > 0:
            table[0].append("Enhance Shield")
            table[1].append(f"{self._shieldDuration} turns left")
            table[1][4] = f"{self._equippedShield.stats['Defense'] * 2} ({self._equippedShield.name} * 2)"
        return tabulate(table, headers='firstrow', tablefmt="fancy_outline", colalign=["left", "center"])


# Testing
'''a = Player
a.reader({"_name": "Newbie", "_level": 1, "_levelProgress":0, "_nextLevel":100, "_health": 100, "_mana": 50, "_damage": 5, "_defense": 2, "_shield": 0, "_inventory": {"Equipped": {"Weapon": "Fists", "Shield": "Fists"}, "Weapon": {"Fists": {"stats": {"Damage": 0}, "quantity": 1}, "Wooden Sword": {"stats": {"Damage": 5}, "quantity": 1}}, "Shield": {"Fists": {"stats": {"Defense": 0}, "quantity": 1}, "Wooden Shield": {"stats": {"Defense": 2}, "quantity": 1}}, "Consumable": {"Burrito": {"stats": {"Health": 15}, "quantity": 3}, "Block of Cheese": {"stats": {"Health": 5}, "quantity": 1}}}})
print(a)
a.level_up(1042)
print(a)'''
