#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import json
import os
from PlayerClass import Player
from LocationTileClass import Tile
from datetime import datetime
from tabulate import tabulate

mainPath = os.path.dirname(__file__)
newGamePath = os.path.join(mainPath, "SaveFiles\\NewGame.json")
saveFileInfoPath = os.path.join(mainPath, "SaveFiles\\SaveFileInfo.json")
invalidChoice = "\n" + tabulate([["I'm sorry, that is not a valid choice."]]) + "\n"

#the main function
def main():
    player, player_dict, tiles_dict, currentTile, currentTileName, saveFilePath = loadGame(mainMenu())
    turn = 0
    if type(player_dict) != dict:
        exit()
    while True:
        if len(currentTile.get_combatEncounter().get_enemies()) > 0:
            currentTile.get_combatEncounter().start_encounter(player, turn)
            tiles_dict[currentTileName]["_combatEncounter"]["_triggerChance"] = currentTile.get_combatEncounter().get_triggerChance()

        #displays tile menu
        turn, currentTileName, choice, save = currentTile.tileMenu(turn, player, currentTileName)

        if choice == 6:
            if save == "yes":
                saveGame(player_dict, player, tiles_dict, currentTileName, currentTile, saveFilePath)
            player, player_dict, tiles_dict, currentTile, currentTileName, saveFilePath = loadGame(mainMenu())
            if type(player_dict) != dict:
                exit()
        
        try:
            currentTile.reader(tiles_dict[currentTileName])
            #triggers passive actions
        except KeyError:
            print("You can't go that way.\n__________________________________________________")

#displays main menu, choose between new game, loading save, or ending program
def mainMenu():
    while True:
        try:
            choice = int(input(tabulate([["1: New Game"], ["2: Load Game"], ["3: Exit"]], tablefmt="fancy_outline") + "\n? "))
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
            currentTileName = currentGame_dict["location"]
            currentTile.reader(tiles_dict[currentTileName])
            player.reader(player_dict)
            while True:
                player.set_name(input("Choose a name for your character (no more than seven characters long): "))
                if len(player.get_name()) > 7:
                    print("I'm sorry, that name is too long.")
                    continue
                print("")
                break
            saveFilePath = newGamePath
            return player, player_dict, tiles_dict, currentTile, currentTileName, saveFilePath
        elif menuChoice == 2:
            try:
                with open(saveFileInfoPath,"r") as savesInfo:
                    a=savesInfo.readlines()
                    savesInfo.close()
                saveFiles_dict = json.loads(a[0])
                loadMenuTable = [["Which game save would you like to load?"]]
                for count, saveFile in enumerate(saveFiles_dict):
                    loadMenuTable.append([f"{count + 1}: {saveFiles_dict[saveFile]['name']} {saveFiles_dict[saveFile]['info']}"])
                    if count + 1 == len(saveFiles_dict):
                        loadMenuTable.append(["6: Go Back"])
                print(tabulate(loadMenuTable, headers="firstrow", tablefmt="fancy_outline"))
                try:
                    saveChoice = int(input("? "))
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
                        player, player_dict, tiles_dict, currentTile, currentTileName, saveFilePath = loadGame(mainMenu())
                        return player, player_dict, tiles_dict, currentTile, currentTileName, saveFilePath
                    case _:
                        print(invalidChoice)
                        continue
                with open(saveFilePath,"r") as saveFile:
                    b=saveFile.readlines()
                    saveFile.close()
                currentGame_dict = json.loads(b[0])
                player_dict = currentGame_dict["player"]
                tiles_dict = currentGame_dict["tiles"]
                currentTileName = currentGame_dict["location"]
                currentTile.reader(tiles_dict[currentTileName])
                player.reader(player_dict)
                return player, player_dict, tiles_dict, currentTile, currentTileName, saveFilePath
            except FileNotFoundError:
                print(tabulate([["I'm sorry, that save slot is empty."]], tablefmt="fancy_outline"))
                continue
        else:
            player_dict, tiles_dict, currentTile, currentTileName, saveFilePath = 0, 0, 0, 0, 0
            return player, player_dict, tiles_dict, currentTile, currentTileName, saveFilePath

#saves current game
def saveGame(player_dict, player, tiles_dict, currentTileName, currentTile, saveFilePath):
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
    currentGame_dict["location"] = currentTileName

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
                        surety = input(f"\nThis will overwrite the current save for {saveFiles_dict[saveFiles_keyList[saveChoice - 1]]['name']}. Are you sure? (yes/no): ")
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
    print("\n" + tabulate([["Thank you for playing."]], tablefmt="fancy_outline") + "\n")
main()
