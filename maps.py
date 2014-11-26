class Mapp:
    pass


class Room:
    def __init__(self, door, contents, num, name):
        self.name = name
        self.num = num
        self.contents = contents
        self.door

        
class Interactable:
    def __init__(self, name, weight, contents, otype, composition, num):
        self.name = name
        self.weight = weight
        self.contents = contents
        self.type = otype
        self.madeof = composition
        self.num = num

class Door(Interactable):
    def __init__(self, name, weight, contents, otype, locked, composition, num):
        super().__init__(name, weight, contents, otype)
        self.locked = locked
        if locked:
            self.lcked = 'locked'
        else:
            self.lcked = 'unlocked'
    
    def open(self, thing, toon):
        thingobj = None
        for item in toon:
            if item.name == thing:
                thingobj = item
        if thingobj == None:
            return False
        
        if self.locked:
            print('You try to open the door with the {}'.format(thingobj.name))
            if isinstance(thingobj, Key):
                if thingobj.unlock == self.num:
                    return True
                return False
            elif isinstance(thingobj, Sword):
                return thingobj.pry(self.madeof)
            return False
        return True


    def examine(self):
        print('Door appears to made of {} and is {}'.format(self.madeof, self.lcked))


class Table(Interactable):
    pass

class Chair(Interactable):
    pass

class NPC(Interactable):
    pass