#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import json
import os
from PlayerClass import Player
from EnemyClass import Enemy
from LocationTileClass import Tile
from datetime import datetime

invalidChoice = "I'm sorry, that is not a valid choice."
mainPath = os.path.dirname(__file__)
newGamePath = os.path.join(mainPath, "SaveFiles\\NewGame.json")
saveFileInfoPath = os.path.join(mainPath, "SaveFiles\\SaveFileInfo.json")

#the main function
def main():
    player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath = loadGame(mainMenu())
    turn = 0
    if type(player_dict) != dict:
        exit()
    while True:
        turn, player, currentTile = combat(turn, player, currentTile)
        print(f"{currentTile.get_name()}\n{currentTile.get_description()}")        
        
        #displays tile menu
        turn, tileCoords, choice, save = tileMenu(turn, player, tileCoords)
        if choice == 6:
            if save == "yes":
                saveGame(player_dict, player, tiles_dict, tileCoords, currentTile, saveFilePath)
            player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath = loadGame(mainMenu())
            if type(player_dict) != dict:
                exit()
        
        try:
            currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
            #triggers passive actions
            turn, player = passiveActions(turn, player)
        except KeyError:
            print("You can't go that way.\n__________________________________________________")
            match choice:
                case 1:
                    tileCoords[1] -= 1
                case 2:
                    tileCoords[0] -= 1
                case 3: 
                    tileCoords[1] += 1
                case 4:
                    tileCoords[0] += 1

#displays main menu, choose between new game, loading save, or ending program
def mainMenu():
    while True:
        try:
            choice = int(input("1: New Game\n2: Load Game\n3: Exit\n? "))
            if choice < 1 or choice > 3:
                print(invalidChoice)
                continue
        except:
            print(invalidChoice)
            continue
        return choice

#loads saved game
def loadGame(menuChoice):
    #loads chosen save file
    currentTile = Tile()
    player = Player()
    while True:
        if menuChoice == 1:
            with open(newGamePath,"r") as saveFile:
                b=saveFile.readlines()
                saveFile.close()
            currentGame_dict = json.loads(b[0])
            player_dict = currentGame_dict["player"]
            tiles_dict = currentGame_dict["tiles"]
            tileCoords = currentGame_dict["location"]
            currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
            player.reader(player_dict)
            while True:
                player.set_name(input("Choose a name for your character (no more than seven characters long): "))
                print("")
                if len(player.get_name()) > 7:
                    print("I'm sorry, that name is too long.")
                    continue
                break
            saveFilePath = newGamePath
            return player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath
        elif menuChoice == 2:
            try:
                with open(saveFileInfoPath,"r") as savesInfo:
                    a=savesInfo.readlines()
                    savesInfo.close()
                saveFiles_dict = json.loads(a[0])
                print("Which game save would you like to load?")
                for count, saveFile in enumerate(saveFiles_dict):
                    print(f"{count + 1}: {saveFiles_dict[saveFile]['name']} {saveFiles_dict[saveFile]['info']}")
                    if count + 1 == len(saveFiles_dict):
                        print("6: Go Back")
                try:
                    saveChoice = int(input("? "))
                    print("")
                except:
                    print(invalidChoice)
                    continue
                match saveChoice:
                    case 1:
                        saveFilePath = os.path.join(mainPath, "SaveFiles\\Save1.json")
                    case 2:
                        saveFilePath = os.path.join(mainPath, "SaveFiles\\Save2.json")
                    case 3:
                        saveFilePath = os.path.join(mainPath, "SaveFiles\\Save3.json")
                    case 4:
                        saveFilePath = os.path.join(mainPath, "SaveFiles\\Save4.json")
                    case 5:
                        saveFilePath = os.path.join(mainPath, "SaveFiles\\Save5.json")
                    case 6:
                        player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath = loadGame(mainMenu())
                        return player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath
                    case _:
                        print(invalidChoice)
                        continue
                with open(saveFilePath,"r") as saveFile:
                    b=saveFile.readlines()
                    saveFile.close()
                currentGame_dict = json.loads(b[0])
                player_dict = currentGame_dict["player"]
                tiles_dict = currentGame_dict["tiles"]
                tileCoords = currentGame_dict["location"]
                currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
                player.reader(player_dict)
                return player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath
            except FileNotFoundError:
                print("I'm sorry, that save slot is empty.\n")
                continue
        else:
            player_dict, tiles_dict, currentTile, tileCoords, saveFilePath = 0, 0, 0, 0, 0
            return player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath

#displays action menu for current tile
def tileMenu(turn, player, tileCoords):
    save = ""
    while True:
        try:
            #print player status
            print(f"Name\tHealth\tMana\tDamage")
            print(player.__str__())
            print("")

            choice = int(input("What would you like to do?\n1: Go North\n2: Go East\n3: Go South\n4: Go West\n5: Open Inventory\n6: Exit Game\n? "))
            print("")
            match choice:
                case 1:
                    tileCoords[1] += 1
                    break
                case 2:
                    tileCoords[0] += 1
                    break
                case 3: 
                    tileCoords[1] -= 1
                    break
                case 4:
                    tileCoords[0] -= 1
                    break
                case 5:
                    print("Yet to be implemented.")
                    continue
                case 6:
                    while True:
                        save = input("Would you like to save your progress? (yes/no): ")
                        if save == "yes":
                            break
                        elif save == "no":
                            save = input("Are you sure? (yes/no): ")
                            if save == "yes":
                                print("\nThank you for playing.\n")
                                save = "no"
                                return turn, tileCoords, choice, save
                            elif save == "no":
                                continue
                            else:
                                print(invalidChoice)
                        else:
                                print(invalidChoice)
                    break
                case _:
                    print(invalidChoice)
                    continue
        except:
            print(invalidChoice)
            continue
    return turn, tileCoords, choice, save

#processes combat
def combat(turn, player, currentTile):
    
    if len(currentTile.get_enemies_dict()) > 0:
        encounterText(currentTile)

    while len(currentTile.get_enemies_dict()) > 0:
        #prints list of enemies and relevant stats
        currentTile.display_enemies()

        #print player status
        print(f"Name\tHealth\tMana\tDamage")
        print(player.__str__())

        #allows players to use actions
        try:
            choice = int(input("\nWhat would you like to do?\n1: Melee Attack\n2: Cast Magic\n3: Use Item\n? ")) #displays options
            print("")
        except:
            print(invalidChoice)
            continue

        match choice:
            case 1:
                if len(currentTile.get_enemies_dict()) > 1:
                    print("Which enemy do you want to attack?") #displays target selection
                    for count, enemy in enumerate(currentTile.get_enemies_dict()):
                        print(f"{count + 1}: {currentTile.get_enemies_dict()[enemy].get_name()}")
                    try:
                        attackEnemy = int(input("? ")) #gets selected target
                        print("")
                        if attackEnemy > len(currentTile.get_enemies_dict()):
                            print(invalidChoice)
                            continue
                    except:
                        print(invalidChoice)
                        continue
                else:
                    attackEnemy = 1
                for count, enemy in enumerate(currentTile.get_enemies_dict()): #damages selected target
                    if count + 1 == attackEnemy:
                        player.attack(currentTile.get_enemies_dict()[enemy], "melee")
            case 2:
                try:
                    spell = int(input("What would you like to cast?\nName\t\tMana Cost\tEffect\n1: Fireball\t5\t\tDeals 8 Damage to All Enemies\n2: Shield\t15\t\tHalves Incoming Damage for 3 Turns\n3: Heal\t\tVariable\tConverts 2x Mana Cost to Health\n? "))
                    print("")
                    match spell:
                        case 1:
                            if player.get_mana() >= 5:
                                player.modify_mana(-5)
                                for count, enemy in enumerate(currentTile.get_enemies_dict()):
                                    player.attack(currentTile.get_enemies_dict()[enemy], "fireball")
                            else:
                                print("Insufficient mana.\n")
                                continue
                        case 2:
                            if player.get_mana() >= 15:
                                player.modify_mana(-15)
                                player.modify_shieldDuration(3)
                            else:
                                print("Insufficient mana.\n")
                                continue
                        case 3:
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
                except:
                    print(invalidChoice)
                    continue
            case 3:
                print("Not yet implemented.")
                continue
            case _:
                print(invalidChoice)
                continue
        
        print("")
        for enemy in currentTile.get_enemies_dict(): #enemy turn(s)
            if currentTile.get_enemies_dict()[enemy].get_health() <= 0:
                currentTile.get_enemies_dict()[enemy].death()
            else:
                currentTile.get_enemies_dict()[enemy].attack(player)
        print("")

        #triggers passive actions
        turn, player = passiveActions(turn, player)
        
        #removes dead enemies from enemies dictionary
        for i in list(currentTile.get_enemies_dict().keys()):
            if currentTile.get_enemies_dict()[i].get_health() <= 0:
                del currentTile.get_enemies_dict()[i]

    for i in list(currentTile.get_enemies().keys()):
        currentTile.set_enemies({})
    return turn, player, currentTile

#displays encountered enemies
def encounterText(currentTile):
    if len(currentTile.get_enemies_dict()) == 1:
        enemy = list(currentTile.get_enemies().keys())
        print(f"You ran into a {enemy[0]}!")
    elif len(currentTile.get_enemies_dict()) > 1 and len(currentTile.get_enemies_dict()) < 6:
        print("You ran into a group of", end = " ")
    elif len(currentTile.get_enemies_dict()) >= 6:
        print("You ran into a horde of", end = " ")
    for count, enemy in enumerate(currentTile.get_enemies()):
        if len(currentTile.get_enemies()) < 2 and len(currentTile.get_enemies_dict()) != 1:
            print(f"{currentTile.get_enemies()[enemy]['quantity']} {enemy}s!")
        elif len(currentTile.get_enemies()) < 3 and len(currentTile.get_enemies_dict()) != 1:
            if count + 1 != len(currentTile.get_enemies()):
                if currentTile.get_enemies()[enemy]['quantity'] <= 1:
                    print(f"{currentTile.get_enemies()[enemy]['quantity']} {enemy} and", end = " ")
                else:
                    print(f"{currentTile.get_enemies()[enemy]['quantity']} {enemy}s and", end = " ")
            else:
                if currentTile.get_enemies()[enemy]['quantity'] <= 1:
                    print(f"{currentTile.get_enemies()[enemy]['quantity']} {enemy}!")
                else:
                    print(f"{currentTile.get_enemies()[enemy]['quantity']} {enemy}s!")
        elif len(currentTile.get_enemies_dict()) != 1:
            if count + 1 != len(currentTile.get_enemies()):
                if currentTile.get_enemies()[enemy]['quantity'] <= 1:
                    print(f"{currentTile.get_enemies()[enemy]['quantity']} {enemy},", end = " ")
                else:
                    print(f"{currentTile.get_enemies()[enemy]['quantity']} {enemy}s,", end = " ")
            else:
                if currentTile.get_enemies()[enemy]['quantity'] <= 1:
                    print(f"and {currentTile.get_enemies()[enemy]['quantity']} {enemy}!")
                else:
                    print(f"and {currentTile.get_enemies()[enemy]['quantity']} {enemy}s!")

#saves current game
def saveGame(player_dict, player, tiles_dict, tileCoords, currentTile, saveFilePath):
    currentGame_dict = {}
    player_dict["_name"] = player.get_name()
    player_dict["_health"] = player.get_health()
    player_dict["_mana"] = player.get_mana()
    currentGame_dict["player"] = player_dict
    currentGame_dict["tiles"] = tiles_dict
    currentGame_dict["location"] = tileCoords

    with open(saveFileInfoPath,"r") as saveInfo:
        a=saveInfo.readlines()
        saveInfo.close()
    saveFiles_dict = json.loads(a[0])
    saveFiles_keyList = list(saveFiles_dict.keys())

    if saveFilePath == newGamePath:
        while True:
            print("Which slot would you like to save your progress in?")
            for count, saveFile in enumerate(saveFiles_dict):
                print(f"{count + 1}: {saveFiles_dict[saveFile]['name']} {saveFiles_dict[saveFile]['info']}")
            try:
                saveChoice = int(input("? "))
                if saveChoice > len(saveFiles_dict):
                    print(invalidChoice)
                    continue
                while True:
                    if saveFiles_dict[saveFiles_keyList[saveChoice - 1]]["info"] != "(Empty)":
                        surety = input(f"This will overwrite the current game in {saveFiles_dict[saveFiles_keyList[saveChoice - 1]]['name']}. Are you sure? (yes/no): ")
                        if surety == "no":
                            break
                        elif surety == "yes":
                            break
                        else:
                            print(invalidChoice)
                            continue
                    else:
                        surety = ""
                        break
                if surety == "no":
                    continue
            except:
                print(invalidChoice)
                continue
            match saveChoice:
                case 1:
                    saveFilePath = os.path.join(mainPath, "SaveFiles\\Save1.json")
                case 2:
                    saveFilePath = os.path.join(mainPath, "SaveFiles\\Save2.json")
                case 3:
                    saveFilePath = os.path.join(mainPath, "SaveFiles\\Save3.json")
                case 4:
                    saveFilePath = os.path.join(mainPath, "SaveFiles\\Save4.json")
                case 5:
                    saveFilePath = os.path.join(mainPath, "SaveFiles\\Save5.json")
                case _:
                    print(invalidChoice)
                    continue
            break
        
        saveFiles_dict["Save" + str(saveChoice)]["name"] = player_dict["_name"]
    saveFiles_dict["Save" + str(saveChoice)]["info"] = f"(Last Saved: {datetime.now().replace(microsecond = 0).isoformat(' ')} Location: {currentTile.get_name()})"

    with open(saveFileInfoPath,"w") as saveInfo:
        json.dump(saveFiles_dict, saveInfo)
        saveInfo.close()

    with open(saveFilePath,"w") as saveFile:
        json.dump(currentGame_dict, saveFile)
        saveFile.close()
    print("\nThank you for playing.\n")

#passive actions
def passiveActions(turn, player):
    turn += 1
    if turn % 2 == 0:
        player.modify_mana(5)
    if player.get_shieldDuration() > 0:
        player.modify_shieldDuration(-1)
        if player.get_shieldDuration() == 0:
            print("Your shield flickers and dies.")
    return turn, player

main()
