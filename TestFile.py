#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import sys
import json
from PlayerClass import Player
from InventoryClass import Inventory
from EnemyClass import Enemy
from LocationTileClass import Tile

def main():
    player = Player()
    inventory = Inventory()
    currentTile = Tile()
    
    #loads chosen save file
    while True:
        try:
            saveFileName = input("Input the name of your save file: ")
            with open(f"{saveFileName}.json","r") as saveFile:
                a=saveFile.readlines()
                saveFile.close()
            saveFile_dict = json.loads(a[0])
            player_dict = saveFile_dict["player"]
            tiles_dict = saveFile_dict["tiles"]
            tileCoords = saveFile_dict["location"]
            currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
            break
        except FileNotFoundError:
            print("I'm sorry, the file you entered does not exist.")
            continue

    while True:
        player, currentTile = combat(player, currentTile)
        print(f"{currentTile.name}\n{currentTile.description}")        
        
        #displays menu
        tileCoords, choice, save = menu(tileCoords, saveFile)
        if choice == 6:
            if save == "yes":
                saveFile_dict["player"] = player_dict
                saveFile_dict["tiles"] = tiles_dict
                saveFile_dict["location"] = tileCoords
                saveFileName = input("Input the name of your save file: ")
                with open(f"{saveFileName}.json","w") as saveFile:
                    json.dump(saveFile_dict, saveFile)
                    saveFile.close()
                print("Thank you for playing.")
            break
        
        try:
            currentTile.reader(tiles_dict["tile" + str(tileCoords[0]) + str(tileCoords[1])])
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

def menu(tileCoords, saveFile):
    while True:
        save = ""
        try:
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
                                print("I'm sorry, that is not a valid choice.")
                        else:
                                print("I'm sorry, that is not a valid choice.")
                    break
                case _:
                    print("I'm sorry, that's not a valid choice.")
                    continue
        except:
            print("I'm sorry, that's not a valid choice.")
            continue
    return tileCoords, choice, save

def combat(player, currentTile):
    while len(currentTile.enemies_dict) > 0:
        #prints list of enemies and relevant stats
        currentTile.display_enemies()

        #print player status
        print(f"Name\tHealth\tMana\tDamage")
        player.print_stats()

        #allows players to use actions
        try:
            choice = int(input("What would you like to do?\n1: Attack\n2: Magic\n3: Use Item\n? ")) #displays options
        except:
            print("I'm sorry, that's not a valid choice.")
            continue

        match choice:
            case 1:
                print("Which enemy do you want to attack?") #displays target selection
                for count, enemy in enumerate(currentTile.enemies_dict):
                    print(f"{count + 1}: {currentTile.enemies_dict[enemy].name}")
                try:
                    attackEnemy = int(input("? ")) #gets selected target
                    if attackEnemy > len(currentTile.enemies_dict):
                        print("I'm sorry, that's not a valid choice.")
                        continue
                except:
                    print("I'm sorry, that's not a valid choice.")
                    continue
                for count, enemy in enumerate(currentTile.enemies_dict): #damages selected target
                    if count + 1 == attackEnemy:
                        player.attack(currentTile.enemies_dict[enemy])        
            case 2:
                print("Not yet implemented.")
                continue
            case 3:
                print("Not yet implemented.")
                continue
            case _:
                print("I'm sorry, that's not a valid choice.")
                continue
        
        for enemy in currentTile.enemies_dict: #enemy turn(s)
            if currentTile.enemies_dict[enemy].health <= 0:
                currentTile.enemies_dict[enemy].death()
            else:
                currentTile.enemies_dict[enemy].attack(player)
        
        #removes dead enemies from enemies dictionary
        for i in list(currentTile.enemies_dict.keys()):
            if currentTile.enemies_dict[i].health <= 0:
                del currentTile.enemies_dict[i]
    for i in list(currentTile.enemies.keys()):
        del currentTile.enemies[i]
    return player, currentTile

main()
