from character import Character

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, "Rogue", armor=0, hitpoints=100, damage = 50)
        # Additional attributes and methods specific to the Rogue class
    
    def damage(self):
        return self.getDamage()
    
    def getHealth(self):
        return self.__hit_points
    