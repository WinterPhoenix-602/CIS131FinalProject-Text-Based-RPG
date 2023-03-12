import time
from tabulate import tabulate

string = tabulate([["Testing\n1\n2"]], tablefmt="fancy_outline")

while True:
    line = ""
    previousChar = ""
    for character in string:
        line += character
        if character == "\n":
            print(line, end="")
            line = ""
            previousChar = ""
            time.sleep(1)
            continue
        previousChar = character
    break
