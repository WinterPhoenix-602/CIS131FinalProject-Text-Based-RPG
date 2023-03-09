#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import json
from PlayerClass import Player
from EnemyClass import Enemy
from LocationTileClass import Tile
from datetime import datetime

invalidChoice = "I'm sorry, that is not a valid choice."

#the main function
def main():
    player, player_dict, tiles_dict, currentTile, tileCoords, saveFileName = loadGame(mainMenu())
    turn = 0
    if type(player_dict) != dict:
        exit()
    while True:
        turn, player, currentTile = combat(turn, player, currentTile)
        print(f"{currentTile.name}\n{currentTile.description}")        
        
        #displays tile menu
        tileCoords, choice, save = tileMenu(player, tileCoords)
        if choice == 6:
            if save == "yes":
                saveGame(player_dict, player, tiles_dict, tileCoords, currentTile, saveFileName)
            break
        
        try:
            currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
            #triggers passive actions
            turn, player = passiveActions(turn, player)
            turn += 1
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
            with open(f"NewGame.json","r") as saveFile:
                b=saveFile.readlines()
                saveFile.close()
            currentGame_dict = json.loads(b[0])
            player_dict = currentGame_dict["player"]
            tiles_dict = currentGame_dict["tiles"]
            tileCoords = currentGame_dict["location"]
            currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
            player.reader(player_dict)
            while True:
                player.name = input("Choose a name for your character (no more than seven characters long): ")
                if len(player.name) > 7:
                    print("I'm sorry, that name is too long.")
                    continue
                player_dict["name"] = player.name
                break
            saveFileName = "NewGame"
            return player, player_dict, tiles_dict, currentTile, tileCoords, saveFileName
        elif menuChoice == 2:
            try:
                with open(f"SaveFileInfo.json","r") as savesInfo:
                    a=savesInfo.readlines()
                    savesInfo.close()
                saveFiles_dict = json.loads(a[0])
                saveFiles_keyList = list(saveFiles_dict.keys())
                print("Which game save would you like to load?")
                for count, saveFile in enumerate(saveFiles_dict):
                    print(f"{count + 1}: {saveFiles_dict[saveFile]['name']} {saveFiles_dict[saveFile]['info']}")
                    if count + 1 == len(saveFiles_dict):
                        print("6: Go Back")
                try:
                    saveChoice = int(input("? "))                        
                except:
                    print(invalidChoice)
                    continue
                match saveChoice:
                    case 1:
                        saveFileName = saveFiles_keyList[0]
                    case 2:
                        saveFileName = saveFiles_keyList[1]
                    case 3:
                        saveFileName = saveFiles_keyList[2]
                    case 4:
                        saveFileName = saveFiles_keyList[3]
                    case 5:
                        saveFileName = saveFiles_keyList[4]
                    case 6:
                        player, player_dict, tiles_dict, currentTile, tileCoords, saveFileName = loadGame(mainMenu())
                        return player, player_dict, tiles_dict, currentTile, tileCoords, saveFileName
                    case _:
                        print(invalidChoice)
                        continue
                with open(f"{saveFileName}.json","r") as saveFile:
                    b=saveFile.readlines()
                    saveFile.close()
                currentGame_dict = json.loads(b[0])
                player_dict = currentGame_dict["player"]
                tiles_dict = currentGame_dict["tiles"]
                tileCoords = currentGame_dict["location"]
                currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
                player.reader(player_dict)
                return player, player_dict, tiles_dict, currentTile, tileCoords, saveFileName
            except FileNotFoundError:
                with open(f"NewGame.json","r") as saveFile:
                    b=saveFile.readlines()
                    saveFile.close()
                currentGame_dict = json.loads(b[0])
                player_dict = currentGame_dict["player"]
                tiles_dict = currentGame_dict["tiles"]
                tileCoords = currentGame_dict["location"]
                currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
                while True:
                    player.name = input("Choose a name for your character (no more than seven characters long): ")
                    if len(player.name) > 7:
                        print("I'm sorry, that name is too long.")
                        continue
                    player_dict["name"] = player.name
                    break
                return player, player_dict, tiles_dict, currentTile, tileCoords, saveFileName
        else:
            player_dict, tiles_dict, currentTile, tileCoords, saveFileName = 0, 0, 0, 0, 0
            return player, player_dict, tiles_dict, currentTile, tileCoords, saveFileName

#displays action menu for current tile
def tileMenu(player, tileCoords):
    save = ""
    while True:
        try:
            #print player status
            print(f"Name\tHealth\tMana\tDamage")
            player.print_stats()

            choice = int(input("What would you like to do?\n1: Go North\n2: Go East\n3: Go South\n4: Go West\n5: Open Inventory\n6: Exit Game\n? "))
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
                                print("Thank you for playing.")
                                save = "no"
                                return tileCoords, choice, save
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
    return tileCoords, choice, save

#processes combat
def combat(turn, player, currentTile):
    while len(currentTile.enemies_dict) > 0:
        #prints list of enemies and relevant stats
        currentTile.display_enemies()

        #print player status
        print(f"Name\tHealth\tMana\tDamage")
        player.print_stats()

        #allows players to use actions
        try:
            choice = int(input("What would you like to do?\n1: Melee Attack\n2: Cast Magic\n3: Use Item\n? ")) #displays options
        except:
            print(invalidChoice)
            continue

        match choice:
            case 1:
                if len(currentTile.enemies_dict) > 1:
                    print("Which enemy do you want to attack?") #displays target selection
                    for count, enemy in enumerate(currentTile.enemies_dict):
                        print(f"{count + 1}: {currentTile.enemies_dict[enemy].name}")
                    try:
                        attackEnemy = int(input("? ")) #gets selected target
                        if attackEnemy > len(currentTile.enemies_dict):
                            print(invalidChoice)
                            continue
                    except:
                        print(invalidChoice)
                        continue
                else:
                    attackEnemy = 1
                for count, enemy in enumerate(currentTile.enemies_dict): #damages selected target
                    if count + 1 == attackEnemy:
                        player.attack(currentTile.enemies_dict[enemy], player.damage)        
            case 2:
                try:
                    spell = int(input("What would you like to cast?\nName\t\tMana Cost\tEffect\n1: Fireball\t5\t\t8 Damage\n2: Shield\t15\t\tHalves Incoming Damage for 3 Turns\n3: Heal\t\tVariable\tConverts 2x Mana Cost to Health\n? "))
                    match spell:
                        case 1:
                            if player.mana >= 5:
                                player.modify_mana(-5)
                                if len(currentTile.enemies_dict) > 1:
                                    print("Which enemy do you want to attack?") #displays target selection
                                    for count, enemy in enumerate(currentTile.enemies_dict):
                                        print(f"{count + 1}: {currentTile.enemies_dict[enemy].name}")
                                    try:
                                        attackEnemy = int(input("? ")) #gets selected target
                                        if attackEnemy > len(currentTile.enemies_dict):
                                            print(invalidChoice)
                                            continue
                                    except:
                                        print(invalidChoice)
                                        continue
                                else:
                                    attackEnemy = 1
                                for count, enemy in enumerate(currentTile.enemies_dict): #damages selected target
                                    if count + 1 == attackEnemy:
                                        player.attack(currentTile.enemies_dict[enemy], 8)
                        case 2:
                            print("Not yet implemented.")
                            continue
                        case 3:
                            print("Not yet implemented.")
                            continue
                        case _:
                            print(invalidChoice)
                            continue
                except:
                    print(invalidChoice)
            case 3:
                print("Not yet implemented.")
                continue
            case _:
                print(invalidChoice)
                continue
        
        for enemy in currentTile.enemies_dict: #enemy turn(s)
            if currentTile.enemies_dict[enemy].health <= 0:
                currentTile.enemies_dict[enemy].death()
            else:
                currentTile.enemies_dict[enemy].attack(player)

        #triggers passive actions
        turn, player = passiveActions(turn, player)
        
        #removes dead enemies from enemies dictionary
        for i in list(currentTile.enemies_dict.keys()):
            if currentTile.enemies_dict[i].health <= 0:
                del currentTile.enemies_dict[i]

    for i in list(currentTile.enemies.keys()):
        del currentTile.enemies[i]
    return turn, player, currentTile

#saves current game
def saveGame(player_dict, player, tiles_dict, tileCoords, currentTile, saveFileName):
    currentGame_dict = {}
    player_dict["health"] = player.health
    player_dict["mana"] = player.mana
    currentGame_dict["player"] = player_dict
    currentGame_dict["tiles"] = tiles_dict
    currentGame_dict["location"] = tileCoords

    with open(f"SaveFileInfo.json","r") as saveInfo:
        a=saveInfo.readlines()
        saveInfo.close()
    saveFiles_dict = json.loads(a[0])
    saveFiles_keyList = list(saveFiles_dict.keys())

    if saveFileName == "NewGame":
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
                    saveFileName = saveFiles_keyList[0]
                case 2:
                    saveFileName = saveFiles_keyList[1]
                case 3:
                    saveFileName = saveFiles_keyList[2]
                case 4:
                    saveFileName = saveFiles_keyList[3]
                case 5:
                    saveFileName = saveFiles_keyList[4]
                case _:
                    print(invalidChoice)
                    continue
            break
        
    saveFiles_dict[saveFileName]["info"] = f"(Last Saved: {datetime.now().replace(microsecond = 0).isoformat(' ')} Location: {currentTile.name})"
    saveFiles_dict[saveFileName]["name"] = player_dict["name"]

    with open(f"SaveFileInfo.json","w") as saveInfo:
        json.dump(saveFiles_dict, saveInfo)
        saveInfo.close()

    with open(f"{saveFileName}.json","w") as saveFile:
        json.dump(currentGame_dict, saveFile)
        saveFile.close()
    print("Thank you for playing.")

#passive actions
def passiveActions(turn, player):
    turn += 1
    if turn % 2 == 0:
        player.modify_mana(5)
    if player.shield > 0:
        player.shield_turns(-1)
    return turn, player

main()
