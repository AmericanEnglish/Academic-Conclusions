class Mapp:
    pass


class Room:
    pass


class Interactable:
    def __init__(self, name, weight, contents, otype):
        self.name = name
        self.weight = weight
        self.contents = contents
        self.type = otype


class Door(Interactable):
    def __init__(self, name, weight, contents, otype, locked):
        super().__init__(name, weight, contents, otype)
        self.locked = locked
    def open():
        pass

    def examine():
        print('Door appears to made of {} and is {}')


class Table(Interactable):
    pass

class Chair(Interactable):
    pass

class NPC(Interactable):
    pass