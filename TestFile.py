#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Testing

import json
from PlayerClass import Player
from EnemyClass import Enemy
from LocationTileClass import Tile

with open("Tiles.json",'r') as file:
  a=file.readlines()
dict_0=json.loads(a[0])

tile_instance = Tile()
tile_instance.reader(dict_0)

print(f'{tile_instance.name}\n{tile_instance.description}')
tile_instance.offerDirections()

def main():
    player = Player('Player', 100, 100, 5, 1)
    goblin = Enemy('Goblin', 25, 0, 2, 1)
    player.printStats()
    goblin.printStats()
    player.modifyHealth(goblin.damage)
    player.modifyMagic(-10)
    player.printStats()

# main()