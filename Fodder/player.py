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
            exit()

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
                exit()
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
        thing = thing.lower().title()
        #Checks to make sure item exists and pulls the id
        cur.execute("""SELECT id, name FROM items WHERE name = %s """, [thing])
        items_query = cur.fetchall()
        if items_query == []:
            print("You dont have {} in your pack!\n".format(thing))
        else:
            # Checks the backpack for item
            cur.execute("""SELECT id FROM inventory 
                WHERE name = %s AND backpack = TRUE""", items_query[0])
            inventory_query = cur.fetchall()
            if inventory_query == []:
                print('You dont have {} in your pack!\n'.format(thing))
            else:
                # Moves item to personal inventory
                cur.execute("""UPDATE inventory_query SET backpack = FALSE 
                        WHERE id = %s""", inventory_query[0])
                print('Youve pulled {} from your pack!\n'.format(thing))

    def put(self, thing, cur):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        thing = thing.lower().title()
        #Checks to make sure item exists and pulls the item_id
        cur.execute("""SELECT id FROM items WHERE name = %s""", [thing])
        items_query = cur.fetchall()
        if items_query == []:
            print('You do not possess {}!'.format(thing))
        else:
            # Checks to see if item_id in personal inventory
            cur.execute("""SELECT id FROM inventory
                WHERE id = %s AND name IS NULL AND backpack = FALSE""", items_query[0])
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
        #create sorting algorithim
        cur.execute("""SELECT items.name FROM inventory, items
            WHERE items.id = inventory.id AND backpack = TRUE""")
        backpack = cur.fetchall()
        print('> Your Pack <')
        backpack.sort()
        if backpack == []:
            print('-Empty-')
        else:
            for items in backpack:
                print('-{}'.format(items[0]))
        print()

    def person_view(self, cur):
        cur.execute("""SELECT items.name FROM inventory, items
            WHERE items.id = inventory.id AND inventory.name IS NULL
                AND backpack = FALSE""")
        person = cur.fetchall()
        person.sort()
        print('> You Hold <')
        if person == []:
            print('-Nothing-')
        else:
            for item in person:
                print('-{}'.format(item[0]))
        print()
        
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
