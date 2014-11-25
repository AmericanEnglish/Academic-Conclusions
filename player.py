class Player:
    """Creates the player"""
    def __init__(self, name, stats, coords):
        """(Player, str, list of nums, tuple of nums)"""
        self.name = name.split()
        self.stats = stats
        self.contents = []
        self.pack = Backpack()
        self.hp = hp
        self.pos = coords
        self.map = 0

    def move(motion):
        """(str) -> None

        Moves the player in one direction:
        
        North
        South
        East
        West
        
        All other input is ignored
        """
        directions = {
                    'north': (0,1),
                    'south':(0,-1), 
                    'east':(1, 0), 
                    'west':(-1, 0)
                    }
        if motion.lower() in directions:
            self.pos[0] += directions[motion.lower()][0]
            self.post[1] += directions[motion.lower()][1]


class Backpack:
    """Creates a backpack"""
    def __init__(self):
        self.contents = []

    def pull(thing):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """

        for item in self.contents:
            if thing.lower() == item.name.lower():
                return item
        return None

    def put(thing):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        for item in Player.contents:
            if thing.lower() == item.name.lower():
                self.contents.append(item)
                del Player.contents[item]
                return '{} was put into the pack'.format(thing)
        return None

