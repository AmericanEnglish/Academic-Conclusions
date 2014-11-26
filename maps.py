class Mapp:
    def __init__(self, contents):
        self.contents = contents
            #contents is a dict of tuple: list objects
            # {(0, 0):[Room, Enemey], (0,1): []} 
    
    def check(self, pos):
        return self.contents[pos]


class Room:
    def __init__(self, name, door, contents, num):
        self.name = name
        self.num = num
        self.contents = contents
        self.door = door


class Interactable:
    def __init__(self, name, weight, composition, num):
        self.name = name
        self.weight = weight
        self.madeof = composition
        self.num = num

class Door(Interactable):
    def __init__(self, name, weight, locked, composition, num):
        super().__init__(name, weight, composition, num)
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

def inroom(protag, curroom):
    pass