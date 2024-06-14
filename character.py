class Character:
    # Setting Attributes
    __name = None
    __character_class = None
    armor = None
    __level = None
    __experience_points = None
    __hit_points = None
    __armor_class = None
    __skills = None
    __inventory = None
    __gold = None
    __attribute_points = None
    hitpoints = None
    
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level

    def __init__(self, name, character_class, armor, damage, hitpoints):
        self.setName(name)  # Character's name
        self.setCharacter_class(character_class)  # Character's class
        self.setArmor(armor)  # Character's armor value
        self.setLevel(1)  # Character's current level
        self.setExperience_points(0)  # Character's current experience points
        self.setHit_points(100)  # Example starting value for character's hit points
        self.setArmor_class(10)  # Example starting value for character's armor class
        self.setSkills({})  # Example empty dictionary for character's skills
        self.setInventory([])  # Example empty list for character's inventory
        self.setGold(0)  # Example starting value for character's gold
        self.setAttribute_points(0)  # Attribute points available to allocate
        self._damage = damage
        self.hitpoints = hitpoints

    
    def getName(self):
        return self.__name
    
    def getCharacter_class(self):
        return self.__character_class
    
    def getArmor(self):
        return self.armor
    
    def getLevel(self):
        return self.__level
    
    def getExperience_points(self):
        return self.__experience_points
    
    def getHit_points(self):
        return self.__hit_points
    
    def getArmor_class(self):
        return self.__armor_class
    
    def getSkills(self):
        return self.__skills
    
    def getInventory(self):
        return self.__inventory
    
    def getGold(self):
        return self.__gold
    
    def getAttribute_points(self):
        return self.__attribute_points

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
    
    def setLevel(self, new_level):
        if 1 <= new_level <= self.MAX_LEVEL:
            self.__level = new_level
        else:
            raise ValueError(f"Level must be between 1 and {self.MAX_LEVEL}")
    
    def setExperience_points(self, new_experience_points):
        if new_experience_points >= 0:
            self.__experience_points = new_experience_points
        else:
            raise ValueError("Experience points cannot be negative")
    
    def setHit_points(self, new_hit_points):
        if new_hit_points >= 0: 
            self.__hit_points = new_hit_points
        else:
            print("You lost!")
            raise ValueError("Hit points cannot be negative")
    
    def setArmor_class(self, new_armor_class):
        if new_armor_class >= 0:
            self.__armor_class = new_armor_class
        else:
            raise ValueError("Armor class cannot be negative")
    
    def setSkills(self, new_skills):
        if isinstance(new_skills, dict):
            self.__skills = new_skills
        else:
            raise ValueError("Skills must be a dictionary")
    
    def setInventory(self, new_inventory):
        if isinstance(new_inventory, list):
            self.__inventory = new_inventory
        else:
            raise ValueError("Inventory must be a list")
    
    def setGold(self, new_gold):
        if new_gold >= 0:
            self.__gold = new_gold
        else:
            raise ValueError("Gold cannot be negative")
    
    def setAttribute_points(self, new_attribute_points):
        if new_attribute_points >= 0:
            self.__attribute_points = new_attribute_points
        else:
            raise ValueError("Attribute points cannot be negative")

        

    def assign_attribute_points(self, attribute, points):
        # Ensure the attribute exists before assigning points
        if attribute in self.__dict__:
            setattr(self, attribute, getattr(self, attribute) + points)  # Add points to the attribute
            self.attribute_points -= points  # Decrease available attribute points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")

    def gain_experience(self, experience):
        self.experience_points += experience  # Increase character's experience points
        # Calculate experience required for next level
        required_experience = self.calculate_required_experience(self.level + 1)
        # Check if character has enough experience to level up and is below the level cap
        while self.experience_points >= required_experience and self.level < self.MAX_LEVEL:
            self.level += 1  # Level up the character
            self.experience_points -= required_experience  # Decrease character's experience points
            self.hit_points += 10  # Example: Increase hit points by 10 each level up
            self.attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.name} is now level {self.level}.")
            # Calculate experience required for next level
            required_experience = self.calculate_required_experience(self.level + 1)

    def calculate_required_experience(self, level):
        # Example exponential scaling: Each level requires 100 more experience points than the previous level
        return int(100 * (1.5 ** (level - 1)))

    def is_alive(self):
        return self.hit_points > 0

    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.getArmor())
        self.setHit_points(self.getHit_points() - actual_damage)
        if self.getHit_points() <= 0:
            print(f"{self.getName()} takes {actual_damage} damage and has been defeated!")
        else:
            #print(f"{self.getName()} takes {actual_damage} damage. Remaining hit points: {self.getHit_points()}")
            return actual_damage

    def health_bar(self):
        print(self.getHit_points(self))