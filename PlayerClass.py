#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Player Class

class Player:
    maxHealth = 100
    maxMagic = 100

    def __init__(self, name = '', health = 0, magic = 0, baseDamage = 0, baseDefense = 0):
        self.name = name
        self.health = health
        self.magic = magic
        self.baseDamage = baseDamage
        self.baseDefense = baseDefense

    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except:
                print('No such attribute, please consider adding it in init.')
                continue
    
    def modify_health(self, change):
        self.health += change
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def modify_magic(self, change):
        self.magic += change
        if self.magic > self.maxMagic:
            self.magic = self.maxMagic
    
    def print_stats(self):
        print(f'____________________\n{self.name}\nHealth: {self.health}\nMagic: {self.magic}\nDamage: {self.baseDamage}\nDefense: {self.baseDefense}')
