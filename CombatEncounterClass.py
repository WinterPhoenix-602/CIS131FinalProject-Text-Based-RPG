# Caiden Wilson
# 3/10/2023
# Final Project: Combat Encounter Class

import textwrap
from EntityClasses import Enemy
from EntityClasses import Player
from tabulate import tabulate
from random import randint
from SlowPrint import slowTablePrint

invalidChoice = "\n" + \
    tabulate([["I'm sorry, that is not a valid choice."]], tablefmt="fancy_outline") + "\n"


class CombatEncounter:
    def __init__(self, name="", startDescription=[""], enemies={}, endDescription=[""], expReward=0, triggerChance=[0, 0]):
        self._name = name
        self._startDescription = startDescription
        self._enemies = enemies
        self._enemies_dict = {}
        self._endDescription = endDescription
        self._expReward = expReward
        self._triggerChance = triggerChance

    # getters
    @property
    def name(self):
        return self._name

    @property
    def startDescription(self):
        return "\n\n".join(self._startDescription)

    @property
    def enemies(self):
        return self._enemies

    @property
    def enemies_dict(self):
        return self._enemies_dict

    @property
    def endDescription(self):
        return "\n\n".join(self._endDescription)

    @property
    def expReward(self):
        return self._expReward

    @property
    def triggerChance(self):
        return self._triggerChance

    # setters
    @name.setter
    def name(self, name):
        self._name = name

    @startDescription.setter
    def startDescription(self, startDescription):
        self._startDescription = startDescription

    @enemies.setter
    def enemies(self, enemies):
        self._enemies = enemies

    @enemies_dict.setter
    def enemies_dict(self, enemies_dict):
        self._enemies_dict = enemies_dict

    @endDescription.setter
    def endDescription(self, endDescription):
        self._endDescription = endDescription

    @expReward.setter
    def expReward(self, expReward):
        self._expReward = expReward

    @triggerChance.setter
    def triggerChance(self, triggerChance):
        self._triggerChance = triggerChance

    # sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue
            if key == "_startDescription":
                for count, paragraph in enumerate(self._startDescription):
                    self._startDescription[count] = textwrap.fill(
                        self._startDescription[count], 100)
            if key == "_endDescription":
                for count, paragraph in enumerate(self._endDescription):
                    self._endDescription[count] = textwrap.fill(
                        self._endDescription[count], 100)

    # runs combat encounter
    def start_encounter(self, player=Player(), turn=0):
        for enemy in self._enemies:
            for quantity in range(self._enemies[enemy]["quantity"]):
                a = Enemy(f"{enemy} {quantity + 1}")
                a.reader(self._enemies[enemy])
                self._enemies_dict[f"{enemy} {quantity + 1}"] = a
        if randint(1, 100) <= self._triggerChance[0] and len(self._enemies_dict) > 0 and turn > 0:
            for enemy in self._enemies_dict:
                self._expReward += randint(self._enemies_dict[enemy].maxHealth // 4, self._enemies_dict[enemy].maxHealth // 2) + self._enemies_dict[enemy].damage + \
                    self._enemies_dict[enemy].defense + self._enemies_dict[enemy].equippedWeapon.stats["Damage"] + \
                    self._enemies_dict[enemy].equippedShield.stats["Defense"]
            slowTablePrint(tabulate([[self.encounterText()], ["\n\n".join(self._startDescription)]],
                  tablefmt="fancy_grid") + "\n")  # prints encounter start description
            while len(self._enemies_dict) > 0:
                slowTablePrint(f"{self.__str__()}")  # displays enemy stats

                slowTablePrint(player.__str__())  # displays player stats

                # displays combat actions, gets choice of player
                try:
                    slowTablePrint(f"{tabulate([['What would you like to do?'], ['1: Melee Attack'], ['2: Cast Magic'], ['3: Use Item']], headers='firstrow', tablefmt='fancy_outline')}")
                    choice = int(input("? "))
                    print("")
                except:
                    slowTablePrint(invalidChoice)
                    continue

                # fulfills action chosen by player
                match choice:
                    # case 1 is melee attack
                    case 1:
                        if len(self._enemies_dict) > 1:
                            # displays target selection
                            enemyTable = [
                                ["Which enemy do you want to attack?"]]
                            for count, enemy in enumerate(self._enemies_dict):
                                enemyTable.append(
                                    [f"{count + 1}: {self._enemies_dict[enemy].name}"])
                            slowTablePrint(tabulate(enemyTable, headers="firstrow",
                                  tablefmt="fancy_outline"))
                            # gets target selection from player
                            try:
                                attackEnemy = int(input("? "))
                                print("")
                                if attackEnemy > len(self._enemies_dict):
                                    slowTablePrint(invalidChoice)
                                    continue
                            except:
                                slowTablePrint(invalidChoice)
                                continue
                        # if only one enemy is present, they are the target by default
                        else:
                            attackEnemy = 1
                        # damages selected target
                        for count, enemy in enumerate(self._enemies_dict):
                            if count + 1 == attackEnemy:
                                player.melee_attack(self._enemies_dict[enemy])
                    # case 2 is casting magic
                    case 2:
                        # displays available spells, gets spell selection from player
                        try:
                            slowTablePrint(tabulate([["What would you like to cast?"]], tablefmt="fancy_outline") + "\n" + tabulate([["Name", "Mana Cost", "Effect"], ["1: Fireball", 5, "Deals 75% Base Damage to All Enemies"], [
                                        "2: Force Shield", 15, "Doubles Defense for 3 Turns"], ["3: Heal", "Variable", "Converts 2x Mana Cost to Health"]], headers="firstrow", tablefmt="fancy_outline"))
                            spell = int(input("? "))
                            print("")
                        except:
                            slowTablePrint(invalidChoice)
                            continue
                        # casts spell chosen by player
                        match spell:
                            # case 1 is fireball
                            case 1:
                                if player.mana >= 5:
                                    player.modify_attribute("mana", -5)
                                    for count, enemy in enumerate(self._enemies_dict):
                                        player.cast_fireball(
                                            self._enemies_dict[enemy])
                                else:
                                    print("Insufficient mana.\n")
                                    continue
                            # case 2 is shield
                            case 2:
                                if player.mana >= 15:
                                    player.modify_attribute("mana", -15)
                                    player.modify_shieldDuration(3)
                                else:
                                    print("Insufficient mana.\n")
                                    continue
                            # case 3 is heal
                            case 3:
                                # gets input mana from player
                                try:
                                    heal = int(
                                        input("How much mana will you expend? "))
                                except:
                                    print("Not a valid amount of mana.")
                                    continue
                                if heal <= player.mana and heal > 0:
                                    player.modify_mana(-heal)
                                    player.modify_health(heal * 2)
                                elif heal <= 0:
                                    print("You can't expend less than 1 mana.")
                                    continue
                                else:
                                    print("You don't have enough mana.")
                                    continue
                            case _:
                                slowTablePrint(invalidChoice)
                                continue
                    # case 3 is using an item
                    case 3:
                        # prints available items
                        slowTablePrint(
                            tabulate([["Which item would you like to use?"]], tablefmt="fancy_grid"))
                        slowTablePrint(player.inventory_table("Consumable"))
                        try:
                            # gets player selection
                            itemChoice = int(input("? "))
                            print("")
                        except:
                            slowTablePrint(invalidChoice)
                            continue
                        if itemChoice > len(player.inventory["Consumable"]) + 1:
                            slowTablePrint(invalidChoice)
                            continue
                        # uses selected item
                        for count, item in enumerate(list(player.inventory["Consumable"].keys())):
                            if count + 1 == itemChoice:
                                player.use_item(
                                    player.inventory["Consumable"][item])
                                continue
                            slowTablePrint(
                                tabulate([["You decided against using anything."]], tablefmt="fancy_outline"))
                    case _:
                        slowTablePrint(invalidChoice)
                        continue

                print("")  # adds newline between player and enemy turn

                # enemies take their turns
                for enemy in list(self._enemies_dict.keys()):
                    if self._enemies_dict[enemy].health <= 0:
                        self._enemies_dict[enemy].death(self)
                    else:
                        self._enemies_dict[enemy].melee_attack(player)

                print("")  # adds newline after enemy turns

                # triggers passive actions
                turn = self.passive_actions(turn, player)
            # prints long encounter end description
            slowTablePrint(
                tabulate([["\n\n".join(self._endDescription)]], tablefmt="fancy_grid"))
            player.level_up(self._expReward)
            # sets trigger chance to what it should be after the first encounter
            self._triggerChance[0] = self._triggerChance[1]

    # displays encountered enemies
    def encounterText(self):
        encounterText = ""
        if len(self._enemies_dict) == 1:
            enemy = list(self._enemies.keys())
            encounterText += f"You ran into a {enemy[0]}!"
            return encounterText
        elif len(self._enemies_dict) == 2 and len(self._enemies) == 1:
            enemy = list(self._enemies.keys())
            encounterText += f"You ran into a pair of {enemy[0]}s!"
            return encounterText
        elif len(self._enemies_dict) > 1 and len(self._enemies_dict) < 6:
            encounterText += "You ran into a group of "
        elif len(self._enemies_dict) >= 6:
            encounterText += "You ran into a horde of "
        for count, enemy in enumerate(self._enemies):
            if len(self._enemies) < 2 and len(self._enemies_dict) != 1:
                encounterText += f"{self._enemies[enemy]['quantity']} {enemy}s!"
                return encounterText
            elif len(self._enemies) < 3 and len(self._enemies_dict) != 1:
                if count + 1 != len(self._enemies):
                    if self._enemies[enemy]['quantity'] <= 1:
                        encounterText += f"{self._enemies[enemy]['quantity']} {enemy} and "
                    else:
                        encounterText += f"{self._enemies[enemy]['quantity']} {enemy}s and "
                else:
                    if self._enemies[enemy]['quantity'] <= 1:
                        encounterText += f"{self._enemies[enemy]['quantity']} {enemy}!"
                        return encounterText
                    else:
                        encounterText += f"{self._enemies[enemy]['quantity']} {enemy}s!"
                        return encounterText
            elif len(self._enemies_dict) != 1:
                if count + 1 != len(self._enemies):
                    if self._enemies[enemy]['quantity'] <= 1:
                        encounterText += f"{self._enemies[enemy]['quantity']} {enemy}, "
                    else:
                        encounterText += f"{self._enemies[enemy]['quantity']} {enemy}s, "
                else:
                    if self._enemies[enemy]['quantity'] <= 1:
                        encounterText += f"and {self._enemies[enemy]['quantity']} {enemy}!"
                        return encounterText
                    else:
                        encounterText += f"and {self._enemies[enemy]['quantity']} {enemy}s!"
                        return encounterText

    # passive actions
    def passive_actions(self, turn, player=Player()):
        turn += 1
        if turn % 2 == 0:
            player.modify_attribute("mana", 5)
        if player.shieldDuration > 0:
            player.modify_shieldDuration(-1)
        return turn

    # returns formatted table representation
    def __str__(self):
        enemyTable = [["Enemy Name", "Level",
                       "Health", "Mana", "Damage", "Defense"]]
        for enemy in self._enemies_dict:
            enemyTable.append(self._enemies_dict[enemy].get_stats_list())
        return tabulate(enemyTable, headers="firstrow", tablefmt="fancy_outline")


'''# Testing
p = Player()
p.reader({"_name": "Newbie", "_health": 100, "_mana": 50, "_damage": 1, "_defense": 1, "_shield": 0, "_inventory": {"Equipped": {"Weapon": "Fists", "Shield": "Wooden Shield"}, "Weapon": {"Fists": {"stats": {"Damage": 1}, "quantity": 1}, "Wooden Sword": {"stats": {"Damage": 5}, "quantity": 1}}, "Shield": {"Fists": {"stats": {"Defense": 1}, "quantity": 1}, "Wooden Shield": {"stats": {"Defense": 2}, "quantity": 1}}, "Consumable": {"Burrito": {"stats": {"Health": 15}, "quantity": 3}}}})
x = CombatEncounter()
x.reader({"_name":"Ambush", "_startDescription":["As you make your way towards the village, your peaceful reverie is abruptly shattered by the sudden appearance of two goblins. They emerge from behind a nearby rock, their beady eyes fixed on you with a mixture of curiosity and hostility. The goblins are small, barely up to your waist, with green skin, pointy ears, and long, sharp teeth.", "As they step out of hiding, they brandish crude weapons made of wood and rusted metal, and let out a guttural snarl. You can see that they're clearly spoiling for a fight, their stance aggressive and threatening."], "_enemies": {"Goblin":{"_health": 20, "_maxHealth": 20, "_damage": 2, "_accuracy": 50, "quantity": 2}}, "_endDescription":["The goblins lie motionless on the ground, their weapons clattering to the earth beside them. You take a moment to catch your breath, your heart pounding with the adrenaline of the fight. You're glad to have emerged victorious, but you know that there may be more dangers ahead as you continue on your journey towards the village."], "_triggerChance":[100, 10]})
t = 1
x.start_encounter(p, t)'''
