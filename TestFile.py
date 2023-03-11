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

invalidChoice = "I'm sorry, that is not a valid choice.\n"
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
        if len(currentTile.get_combatEncounter().get_enemies()) > 0:
            currentTile.get_combatEncounter().start_encounter(player, turn)
            tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])]["_combatEncounter"]["_triggerChance"] = currentTile.get_combatEncounter().get_triggerChance()
        print(f"{currentTile.get_name()}\n\n{currentTile.get_description()}\n")        
        
        #displays tile menu
        turn, player, tileCoords, choice, save = tileMenu(turn, player, tileCoords)
        if choice == 6:
            if save == "yes":
                saveGame(player_dict, player, tiles_dict, tileCoords, currentTile, saveFilePath)
            player, player_dict, tiles_dict, currentTile, tileCoords, saveFilePath = loadGame(mainMenu())
            if type(player_dict) != dict:
                exit()
        
        try:
            currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
            #triggers passive actions
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
        #print player status
        print(player)
        print("")
        try:
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
                    player = openInventory(player)
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
                                return turn, player, tileCoords, choice, save
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
    return turn, player, tileCoords, choice, save

def openInventory(player):
    while True:
        print(player.get_inventory_table("Full"))
        try:
            inventoryChoice = int(input("\nWhat would you like to do?\n1: Equip Weapon\n2: Equip Shield\n3: Use Item\n4: Go Back\n? "))
            print("")
            match inventoryChoice:
                case 1:
                    print("Which weapon would you like to equip?")
                    print(player.get_inventory_table("Weapon"))
                    try:
                        weaponChoice = int(input("? "))
                        print("")
                        if weaponChoice > len(player.get_inventory()["Weapon"]):
                            print(invalidChoice)
                            continue
                        for count, weapon in enumerate(player.get_inventory()["Weapon"]):
                            if count + 1 == weaponChoice:
                                player.equip_item(player.get_inventory()["Weapon"][weapon])
                                continue
                    except:
                        print(invalidChoice)
                        continue
                case 2:
                    print("Which shield would you like to equip?")
                    print(player.get_inventory_table("Shield"))
                    try:
                        shieldChoice = int(input("? "))
                        print("")
                        if shieldChoice > len(player.get_inventory()["Shield"]):
                            print(invalidChoice)
                            continue
                        for count, shield in enumerate(player.get_inventory()["Shield"]):
                            if count + 1 == shieldChoice:
                                player.equip_item(player.get_inventory()["Shield"][shield])
                                continue
                    except:
                        print(invalidChoice)
                        continue
                case 3:
                    print("Which item would you like to use?")
                    print(player.get_inventory_table("Consumable"))
                    try:
                        itemChoice = int(input("? "))
                        print("")
                        if itemChoice > len(player.get_inventory()["Consumable"]):
                            print(invalidChoice)
                            continue
                        for count, item in enumerate(player.get_inventory()["Consumable"]):
                            if count + 1 == itemChoice:
                                player.use_item(item)
                                continue
                    except:
                        print(invalidChoice)
                        continue
                case 4:
                    return player
        except:
            print(invalidChoice)
            continue

#saves current game
def saveGame(player_dict, player, tiles_dict, tileCoords, currentTile, saveFilePath):
    currentGame_dict = {}
    player_dict["_name"] = player.get_name()
    player_dict["_health"] = player.get_health()
    player_dict["_mana"] = player.get_mana()
    for itemType in player.get_inventory():
        if itemType != "Equipped":
            for item in player.get_inventory()[itemType]:
                player_dict["_inventory"][itemType][item] = {"stats":player.get_inventory()[itemType][item].get_stats(), "quantity":player.get_inventory()[itemType][item].get_quantity()}
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
                        surety = input(f"This will overwrite the current save for {saveFiles_dict[saveFiles_keyList[saveChoice - 1]]['name']}. Are you sure? (yes/no): ")
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

main()
