class Weapon:
    """Generates a weapon object"""
    def __init__(self, name, dmg, mod, durability):
        """(Weapon, str, num, num, tuple) -> None
        """
        self.name = name
        self.dmg = dmg
        self.mod = mod
        self.status = durability[0]
        self.max = durability[1]

class Sword(Weapon):
    def __init__(self, name, dmg, mod, durability):
        super().__init__(name, dmg, mod, durability)
        self.wtype = 'Sword'

    def pry(objstr):
        #roll to force open here
        pass