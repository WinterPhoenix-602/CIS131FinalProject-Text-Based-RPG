#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Text Based RPG

from PlayerClass import Player
from EnemyClass import Enemy

def main():
    player = Player('Player', 100, 100, 5, 1)
    goblin = Enemy('Goblin', 25, 0, 2, 1)
    player.printStats()
    goblin.printStats()
    player.modifyHealth(goblin.damage)
    player.modifyMagic(-10)
    player.printStats()

main()