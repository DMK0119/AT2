class Character:
    # Setting Attributes
    __name = None
    __character_class = None
    armor = None
    _hit_points = None  # Changed from '__hit_points'
    __armor_class = None


    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level

    def __init__(self, name, character_class, armor, damage, hitpoints):
        self.setName(name)  # Character's name
        self.setCharacter_class(character_class)  # Character's class
        self.setArmor(armor)  # Character's armor value
        self.setHit_points(hitpoints)  # Example starting value for character's hit points
        self.setArmor_class(10)  # Example starting value for character's armor class
        self._damage = damage

    def getName(self):
        return self.__name

    def getCharacter_class(self):
        return self.__character_class

    def getArmor(self):
        return self.armor

    def getHit_points(self):
        return self._hit_points  # Changed from '__hit_points'

    def getArmor_class(self):
        return self.__armor_class

    def getDamage(self):
        return self._damage

    def setDamage(self, new_damage):
        self.damage = new_damage

    def setName(self, new_name):
        self.__name = new_name

    def setCharacter_class(self, new_character_class):
        self.__character_class = new_character_class

    def setArmor(self, new_armor):
        self.armor = new_armor

    def setHit_points(self, new_hit_points):
        if new_hit_points >= 0:
            self._hit_points = new_hit_points  # Changed from '__hit_points'
        else:
            print("You lost!")
            raise ValueError("Hit points cannot be negative")

    def setArmor_class(self, new_armor_class):
        if new_armor_class >= 0:
            self.__armor_class = new_armor_class
        else:
            raise ValueError("Armor class cannot be negative")
        
    def is_alive(self):
        return self.hit_points > 0

    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.getArmor())
        new_hit_points = self.getHit_points() - actual_damage

        if new_hit_points <= 0:
            new_hit_points = 0  # Ensure hit points don't go negative

        self.setHit_points(new_hit_points)

        if new_hit_points == 0:
            print(f"{self.getName()} has been defeated!")
        else:
            print(f"{self.getName()} takes {actual_damage} damage. Remaining hit points: {new_hit_points}")

        return actual_damage

    def health_bar(self):
        print(self.getHit_points())  # Placeholder for health bar implementation
