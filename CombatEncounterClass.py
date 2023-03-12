#Caiden Wilson
#3/10/2023
#Final Project: Combat Encounter Class

import textwrap
from EnemyClass import Enemy
from PlayerClass import Player
from tabulate import tabulate
from random import randint

invalidChoice = "I'm sorry, that is not a valid choice.\n"

class CombatEncounter:
    def __init__(self, name = "", startDescription = [""], enemies = {}, endDescription = [""], triggerChance = [0, 0]):
        self._name = name
        self._startDescription = startDescription
        self._enemies = enemies
        self._enemies_dict = {}
        self._endDescription = endDescription
        self._triggerChance = triggerChance

    #getters
    def get_name(self):
        return self._name
    def get_startDescription(self):
        return "\n\n".join(self._startDescription)
    def get_enemies(self):
        return self._enemies
    def get_enemies_dict(self):
        return self._enemies_dict
    def get_endDescription(self):
        return "\n\n".join(self._endDescription)
    def get_triggerChance(self):
        return self._triggerChance
    
    #setters
    def set_name(self, name):
        self._name = name
    def set_startDescription(self, startDescription):
        self._startDescription = startDescription
    def set_enemies(self, enemies):
        self._enemies = enemies
    def set_enemies_dict(self, enemies_dict):
        self._enemies_dict = enemies_dict
    def set_endDescription(self, endDescription):
        self._endDescription = endDescription
    def set_triggerChance(self, triggerChance):
        self._triggerChance = triggerChance

    #sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
                if key == "_startDescription":
                    for count, paragraph in enumerate(self._startDescription):
                        self._startDescription[count] = textwrap.fill(self._startDescription[count], 100)
                if key == "_enemies":
                    for enemy in self._enemies:
                        for quantity in range(self._enemies[enemy]["quantity"]):
                            a = Enemy(f"{enemy} {quantity + 1}")
                            a.reader(self._enemies[enemy])
                            self._enemies_dict[f"{enemy} {quantity + 1}"] = a
                if key == "_endDescription":
                    for count, paragraph in enumerate(self._endDescription):
                        self._endDescription[count] = textwrap.fill(self._endDescription[count], 100)
            except:
                print("No such attribute, please consider adding it in init.")

    def start_encounter(self, player = Player(), turn = 0):
        for enemy in self._enemies:
            for quantity in range(self._enemies[enemy]["quantity"]):
                a = Enemy(f"{enemy} {quantity + 1}")
                a.reader(self._enemies[enemy])
                self._enemies_dict[f"{enemy} {quantity + 1}"] = a
        if randint(1, 100) <= self._triggerChance[0] and len(self._enemies_dict) > 0 and turn > 0:
            print(tabulate([["\n\n".join(self._startDescription)]], tablefmt="fancy_grid") + "\n") #prints long encounter start description
            print(self.encounterText() + "\n") #prints simple encounter start description
            while len(self._enemies_dict) > 0:
                print(f"{self.__str__()}") #displays enemy stats

                print(player) #displays player stats

                #displays combat actions, gets choice of player
                try:
                    choice = int(input("\nWhat would you like to do?\n1: Melee Attack\n2: Cast Magic\n3: Use Item\n? "))
                    print("")
                except:
                    print(invalidChoice)
                    continue

                #fulfills action chosen by player
                match choice:
                    #case 1 is melee attack
                    case 1:
                        if len(self._enemies_dict) > 1:
                            #displays target selection
                            print("Which enemy do you want to attack?") 
                            for count, enemy in enumerate(self._enemies_dict):
                                print(f"{count + 1}: {self._enemies_dict[enemy].get_name()}")
                            #gets target selection from player
                            try:
                                attackEnemy = int(input("? "))
                                print("")
                                if attackEnemy > len(self._enemies_dict):
                                    print(invalidChoice)
                                    continue
                            except:
                                print(invalidChoice)
                                continue
                        #if only one enemy is present, they are the target by default
                        else:
                            attackEnemy = 1
                        #damages selected target
                        for count, enemy in enumerate(self._enemies_dict):
                            if count + 1 == attackEnemy:
                                player.melee_attack(self._enemies_dict[enemy])
                    #case 2 is casting magic
                    case 2:
                        #displays available spells, gets spell selection from player
                        try:
                            spell = int(input("What would you like to cast?\nName\t\tMana Cost\tEffect\n1: Fireball\t5\t\tDeals 8 Damage to All Enemies\n2: Shield\t15\t\tHalves Incoming Damage for 3 Turns\n3: Heal\t\tVariable\tConverts 2x Mana Cost to Health\n? "))
                            print("")
                        except:
                            print(invalidChoice)
                            continue
                        #casts spell chosen by player
                        match spell:
                            #case 1 is fireball
                            case 1:
                                if player.get_mana() >= 5:
                                    player.modify_mana(-5)
                                    for count, enemy in enumerate(self._enemies_dict):
                                        player.cast_fireball(self._enemies_dict[enemy])
                                else:
                                    print("Insufficient mana.\n")
                                    continue
                            #case 2 is shield
                            case 2:
                                if player.get_mana() >= 15:
                                    player.modify_mana(-15)
                                    player.modify_shieldDuration(3)
                                else:
                                    print("Insufficient mana.\n")
                                    continue
                            #case 3 is heal
                            case 3:
                                #gets input mana from player
                                try:
                                    heal = int(input("How much mana will you expend? "))
                                except:
                                    print("Not a valid amount of mana.")
                                    continue
                                if heal <= player.get_mana() and heal > 0:
                                    player.modify_mana(-heal)
                                    player.modify_health(heal * 2)
                                elif heal <= 0:
                                    print("You can't expend less than 1 mana.")
                                    continue
                                else:
                                    print("You don't have enough mana.")
                                    continue
                            case _:
                                print(invalidChoice)
                                continue
                    #case 3 is using an item
                    case 3:
                        print("Not yet implemented.")
                        continue
                    case _:
                        print(invalidChoice)
                        continue
                
                print("") #adds newline between player and enemy turn

                #enemies take their turns
                for enemy in list(self._enemies_dict.keys()):
                    if self._enemies_dict[enemy].get_health() <= 0:
                        self._enemies_dict[enemy].death(self)
                    else:
                        self._enemies_dict[enemy].attack(player)
                                    
                print("") #adds newline after enemy turns

                turn = self.passive_actions(turn, player) #triggers passive actions
            print(tabulate([["\n\n".join(self._startDescription)]], tablefmt="fancy_grid")) #prints long encounter end description
            self._triggerChance[0] = self._triggerChance[1] #sets trigger chance to what it should be after the first encounter
        
    #displays encountered enemies
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
                    
    #passive actions
    def passive_actions(self, turn, player):
        turn += 1
        if turn % 2 == 0:
            player.modify_mana(5)
        if player.get_shieldDuration() > 0:
            player.modify_shieldDuration(-1)
            if player.get_shieldDuration() == 0:
                print("Your shield flickers and dies.")
        return turn

    #returns formatted table representation
    def __str__(self):
        enemyTable = [["Enemy Name", "Health", "Damage"]]
        for enemy in self._enemies_dict:
            enemyTable.append([self._enemies_dict[enemy].get_name(), self._enemies_dict[enemy].get_health(), self._enemies_dict[enemy].get_damage()])
        return tabulate(enemyTable, tablefmt="fancy_grid")

'''#Testing
p = Player()
p.reader({"_name": "Newbie", "_health": 100, "_mana": 50, "_damage": 1, "_defense": 1, "_shield": 0, "_inventory": {"Equipped": {"Weapon": "Fists", "Shield": "Wooden Shield"}, "Weapon": {"Fists": {"stats": {"Damage": 1}, "quantity": 1}, "Wooden Sword": {"stats": {"Damage": 5}, "quantity": 1}}, "Shield": {"Fists": {"stats": {"Defense": 1}, "quantity": 1}, "Wooden Shield": {"stats": {"Defense": 2}, "quantity": 1}}, "Consumable": {"Burrito": {"stats": {"Health": 15}, "quantity": 3}}}})
x = CombatEncounter()
x.reader({"_name":"Ambush", "_startDescription":["As you make your way towards the village, your peaceful reverie is abruptly shattered by the sudden appearance of two goblins. They emerge from behind a nearby rock, their beady eyes fixed on you with a mixture of curiosity and hostility. The goblins are small, barely up to your waist, with green skin, pointy ears, and long, sharp teeth.", "As they step out of hiding, they brandish crude weapons made of wood and rusted metal, and let out a guttural snarl. You can see that they're clearly spoiling for a fight, their stance aggressive and threatening."], "_enemies": {"Goblin":{"_health": 20, "_maxHealth": 20, "_damage": 2, "_accuracy": 50, "quantity": 2}}, "_endDescription":["The goblins lie motionless on the ground, their weapons clattering to the earth beside them. You take a moment to catch your breath, your heart pounding with the adrenaline of the fight. You're glad to have emerged victorious, but you know that there may be more dangers ahead as you continue on your journey towards the village."], "_triggerChance":[100, 10]})
t = 1
x.start_encounter(p, t)'''
