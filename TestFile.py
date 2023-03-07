#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import json
from PlayerClass import Player
from EnemyClass import Enemy
from LocationTileClass import Tile

def main():
    player = Player()
    tileCoords = [0,0]
    currentTile = Tile()
    with open("DefaultTiles.json","r") as tilesFile:
        a=tilesFile.readlines()
        tilesFile.close()
    tiles_dict = json.loads(a[0])
    currentTile.reader(tiles_dict['tile' + str(tileCoords[0]) + str(tileCoords[1])])

    while True:
        player = combat(player, currentTile)
        print(f"{currentTile.name}\n{currentTile.description}")        
        tileCoords, tiles_dict, choice = menu(tileCoords, tiles_dict)

        if choice == 6:
            print("Thank you for playing.")
            break
        
        try:
            currentTile.reader(tiles_dict['tile' + str(tileCoords[0]) + str(tileCoords[1])])
        except KeyError:
            print("You can\'t go that way.\n__________________________________________________")
            match choice:
                case 1:
                    tileCoords[1] -= 1
                case 2:
                    tileCoords[0] -= 1
                case 3: 
                    tileCoords[1] += 1
                case 4:
                    tileCoords[0] += 1

def menu(tileCoords, tiles_dict):
    while True:
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
                    break
        except TypeError:
            print("I\'m sorry, that\'s not a valid choice.")
            continue
    return tileCoords, tiles_dict, choice

def combat(player, currentTile):
    while len(currentTile.enemies_dict) > 0:
        #prints list of enemies and relevant stats
        print(f"Name\t\tHealth\tDamage")
        print(f"__________________________________________________")
        for enemy in currentTile.enemies_dict:
            currentTile.enemies_dict[enemy].print_stats()
        print(f"__________________________________________________")

        #print player status
        print(f"Name\tHealth\tMana\tDamage")
        player.print_stats()

        #allows players to use actions
        try:
            choice = int(input("What would you like to do?\n1: Attack\n2: Magic\n? "))
        except:
            print("I\'m sorry, that\'s not a valid choice.")
            continue

        match choice:
            case 1:
                if len(currentTile.enemies_dict) > 0:
                    print("Which enemy do you want to attack?")
                    for count, enemy in enumerate(currentTile.enemies_dict):
                        print(f"{count + 1}: {currentTile.enemies_dict[enemy].name}")
                    try:
                        attackEnemy = int(input("? "))
                    except:
                        print("I'm sorry, that's not a valid choice.")
                        continue
                    for count, enemy in enumerate(currentTile.enemies_dict):
                        if count + 1 == attackEnemy:
                            currentTile.enemies_dict[enemy].modify_health(-player.damage)
                            print(f"You hit {currentTile.enemies_dict[enemy].name} and dealt {player.damage} damage!")
            case 2:
                print("Not yet implemented.")
        
        #removes dead enemies from enemies dictionary
        for i in list(currentTile.enemies_dict.keys()):
            if currentTile.enemies_dict[i].health <= 0:
                del currentTile.enemies_dict[i]
    return player

main()
