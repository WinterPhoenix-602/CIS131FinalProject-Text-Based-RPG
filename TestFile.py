#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import json
from PlayerClass import Player
from EnemyClass import Enemy
from LocationTileClass import Tile

def menu(tile, dict_0):
    while True:
        try:
            choice = int(input('What would you like to do?\n1: Go North\n2: Go East\n3: Go South\n4: Go West\n5: Open Inventory\n6: Exit Game '))
            match choice:
                case 1:
                    tile[1] += 1
                    with open('Tile' + str(tile[0]) + str(tile[1]) + '.json','r') as file:
                        a=file.readlines()
                        file.close()
                    dict_0=json.loads(a[0])
                    break
                case 2:
                    tile[0] += 1
                    with open('Tile' + str(tile[0]) + str(tile[1]) + '.json','r') as file:
                        a=file.readlines()
                        file.close()
                    dict_0=json.loads(a[0])
                    break
                case 3: 
                    tile[1] -= 1
                    with open('Tile' + str(tile[0]) + str(tile[1]) + '.json','r') as file:
                        a=file.readlines()
                        file.close()
                    dict_0=json.loads(a[0])
                    break
                case 4:
                    tile[0] -= 1
                    with open('Tile' + str(tile[0]) + str(tile[1]) + '.json','r') as file:
                        a=file.readlines()
                        file.close()
                    dict_0=json.loads(a[0])
                    break
                case 5:
                    continue
                case 6:
                    break
        except TypeError:
            print('I\'m sorry, that\'s not a valid choice.')
            continue
        except FileNotFoundError:
            print('You can\'t go that way.')
    return tile, dict_0, choice

def main():
    tile = [0,0]
    with open('Tile' + str(tile[0]) + str(tile[1]) + '.json','r') as file:
        a=file.readlines()
        file.close()
    dict_0=json.loads(a[0])
    while True:
        tile_instance = Tile()
        tile_instance.reader(dict_0)

        print(f'{tile_instance.name}\n{tile_instance.description}')
        tile, dict_0, choice = menu(tile, dict_0)

        if choice == 6:
            break

main()