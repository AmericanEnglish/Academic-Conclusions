import psycopg2

class Player:
    """Creates the player"""
    def __init__(self, name):
        """(Player, str, list of nums, tuple of nums)"""
        self.name = name
        self.pos = (0, 1)
        self.map = 'Small Town'
        self.room = None
        self.totalmoves = 0
        self.death = False

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
                    'north': (0,1),
                    'south':(0,-1), 
                    'east':(1, 0), 
                    'west':(-1, 0)
                    }
        x = self.pos[0]
        y = self.pos[1]
        
        # Pulls down the max x,y for the current map
        cur.execute("""SELECT max_x, max_y FROM maps
                    WHERE name = %s""", [self.map])
        mapmax = cur.fetch()[0]
        if motion.lower() in directions:
            x = self.pos[0] + directions[motion.lower()][0]
            y = self.pos[1] + directions[motion.lower()][1]
            # Checks if player ignore the turn back warning
            if x < -1 or x > mapmax[0] + 1 or y < -1 or y > mapmax[1] + 1:
                print('>Dead<\n')
                self.death = True
            self.pos = x, y
            print('You have moved {}\n'.format(motion))
        
        # Sends a turn back warning if player leaves the map boundaries
        if not (0 <= self.pos[0] <= mapmax[0]) or not (0 <= self.pos[1] <= mapmax[1]):
            print("""You see the torch flicker and the wind begins to pick up\n
                    Any further and you might not be going back.""")

        else:
            print('Not a valid command, type help for help\n')

    def pull(self, thing, cur):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """
        #Query helps keep person inventory beneath 11
        cur.execute("""SELECT COUNT(*) FROM inventory 
            WHERE backpack = FALSE AND name IS NULL
            GROUP BY name""")
        capacity = cur.fetchall()[0][0]
        if capacity >= 10:
            print('You attempt to use your pack but you fumble your items. \
                You cant carry anymore in your hands, consider putting something \
                away')
            return
        thing = thing.lower().title()
        #Checks to make sure item exists and pulls the id
        cur.execute("""SELECT inventory.id FROM inventory, items
            WHERE inventory.id = items.id AND items.name = %s AND 
                backpack = TRUE""", [thing])
        
        inventory_query = cur.fetchall()
        if inventory_query == []:
            print('You dont have {} in your pack!\n'.format(thing))
        else:
            # Moves item to personal inventory
        cur.execute("""UPDATE inventory SET backpack = FALSE 
                    WHERE id = %s""", inventory_query[0])
            print('Youve pulled {} from your pack!\n'.format(thing))

    def put(self, thing, cur):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        thing = thing.lower().title()
        #Checks to make sure item exists and pulls the item_id
        cur.execute("""SELECT inventory.id FROM inventory, items
            WHERE inventory.id = items.id AND items.name = %s AND 
            inventory.name IS NULL AND backpack = FALSE""", [thing])
        
        inventory_query = cur.fetchall()
        if inventory_query == []:
            print('You do not possess {}!'.format(thing))
        else:
            # Moves item to backpack by changing backpack -> TRUE
            cur.execute("""UPDATE inventory SET backpack = TRUE
                    WHERE id = %s""", inventory_query[0])
            print('Youve put {} in your pack!\n'.format(thing))


    def pack_view(self, cur):
        """(Backpack)

        Displays a sort list of backpack contents
        """
        # Selects items that are in pack and them collects their names'
        cur.execute("""SELECT items.name FROM inventory, items
            WHERE items.id = inventory.id AND backpack = TRUE""")
        
        backpack = cur.fetchall()
        backpack.sort()

        # Displays information in uniform fashion
        print('> Your Pack <')
        if backpack == []:
            print('-Empty-')
        else:
            for items in backpack:
                print('-{}'.format(items[0]))
        print()

    def person_view(self, cur):
        # Selects items that are on person and collects their names'
        cur.execute("""SELECT items.name FROM inventory, items
            WHERE items.id = inventory.id AND inventory.name IS NULL
                AND backpack = FALSE""")
        person = cur.fetchall()
        person.sort()

        # Displays information in uniform fashion
        print('> You Hold <')
        if person == []:
            print('-Nothing-')
        else:
            for item in person:
                print('-{}'.format(item[0]))
        print()

    def look(self, cur):
        
        # Gathers the names of surrounding containers
        cur.execute("""SELECT name FROM containers
                WHERE containers.map_name = %s AND
                    containers.x = %s AND containers.y = %s""",
                    [self.map, self.pos[0], self.pos[1]])
        surroundings = cur.fetchall()
        surroundings.sort()

        #Display information in uniform fashion
        print('> Around You See <')
        if surroundings == []:
            print('-Nothing-')
        else:
            for items in surroundings:
                print('-{}'.format(items[0]))
        print()

    def ground(self, cur):
        # Gathers the names of ground items
        cur.execute("""SELECT name FROM items
            WHERE item.map_name = %s AND
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
            print('Not a valid command, type help for help.\n')
        else:
            # Puts item into personal inventory
            cur.execute("""INSERT INTO inventory VALUES (NULL, %s, FALSE)""",
                items_query[0])
            # 'Removes' item from map
            cur.execute("""UPDATE items 
                SET x = NULL, y = NULL, map_name = NULL
                WHERE id = %s""", items_query[0])
            print('> You Picked Up <\n{}\n'.format(thing))

    def examine(self, thing):
        tracking = 0
        for item in self.person:
            if item.name.lower() == thing:
                item.examine()
            else:
                tracking += 1
        if tracking == len(self.person):
            print('')

    # def has(id) <- Checks NPC conditionals return Bool
def help(command, cur):
    cur.execute("""SELECT name, syntax, description FROM help
                                WHERE name = %s""", [action[1]])
                info = cur.fetchall()
                print('{} -> {} \n++{}\n'.format(info[0], info[1], info[2]))
