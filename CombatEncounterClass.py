#Caiden Wilson
#3/10/2023
#Final Project: Combat Encounter Class

class CombatEncounter:
    def __init__(self, name = "", description = "", enemies_dict = {}):
        self._name = name
        self._description = description
        self._enemies_dict = enemies_dict

    #getters
    def get_name(self):
        return self._name
    def get_description(self):
        return self._description
    def get_enemies_dict(self):
        return self._enemies_dict
    
    #setters
    def set_name(self):
        self._name
    def set_description(self, description):
        self._description = description
    def set_enemies_dict(self, enemies_dict):
        self._enemies_dict = enemies_dict

    #sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                if key != "quantity":
                    setattr(self, key, input_dict[key])
            except:
                print("No such attribute, please consider adding it in init.")
                continue

    def start_encounter(self):
        print(self.description)
        print("Enemies present: ", end="")
        for enemy in self.enemies:
            print(enemy.name, end=", ")
        print("\nLet the combat begin!\n")
     