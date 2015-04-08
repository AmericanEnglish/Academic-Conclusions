import psycopg2

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
        mapmax = cur.fetchall()[0]
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
                print("-You see the torch flicker and the wind begins to pick up Any further and you might not be going back.\n")

        else:
            print('Not a valid command, type help for help\n')

    def pull(self, thing, cur):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """
        #Query helps keep person inventory beneath 11
        cur.execute("""SELECT * FROM inventory 
            WHERE backpack = FALSE AND name IS NULL""")
        capacity = cur.fetchall()
        if len(capacity) >= 10:
            print('You attempt to use your pack but you fumble your items. \
                You cant carry anymore in your hands, consider putting something \
                away\n')
            return

        thing = thing.lower().title()
        #Checks to make sure item exists and pulls the id
        cur.execute("""SELECT inventory.item_id FROM inventory, items
            WHERE inventory.item_id = items.id AND items.name = %s AND 
                backpack = TRUE""", [thing])
        
        inventory_query = cur.fetchall()
        if inventory_query == []:
            print('You dont have {} in your pack!'.format(thing))
        else:
            # Moves item to personal inventory
            cur.execute("""UPDATE inventory SET backpack = FALSE 
                    WHERE item_id = %s""", inventory_query[0])
            print('Youve pulled {} from your pack!'.format(thing))
        print()

    def put(self, thing, cur):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        thing = thing.lower().title()
        #Checks to make sure item exists and pulls the item_id
        cur.execute("""SELECT inventory.item_id FROM inventory, items
            WHERE inventory.item_id = items.id AND items.name = %s AND 
            inventory.name IS NULL AND backpack = FALSE""", [thing])
        
        inventory_query = cur.fetchall()
        if inventory_query == []:
            print('You do not possess {}!'.format(thing))
        else:
            # Moves item to backpack by changing backpack -> TRUE
            cur.execute("""UPDATE inventory SET backpack = TRUE
                    WHERE item_id = %s""", inventory_query[0])
            print('Youve put {} in your pack!\n'.format(thing))


    def pack_view(self, cur):
        """(Backpack)

        Displays a sort list of backpack contents
        """
        # Selects items that are in pack and them collects their names'
        cur.execute("""SELECT items.name FROM inventory, items
            WHERE items.id = inventory.item_id AND backpack = TRUE""")
        
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
            WHERE items.id = inventory.item_id AND inventory.name IS NULL
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
                WHERE map_name = %s AND x = %s AND y = %s""",
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
        cur.execute("""SELECT id FROM inventory, items
            WHERE items.name = %s AND backpack = FALSE AND
                inventory.name IS NULL""", [thing])
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

    def examine(self, thing, cur):
        # Examine spans items, npcs, and containers
        # Starting with the smaller relation first
        thing = thing.lower().title()
        cur.execute("""SELECT description FROM npcs
            WHERE name = %s AND x = %s AND y = %s""",
            [thing, self.pos[0], self.pos[1]])
        npc_query = cur.fetchall()
        if npc_query == []:
            # Then checks containers in the area
            cur.execute("""SELECT id, description, unlock_item_id, room_flag
                FROM containers
                WHERE name = %s AND x = %s AND y = %s""",
                [thing, self.pos[0], self.pos[1]])
            container_query = cur.fetchall()
            if container_query == []:
                # Time to check personal inventory
                cur.execute("""SELECT description FROM inventory, items
                    WHERE items.id = inventory.item_id AND items.name = %s AND
                        backpack = FALSE AND inventory.name IS NULL""", [thing])
                personal_query = cur.fetchall()
                if personal_query == []:
                    # Maybe its a warp_point?
                    cur.execute("""SELECT description FROM maps, warp_points
                        WHERE maps.name = warp_points.to_map AND to_map = %s
                            AND from_map = %s AND from_point = '{%s, %s}'""",
                            [thing, self.map, self.pos[0], self.pos[1]])
                    portal_query = cur.fetchall()
                    if portal_query == []:
                        print('Not a valid command, type help for help.')
                    else:
                        print('-{}\n++{}'.format(thing, portal_query[0][0]))
                else:
                    print('-{}\n++{}'.format(thing, personal_query[0][0]))
            else: 
                #Turns the list of tuples into just a tuple
                container_query = container_query[0]
                # Checks room flag
                room_flag = container_query[3]
                locked =  container_query[2] != None
                if room_flag:
                    print('-{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[1]))
                else:
                    # If not a room, than just a normal container
                    # Checks first to display locked or not
                    if locked:
                        print('-{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[1]))
                    # If not locked displays contents of the container
                    else:
                        print('-{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[1]))
                        # Pulls contents from items table
                        print('> Inside You See <')
                        cur.execute("""SELECT name FROM items
                            WHERE items.container_id = %s""", [container_query[0]])
                        contents = cur.fetchall()
                        contents.sort()
                        if contents != []:
                            for items in contents:
                                print('-{}'.format(items[0]))
                        else:
                            print('-Empty-')
        else:
            print('-{}\n++{}'.format(thing, npc_query[0][0]))
        print()

    def take(self, combo, cur):
        item = combo[0]
        item = item.lower().title()
        container = combo[1]
        container = container.lower().title()
        cur.execute("""SELECT items.id FROM containers, items
                    WHERE items.name = %s AND containers.name = %s AND
                    containers.x = %s AND containers.y = %s""",
                    [item, container, self.pos[0], self.pos[1]])
        
        # Isolates the tuple from the list
        item_id = cur.fetchall()[0]
        if len(item_id) == 1:
            cur.execute("""INSERT INTO inventory VALUES (NULL, %s, FALSE)""",
                item_id)
            cur.execute("""UPDATE items 
                SET x = NULL, y = NULL, map_name = NULL, container_id = NULL
                WHERE items.id = %s""", item_id)
            print('> You took {} from {} <'.format(item, container))
        else:
            print('Not a valid command, type help for help.')
        print()
    
    def enter(room_name, cur):
        room_name = room_name.lower().title()
        cur.execute("""SELECT id, name, unlock_item_id FROM containers
            WHERE name = %s AND x = %s AND y = %s AND
            room_flag = TRUE AND map_name = %s""",
            [room_name, self.pos[0], self.pos[1], self.map])
        room_ident = cur.fetchall()
        if room_ident == []:
            # If it isn't a room it must be a warp_point
            cur.execute("""SELECT to_map, to_point FROM warp_points
                WHERE from_map = %s AND from_point = ARRAY[%s, %s]""",
                [self.map, self.pos[0], self.pos[1]])
            map_info = cur.fetchall()
            if map_info == []:
                print('Not a valid command, type help for help.')
            else:
                self.map = map_info[0]
                self.pos = map_info[1]
                cur.execute("""SELECT description FROM maps
                    WHERE name = %s""", [self.map])
                # Prints the map description
                print('- You Have Entered The {} -'.format(self.map))
                print('++{}'.format(cur.fetchall()[0]))
        else:
            room_info = cur.fetchall()
            if room_info[2] == None:
                self.room = room_info[0:2]
                print('- Youve Entered The {} -'.format(self.room[1]))
            else:
                print('> You Attempt To Unlock The Building <')
                cur.execute("""SELECT * FROM inventory
                    WHERE name IS NULL AND id = %s""", [room_info[-1]])
                unlock = cur.fetchall()
                if unlock == []:
                    print('- To No Resolve, You Dont Have The Key -')
                else:
                    print('- Success! The Lock & Key Vanish! -')
                    self.unlock(room_info[0], room_info[-1], cur)
                    self.room = room_info[0:2]
                    print('- Youve Entered The {} -'.format(self.room[1]))
        print()

    def unlock(container_id, unlock_item_id, cur):
        cur.execute("""UPDATE containers 
        SET unlock_item_id = NULL
        WHERE id = %s """, [container_id])
        cur.execute("""DELETE FROM inventory 
            WHERE item_id = %s""", [unlock_item_id])

    def room_look(self, cur):
        pass

    def room_ground(self, cur):
        pass

    def room_take(self, thing, cur):
        pass

    def room_examine(self, thing, cur):
        pass

    def talk(self, npc_name, cur):
        pass
    # def has(id) <- Checks NPC conditionals return Bool
def help(command, cur):
    cur.execute("""SELECT name, syntax, description FROM help
                                WHERE name = %s""", [command])
    info = cur.fetchall()[0]
    print('{} -> {} \n++{}\n'.format(info[0], info[1], info[2]))
