#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Player Class

from ItemClass import Item
from tabulate import tabulate

invalidChoice = "\n" + tabulate([["I'm sorry, that is not a valid choice."]]) + "\n"

class Player:
    #initialization method
    def __init__(self, name = "Player", health = 100, maxHealth = 100, mana = 50, maxMana = 50, damage = 1, defense = 1, shieldDuration = 0, inventory = {"itemType":{"itemName":Item()}}, equippedWeapon = Item(), equippedShield = Item()):
        self._name = name
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
    def get_equippedWeapon(self):
        return self._equippedWeapon
    def get_equippedShield(self):
        return self._equippedShield
    
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
    def set_equippedWeapon(self, equippedWeapon):
        self._equippedWeapon = equippedWeapon
    def set_equippedShield(self, equippedShield):
        self._equippedShield = equippedShield

    #sets attributes from input dictionary, initializes inventory with item objects
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
                    self._inventory[itemType][item] = Item(itemType, item, self._inventory[itemType][item]["stats"], self._inventory[itemType][item]["quantity"])
        self._equippedWeapon = self._inventory["Weapon"][self._inventory["Equipped"]["Weapon"]]
        self._damage = self._equippedWeapon.get_stats()["Damage"]
        self._equippedShield = self._inventory["Shield"][self._inventory["Equipped"]["Shield"]]
        self._defense = self._equippedShield.get_stats()["Defense"]
    
    #adds/subtracts value to health, displays appropriate message
    def modify_health(self, change):
        if change >= 1 and self._health + change <= self._maxHealth:
            self._health += change
            print(tabulate([[f"You are healed for {change} health points."]], tablefmt="fancy_outline"))
        elif change < 1:
            self._health += change
        elif self._health + change > self._maxHealth:
            if self._maxHealth - self._health == 1:
                print(tabulate([[f"You are healed for {self._maxHealth - self._health} health point. Overspent a bit there."]], tablefmt="fancy_outline"))
            else:
                print(tabulate([[f"You are healed for {self._maxHealth - self._health} health points. Overspent a bit there."]], tablefmt="fancy_outline"))
            self._health += (self._maxHealth - self._health)

    #adds/subtracts value to mana, displays appropriate message
    def modify_mana(self, change):
        if change > 1 and self._mana + change < 50:
            self._mana += change
            print(tabulate([[f"Your mana regenerates {change} points.\n"]], tablefmt="fancy_outline"))
        elif change < 1:
            self._mana += change
            print(tabulate([[f"You expend {change} mana."]], tablefmt="fancy_outline"))
        elif self._mana != 50:
            print(tabulate([[f"Your mana regenerates {50 - self._mana} points."]], tablefmt="fancy_outline") + "\n")
            self._mana += (50 - self._mana)

    #uses a melee attack on input target
    def melee_attack(self, target):
        target.modify_health(-(self._damage))
        print(tabulate([[f"You hit {target.get_name()} and deal {self._damage} damage!"]], tablefmt="fancy_outline"))
    
    #casts fireball on input target
    def cast_fireball(self, target):
        target.modify_health(-8)
        print(tabulate([[f"The fire engulfs {target.get_name()} and deals 8 damage!"]], tablefmt="fancy_outline"))

    #adds/subtracts turns to shield duration
    def modify_shieldDuration(self, turns):
        if turns > 0 and self._shieldDuration > 0:
            print(tabulate([["Your mana flows out to reinforce your enhancement."]], tablefmt="fancy_outline"))
        elif turns > 0:
            print(tabulate([["Your mana surges out into your shield, helping to protect you from harm."]], tablefmt="fancy_outline"))
            self._defense = self._equippedShield.get_stats()["Defense"] * 2
        self._shieldDuration += turns
        if self._shieldDuration == 0:
            print(tabulate([["Your shield flickers and dies."]], tablefmt="fancy_outline"))
            self._defense = self._equippedShield.get_stats()["Defense"]
    
    #equips selected item
    def equip_item(self, selected = Item()):            
        if selected != self._equippedWeapon and selected != self._equippedShield:
            if selected.get_itemType() == "Weapon":
                if selected.get_name() != "Fists"and self._equippedWeapon.get_name() != "Fists":
                    print(tabulate([[f"You stow away your {self._equippedWeapon.get_name()} and equip your {selected.get_name()}."]], tablefmt='fancy_outline') +"\n")
                elif self._equippedWeapon.get_name() != "Fists":
                    print(tabulate([[f"You stow away your {self._equippedWeapon.get_name()}."]], tablefmt="fancy_outline") + "\n")
                else:
                    print(tabulate([[f"You equip your {selected.get_name()}."]], tablefmt="fancy_outline") + "\n")
                self._equippedWeapon = selected
                self._damage = selected.get_stats()["Damage"]
            if selected.get_itemType() == "Shield":
                if selected.get_name() != "Fists" and self._equippedShield.get_name() != "Fists":
                    print(tabulate([[f"You stow away your {self._equippedShield} and equip your {selected.get_name()}."]], tablefmt="fancy_outline") + "\n")
                elif self._equippedShield.get_name() != "Fists":
                    print(tabulate([[f"You stow away your {self._equippedShield.get_name()}."]], tablefmt="fancy_outline") + "\n")
                else:
                    print(tabulate([[f"You equip your {selected.get_name()}."]], tablefmt="fancy_outline") + "\n")
                self._equippedShield = selected
                self._defense = selected.get_stats()["Defense"]
        else:
            print(tabulate([[f"You decided what you have is good enough for now."]], tablefmt="fancy_outline") + "\n")
    
    #uses selected item
    def use_item(self, item = Item()):
        if item.get_name() in self._inventory["Consumable"]:
            if "Potion" in item.get_name():
                print(tabulate([[f"You pop the cork from the vial, and down the {item.get_name()} within."]], tablefmt="fancy_outline") + "\n")
            else:
                print(tabulate([[f"You quickly scarf down the {item.get_name()}."]], tablefmt="fancy_outline") + "\n")
            item.set_quantity(item.get_quantity() - 1)
            if item.get_quantity() == 0:
                del self._inventory["Consumable"][item.get_name()]

    def openInventory(self):
        while True:
            print(self.get_inventory_table("Full"))
            try:
                inventoryChoice = int(input(tabulate([["What would you like to do?"], ["1: Equip Weapon"], ["2: Equip Shield"], ["3: Use Item"], ["4: Go Back"]], headers="firstrow", tablefmt="fancy_outline") + "\n? "))
                print("")
            except:
                print(invalidChoice)
                continue
            match inventoryChoice:
                case 1:
                    print(tabulate([["Which weapon would you like to equip?"]], tablefmt="fancy_grid"))
                    print(self.get_inventory_table("Weapon"))
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
                    print(tabulate([["Which shield would you like to equip?"]], tablefmt="fancy_grid"))
                    print(self.get_inventory_table("Shield"))
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
                    print(tabulate([["Which item would you like to use?"]], tablefmt="fancy_grid"))
                    print(self.get_inventory_table("Consumable"))
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

    #returns formatted inventory table representation
    def get_inventory_table(self, invType):
        equippedTable = []
        weaponTable = []
        shieldTable = []
        consumableTable = []
        if invType == "Full":
            for itemType in self._inventory:
                if itemType == "Equipped":
                    equippedTable.append([f"Equipment Slot", "Name", "Stats"])
                    equippedTable.append(["Weapon", self._equippedWeapon.get_name(), f"Damage: {self._equippedWeapon.get_stats()['Damage']}"])
                    equippedTable.append(["Shield", self._equippedShield.get_name(), f"Defense: {self._equippedShield.get_stats()['Defense']}"])
                elif itemType == "Weapon":
                    weaponTable.append([f"{itemType} Name", "Stats", "Amount"])
                    for item in self._inventory[itemType]:
                        if self._inventory[itemType][item].get_quantity() > 0:
                            weaponTable.append([item, f"{list(self._inventory[itemType][item].get_stats().keys())[0]}: {self._inventory[itemType][item].get_stats()[list(self._inventory[itemType][item].get_stats().keys())[0]]}", self._inventory[itemType][item].get_quantity()])
                elif itemType == "Shield":
                    shieldTable.append([f"{itemType} Name", "Stats", "Amount"])
                    for item in self._inventory[itemType]:
                        if self._inventory[itemType][item].get_quantity() > 0:
                            shieldTable.append([item, f"{list(self._inventory[itemType][item].get_stats().keys())[0]}: {self._inventory[itemType][item].get_stats()[list(self._inventory[itemType][item].get_stats().keys())[0]]}", self._inventory[itemType][item].get_quantity()])
                elif itemType == "Consumable":
                    consumableTable.append([f"{itemType} Name", "Stats", "Amount"])
                    for item in self._inventory[itemType]:
                        if self._inventory[itemType][item].get_quantity() > 0:
                            consumableTable.append([item, f"{list(self._inventory[itemType][item].get_stats().keys())[0]}: {self._inventory[itemType][item].get_stats()[list(self._inventory[itemType][item].get_stats().keys())[0]]}", self._inventory[itemType][item].get_quantity()])
            return f"{tabulate(equippedTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}\n{tabulate(weaponTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}\n{tabulate(shieldTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}\n{tabulate(consumableTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'center', 'left'))}"
        elif invType == "Weapon":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].get_quantity() > 0:
                    weaponTable.append([f"{count + 1}: {item}", f"{list(self._inventory[invType][item].get_stats().keys())[0]}: {self._inventory[invType][item].get_stats()[list(self._inventory[invType][item].get_stats().keys())[0]]}"])
            return tabulate(weaponTable, tablefmt="fancy_outline")
        elif invType == "Shield":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].get_quantity() > 0:
                    shieldTable.append([f"{count + 1}: {item}", f"{list(self._inventory[invType][item].get_stats().keys())[0]}: {self._inventory[invType][item].get_stats()[list(self._inventory[invType][item].get_stats().keys())[0]]}"])
            return tabulate(shieldTable, tablefmt="fancy_outline")
        elif invType == "Consumable":
            for count, item in enumerate(self._inventory[invType]):
                if self._inventory[invType][item].get_quantity() > 0:
                    consumableTable.append([f"{count + 1}: {item}", f"{list(self._inventory[invType][item].get_stats().keys())[0]}: {self._inventory[invType][item].get_stats()[list(self._inventory[invType][item].get_stats().keys())[0]]}", self._inventory[invType][item].get_quantity()])
            return tabulate(consumableTable, tablefmt="fancy_outline")
    
    #returns formatted list representation
    def __str__(self):
        table = [["Name", "Health", "Mana", "Damage", "Defense"], [self._name, self._health, self._mana, f"{self._equippedWeapon.get_stats()['Damage']} ({self._equippedWeapon.get_name()})", f"{self._equippedShield.get_stats()['Defense']} ({self._equippedShield.get_name()})"]]
        if self._shieldDuration > 0:
            table[0].append("Enhance Shield")
            table[1].append(f"{self._shieldDuration} turns left")
            table[1][4] = f"{self._equippedShield.get_stats()['Defense'] * 2} ({self._equippedShield.get_name()} * 2)"
        return tabulate(table, headers='firstrow', tablefmt="fancy_outline")
