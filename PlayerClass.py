#Caiden Wilson
#3/2/2023
#CIS131
#Final Project: Player Class

class Player:
    maxHealth = 100
    maxMana = 100

    def __init__(self, name = 'Player', health = 100, mana = 50, baseDamage = 5, baseDefense = 1):
        self.name = name
        self.health = health
        self.mana = mana
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

    def modify_mana(self, change):
        self.mana += change
        if self.mana > self.maxMana:
            self.mana = self.maxMana
    
    def print_stats(self):
        print(f'____________________\n{self.name}\nHealth: {self.health}\nMana: {self.mana}\nDamage: {self.baseDamage}\nDefense: {self.baseDefense}')
