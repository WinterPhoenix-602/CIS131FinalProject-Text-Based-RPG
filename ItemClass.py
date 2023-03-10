#Caiden Wilson
#3/9/2023
#CIS131
#Final Project: Item Class

class Item:
    #initialization method
    def __init__(self, itemType = "", name = "", stats = {}):
        self._itemType = itemType
        self._name = name
        self._stats = stats

    #getters
    def get_itemType(self):
        return self._itemType
    def get_name(self):
        return self._name
    def get_stats(self):
        return self._stats
    
    #setters
    def set_itemType(self, itemType):
        self._itemType = itemType
    def set_name(self, name):
        self._name = name
    def set_stats(self, stats):
        self._stats = stats

    #returns formatted string representation
    def __str__(self):
        itemString = f"{self._name}\t| "
        for count, stat in enumerate(self._stats):
            itemString += f"{list(self._stats.keys())[count]}: {self._stats[stat]}\t| "
        return itemString
