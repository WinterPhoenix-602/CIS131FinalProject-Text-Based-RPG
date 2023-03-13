# Caiden Wilson
# 3/9/2023
# CIS131
# Final Project: Item Class

from tabulate import tabulate


class Item:
    # initialization method
    def __init__(self, itemType="", name="", stats={}, quantity=0):
        self._itemType = itemType
        self._name = name
        self._stats = stats
        self._quantity = quantity

    # getters
    @property
    def itemType(self):
        return self._itemType

    @property
    def name(self):
        return self._name

    @property
    def stats(self):
        return self._stats

    @property
    def quantity(self):
        return self._quantity

    # setters
    @itemType.setter
    def itemType(self, itemType):
        self._itemType = itemType

    @name.setter
    def name(self, name):
        self._name = name

    @stats.setter
    def stats(self, stats):
        self._stats = stats

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity

    # returns formatted string representation
    def __str__(self):
        itemTable = [self._name]
        statString = ""
        if len(self._stats) > 1:
            for stat in self._stats:
                statString += f"{stat}: {self._stats[stat]} "
        else:
            for stat in self._stats:
                statString = f"{stat}: {self._stats[stat]}"
        itemTable.append(statString)
        itemTable.append(self._quantity)
        return tabulate([itemTable], tablefmt="fancy_outline")


'''# Testing
a = Item("Bob", "Feesh", {"Gubible":100})
slowLinePrint(a.__str__())'''
