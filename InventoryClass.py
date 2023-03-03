#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Inventory Class

class Inventory:

    def __init__(self, items):
        self.items = items

    def listItems(self):
        for item in self.items:
            if self.items[item > 0]:
                print(f'Name: {item} Quantity: {self.items[item]}')