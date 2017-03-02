import sqlite3


class Player:
    """Creates the player"""
    def __init__(self, name):
        """(Player, str, list of nums, tuple of nums)"""
        self.name = name
        self.pos = [0, 1]
        self.map = 'Small Town'
        self.room = None
        self.totalmoves = 0
        self.death = False
        self.victory = False
        self.backpack = []
        self.onhands = []

    def move(self, motion, cur):
        """(str) -> None

        Moves the player in one direction:

        North
        South
        East
        West

        All other input is ignored
        """

        self.totalmoves += 1
        if self.totalmoves == 300:
            print('>Dead<\n')
            self.death = True
            return

        directions = {
                    'north': (0, 1),
                    'south': (0, -1),
                    'east': (1, 0),
                    'west': (-1, 0)
                    }
        x = self.pos[0]
        y = self.pos[1]

        # Pulls down the max x,y for the current map
        cur.execute("""SELECT max_x, max_y FROM maps
                    WHERE name = %s""", [self.map])
        mapmax = cur.fetchall()[0]
        # Changes coordinates
        if motion.lower() in directions:
            x = self.pos[0] + directions[motion.lower()][0]
            y = self.pos[1] + directions[motion.lower()][1]
            # Checks if player ignore the turn back warning
            # Checks your pos compared to map boundaries
            if x < -1 or x > mapmax[0] + 1 or y < -1 or y > mapmax[1] + 1:
                print('>Dead<\n')
                self.death = True
                return
            self.pos = x, y
            print('You have moved {}\n'.format(motion))

        # Sends a turn back warning if player leaves the map boundaries
            if not (0 <= self.pos[0] <= mapmax[0]) or not (0 <= self.pos[1] <= mapmax[1]):
                print("-You see the torch flicker and the wind begins to pick up any further and you might not be going back.\n")

        else:
            print('Not a valid command, type help for help\n')

    def pull(self, thing, cur):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """
        if len(capacity) >= 10:
            print('You attempt to use your pack but you fumble your items. \
                You cant carry anymore in your hands, consider putting \
                something away')
            return
        print('Youve pulled {} from your pack!'.format(thing))
        print()

    def put(self, thing, cur):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        thing = thing.lower().title()
        # Checks to make sure item exists and pulls the item_id

        # Item not in inventory
        # else put it in pack
        # print('Youve put {} in your pack!\n'.format(thing))


    def pack_view(self, cur):
        """(Backpack)

        Displays a sort list of backpack contents
        """
        # Selects items that are in pack and them collects their names'
        # Displays information in uniform fashion
        print('> Your Pack <')
        # Display if empty

        if self.backpack == []:
            print('-Empty-')
        else:
            for items in self.backpack:
                print('-{}'.format(items[0]))
        print()

    def onhand(self, cur):
        # Selects items that are on person and collects their names'
        
        # Displays information in uniform fashion
        print('> You Hold <')
        if self.hands == []:
            print('-Nothing-')
        else:
            for item in self.hands:
                print('-{}'.format(item[0]))
        print()

    def look(self, cur):
        
        # Gathers the names of surrounding containers
        cur.execute("""SELECT name FROM containers
                WHERE map_name = %s AND x = %s AND y = %s""",
                [self.map, self.pos[0], self.pos[1]])
        containers = cur.fetchall()
        containers.sort()

        cur.execute("""SELECT name FROM npcs
            WHERE map_name = %s AND x = %s AND y = %s""",
            [self.map, self.pos[0], self.pos[1]])
        npcs_query = cur.fetchall()

        cur.execute("""SELECT to_map FROM warp_points
            WHERE from_map = %s AND from_point = '{%s, %s}'""",
            [self.map, self.pos[0], self.pos[1]])
        warp_points = cur.fetchall()
        #Display information in uniform fashion
        print('> Around You See <')
        if containers == [] and npcs_query == [] and warp_points == []:
            print('-Nothing-')
        else:
            if warp_points != []:
                for points in warp_points:
                    print('*{}'.format(points[0]))
            if npcs_query != []:
                for people in npcs_query:
                    print(':{}'.format(people[0]))
            if containers != []:
                for items in containers:
                    print('#{}'.format(items[0]))
        print()

    def ground(self, cur):
        # Gathers the names of ground items
        cur.execute("""SELECT name FROM items
            WHERE items.map_name = %s AND
                items.x = %s AND items.y = %s""",
                [self.map, self.pos[0], self.pos[1]])
        ground = cur.fetchall()
        ground.sort()

        # Displays information in uniform fashion
        print('> On Ground You See <')
        if ground == []:
            print('-Nothing-')
        else:
            for items in ground:
                print('-{}'.format(items[0]))
        print()

    def pickup(self, thing, cur):
        thing = thing.lower().title()
        # Selecting item from items
        cur.execute("""SELECT id FROM items
            WHERE items.map_name = %s AND
                items.name = %s AND
                items.x = %s AND items.y =%s""",
                [self.map, thing, self.pos[0], self.pos[1]])
        items_query = cur.fetchall()
        if items_query == []:
            print('Not a valid command, type help for help.')
        else:
            # Puts item into personal inventory
            cur.execute("""INSERT INTO inventory VALUES (NULL, %s, FALSE)""",
                items_query[0])
            # 'Removes' item from map
            cur.execute("""UPDATE items 
                SET x = NULL, y = NULL, map_name = NULL
                WHERE id = %s""", items_query[0])
            print('> You Picked Up <\n{}'.format(thing))
        print()

    def drop(self, thing, cur):
        thing = thing.lower().title()
        cur.execute("""SELECT items.id FROM inventory, items
            WHERE items.name = %s AND items.id = inventory.item_id AND 
            backpack = FALSE AND inventory.name IS NULL""", [thing])
        dropped = cur.fetchall()
        if dropped == []:
            print('Not a valid command, type help for help')
        else:
            cur.execute("""DELETE FROM inventory WHERE item_id = %s""", dropped[0])
            cur.execute("""UPDATE items 
                        SET x = %s, y = %s, map_name = %s
                        WHERE id = %s""", 
                        [self.pos[0], self.pos[1], self.map, dropped[0][0]])
            print('Youve dropped {} to the ground'.format(thing))
        print()

    def examine(self, thing, location=None):
        # Examine spans items, npcs, and containers
        # Starting with the smaller relation first
        thing = thing.lower().title()

        # Check for npcs
        # Check for containers
        # Check onhands
        # Check backpack

    def take(self, combo, cur):
        item = combo[0]
        item = item.lower().title()
        container = combo[1]
        container = container.lower().title()
        # Isolates the tuple from the list
        print('> You took {} from {} <'.format(item, container))
        print('-The {} Is Locked, Consider Unlocking-'.format(container))
        print('Not a valid command, type help for help.')
    
    def enter(self, room_name, cur):
        room_name = room_name.lower().title()
        # If it isn't a room it must be a warp_point
        # Prints the map description
        print('> You Have Entered The {} <'.format(self.map))
        print('++{}'.format(cur.fetchall()[0][0]))
        print('> You Attempt To Unlock The Building <')
        print('- To No Resolve, You Dont Have The Key -')
        print('- Success! The Lock & Key Vanish! -')
        print('> You Enter The {} <'.format(self.room[1]))

    def unlock(self, container_id, unlock_item_id, cur):
        pass

    def room_look(self, cur):
        print('> Around You See <')
        print('-Nothing-')

    def room_ground(self, cur):
        print('> On The Ground You See <')
        print('-Nothing-')

    def room_take(self, combo, cur):
        print('Not a valid command, type help for help')
        print('> You Took {} From {} <'.format(thing, container))
        print('-The {} Is Locked, Consider Unlocking-'.format(container))
        
    def room_pickup(self, thing, cur):
        thing = thing.lower().title()
        print('Not a valid command, type help for help.')
        print('> You Picked Up The {} <'.format(thing))

    def room_drop(self, thing, cur):
        print('Not a valid command, type help for help.')
        print('> You Dropped {} To The Ground! <'.format(thing))

    def room_examine(self, thing, cur):
        thing = thing.lower().title()
        # First check for NPCs
        # Check those containers
        # Then look at an item on the person
        print('Invalid: try -examine object-, or type help examine for more.')
        print('-{}\n++{}'.format(thing, personal_query[0][0]))
        # Means you can't unlock it
        print('-{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[0][1]))
        # Calls the unlocking method
        print('-{}\n-Locked: False\n++{}'.format(thing, container_query[0][1]))
        print('> Inside You See <')
        # Pulls chest contents
        print('-{}'.format(items[0]))
        print('-Empty-')
        print('-{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[0][1]))
        # Pulls contents from items table
        print('> Inside You See <')
        print('-{}'.format(items[0]))
        print('-Empty-')
        print('-{}\n++{}'.format(thing, npc_query[0][0]))

    def talk(self, npc_name, cur):
        pass 
        
    def give(self, item_id, cur):
        # Moves item to your inventory
        # Displays the moving of item
        print('> You Were Given {} <'.format(thing))

    # def has(id) <- Checks NPC conditionals return Bool
def help(command, cur):
    cur.execute("""SELECT name, syntax, description FROM help
                                WHERE name = %s""", [command])
    info = cur.fetchall()
    if info == []:
        if command =='all':
            cur.execute("""SELECT name FROM help""")
            info = cur.fetchall()
            for item in info:
                print('-{}'.format(item[0]))
            return
        print('Not a valid command, type help for help.')
        print()
        return
    info = info[0]
    print('{} -> {} \n++{}\n'.format(info[0], info[1], info[2]))
