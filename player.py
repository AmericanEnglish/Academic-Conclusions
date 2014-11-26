class Player:
    """Creates the player"""
    def __init__(self, name, stats, coords):
        """(Player, str, list of nums, tuple of nums)"""
        self.name = name.split()
        self.stats = stats
        self.person = []
        self.pack = []
        self.hp = 0
        self.pos = coords
        self.map = 0
        self.room = None

    def move(self, motion):
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
        x = self.pos[0]
        y = self.pos[1]
        if motion.lower() in directions:
            x = self.pos[0] + directions[motion.lower()][0]
            y = self.pos[1] + directions[motion.lower()][1]
            self.pos = x, y
            print('You have moved {}\n'.format(motion))

    def pull(self, thing):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """

        for item in self.pack:
            if thing.lower() == item.name.lower():
                self.person.append(item)
                self.pack.remove(item)
                print('{} was pulled out of your pack\n'.format(thing))
                return
        print('You lack {} in your pack\n'.format(thing))

    def put(self, thing):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        for item in self.person:
            if thing.lower() == item.name.lower():
                self.pack.append(item)
                self.person.remove(item)
                print('{} was put into the pack \n'.format(thing))
                return
        print('You do not posses {} \n'.format(thing))

    def pack_view(self):
        """(Backpack)

        Displays a sort list of backpack contents
        """
        if self.pack == []:
            print('>Pack is empty<\n')
        self.pack.sort()
        for item in self.pack:
            print('{}\n'.format(item.name))

    def person_view(self):
        if self.person == []:
            print('>You have nothing on you<\n')
        self.person.sort()
        for item in self.person:
            print('{}\n'.format(item.name))

    def enter(self, roomobj):
        for item in mapp.check():
            if roomobj.name == item.name:
                
