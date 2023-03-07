#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import json
from PlayerClass import Player
from EnemyClass import Enemy
from LocationTileClass import Tile

def menu(tileCoords, tiles_dict):
    while True:
        try:
            choice = int(input('What would you like to do?\n1: Go North\n2: Go East\n3: Go South\n4: Go West\n5: Open Inventory\n6: Exit Game\n? '))
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
                    print('Yet to be implemented.')
                    continue
                case 6:
                    break
        except TypeError:
            print('I\'m sorry, that\'s not a valid choice.')
            continue
    return tileCoords, tiles_dict, choice

def main():
    tileCoords = [0,0]
    currentTile = Tile()
    with open('DefaultTiles.json','r') as file:
        a=file.readlines()
        file.close()
    tiles_dict = json.loads(a[0])
    currentTile.reader(tiles_dict['tile' + str(tileCoords[0]) + str(tileCoords[1])])

    while True:
        combat(currentTile)
        print(f'{currentTile.name}\n{currentTile.description}')        
        tileCoords, tiles_dict, choice = menu(tileCoords, tiles_dict)

        if choice == 6:
            print('Thank you for playing.')
            break
        
        try:
            currentTile.reader(tiles_dict['tile' + str(tileCoords[0]) + str(tileCoords[1])])
        except KeyError:
            print('You can\'t go that way.\n__________________________________________________')
            match choice:
                case 1:
                    tileCoords[1] -= 1
                case 2:
                    tileCoords[0] -= 1
                case 3: 
                    tileCoords[1] += 1
                case 4:
                    tileCoords[0] += 1

def combat(currentTile):
    print(f'Name\t\tHealth\tDamage\t')
    for enemy in currentTile.enemies_dict:
        currentTile.enemies_dict[enemy].print_stats()

main()
