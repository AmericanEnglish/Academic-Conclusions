class Weapon:
    """Generates a weapon object"""
    def __init__(self, name):
        """(Weapon, str, num, num, tuple) -> None
        """
        #self, name, dmg, mod, durability
        self.name = name
        #self.dmg = dmg
        #self.mod = mod
        #self.status = durability[0]
        #self.max = durability[1]

class Sword(Weapon):
    def __init__(self, name):
        super().__init__(name)

    def pry(objstr):
        #roll to force open here
        pass

    def examine(self):
        print('YOU EXAMINED {}'.format(self.name))
