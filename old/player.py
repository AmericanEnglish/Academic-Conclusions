class Player:
    """Creates the player"""
    def __init__(self, name, coords):
        """(Player, str, list of nums, tuple of nums)"""
        self.name = name
        self.person = []
        self.pack = []
        self.pos = coords
        self.map = None
        self.room = None
        self.score = 0
        self.totalmoves = 0

    def move(self, motion):
        """(str) -> None

        Moves the player in one direction:
        
        North
        South
        East
        West
        
        All other input is ignored
        """
        
        
        self.totalmoves += 1
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
        else:
            print('Not a valid command, type help for help')

    def pull(self, thing):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """

        for item in self.pack:
            if thing.lower() == item.name.lower():
                self.person.append(item)
                self.pack.remove(item)
                print('{} was pulled out of your pack\n'.format(item.name))
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
                print('{} was put into the pack \n'.format(item.name))
                return
        print('You do not posses {} \n'.format(thing))

    def pack_view(self):
        """(Backpack)

        Displays a sort list of backpack contents
        """
        #create sorting algorithim
        if self.pack == []:
            print('>Pack is empty<')
        #self.pack.sort()
        for item in self.pack:
            print('{}'.format(str(item).title()))
        print('')

    def person_view(self):
        #create sorting algoritihim
        if self.person == []:
            print('>You have nothing on you<')
        for item in self.person:
            print('{}'.format(str(item).title()))
        print('')

    def examine(self, thing):
        tracking = 0
        for item in self.person:
            if item.name.lower() == thing:
                item.examine()
            else:
                tracking += 1
        if tracking == len(self.person):
            print('')
