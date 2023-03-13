import time
from tabulate import tabulate

def slowLinePrint(string="Testing, 1, 2.", delay = 0.05):
    for character in string:
        print(character, end="")
        time.sleep(delay)

def slowTablePrint(string=tabulate([["Testing"], [1], [2]], tablefmt="fancy_outline"), delay = 0.05):
    for line in string.splitlines():
        print(line)
        time.sleep(delay)

