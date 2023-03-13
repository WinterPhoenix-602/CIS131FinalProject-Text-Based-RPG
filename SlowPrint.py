import time
import termcolor
from termcolor import colored
from tabulate import tabulate

def slowLinePrint(string="Testing, 1, 2.", delay = 0.05, color="white"):
    for character in string:
        print(colored(character, color), end="")
        time.sleep(delay)
    print("")

def slowTablePrint(string=tabulate([["Testing"], [1], [2]], tablefmt="fancy_outline"), delay = 0.05, color="white"):
    for line in string.splitlines():
        print(colored(line, color))
        time.sleep(delay)

# Testing
"""for color in termcolor.COLORS:
    slowLinePrint(color, color=color)
    slowTablePrint(color, color=color)"""
