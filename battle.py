class Weapon:
    """Generates a weapon object"""
    def __init__(self, name, dmg, mod, durability):
        """(Weapon, str, num, num, list) -> None
        """
        self.name = name
        self.dmg = dmg
        self.mod = mod
        self.status = durability[0]
        self.max = durability[1]

class Sword(Weapon):
    def __init__(self, title, dmg, mod, durability):
        super().__init__(title, dmg, mod, durability)
        self.wtype = 'Sword'

