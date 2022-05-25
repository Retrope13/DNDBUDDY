class PC:
    def __init__(self, name = "", race="", char_class="", level=1, stats=[], ac=0, inventory=[], gold=0):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.stats = stats
        self.ac = ac
        self.inventory = inventory
        self.gold = gold
    
    def printInv(self):
        print(self.inventory)
    
    def setProp(self, prop, newVal):
        self.prop = newVal