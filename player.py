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
        self.victory = False

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
        # Checks to make sure item exists and pulls the id
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
        # Checks to make sure item exists and pulls the item_id
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
                        print('Invalid: try -examine object-, or type help examine for more.')
                    else:
                        print('*{}\n++{}'.format(thing, portal_query[0][0]))
                else:
                    print('-{}\n++{}'.format(thing, personal_query[0][0]))
            else: 
                #Turns the list of tuples into just a tuple
                container_query = container_query[0]
                # Checks room flag
                room_flag = container_query[3]
                locked =  container_query[2] != None
                if room_flag:
                    print('#{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[1]))
                else:
                    # If not a room, than just a normal container
                    # Checks first to display locked or not
                    if locked:
                        cur.execute("""SELECT * FROM inventory
                            WHERE item_id = %s AND backpack = FALSE AND name IS NULL""",
                            [container_query[2]])
                        unlocking = cur.fetchall()
                        if unlocking == []:
                            print('#{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[1]))
                        else:
                            self.unlock(container_query[0], container_query[2], cur)
                            print('> You Attempt To Unlock The {} <'.format(thing))
                            print('-The Lock And Key Vanish-\n')
                            print('#{}\n-Locked: False\n++{}'.format(thing, container_query[1]))
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
                    # If not locked displays contents of the container
                    else:
                        print('#{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[1]))
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
            print(':{}\n++{}'.format(thing, npc_query[0][0]))
        print()

    def take(self, combo, cur):
        item = combo[0]
        item = item.lower().title()
        container = combo[1]
        container = container.lower().title()
        cur.execute("""SELECT items.id, containers.unlock_item_id FROM containers, items
                    WHERE items.name = %s AND containers.name = %s AND
                    containers.x = %s AND containers.y = %s""",
                    [item, container, self.pos[0], self.pos[1]])
        
        # Isolates the tuple from the list
        item_id = cur.fetchall()
        if len(item_id) == 1 and item_id[0][1] == None:
            cur.execute("""INSERT INTO inventory VALUES (NULL, %s, FALSE)""",
                [item_id[0][0]])
            cur.execute("""UPDATE items 
                SET x = NULL, y = NULL, map_name = NULL, container_id = NULL
                WHERE items.id = %s""", [item_id[0][0]])
            print('> You took {} from {} <'.format(item, container))
        elif item_id[0][1] != None:
            print('-The {} Is Locked, Consider Unlocking-'.format(container))
        else:
            print('Not a valid command, type help for help.')
        print()
    
    def enter(self, room_name, cur):
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
                self.map = map_info[0][0]
                self.pos = map_info[0][1]
                cur.execute("""SELECT description FROM maps
                    WHERE name = %s""", [self.map])
                # Prints the map description
                print('> You Have Entered The {} <'.format(self.map))
                print('++{}'.format(cur.fetchall()[0][0]))
        else:
            room_info = room_ident[0]
            if room_info[2] == None:
                self.room = room_info[0:2]
                print('> You Enter The {} <'.format(self.room[1]))
            else:
                print('> You Attempt To Unlock The Building <')
                cur.execute("""SELECT * FROM inventory
                    WHERE name IS NULL AND item_id = %s""", [room_info[-1]])
                unlock = cur.fetchall()
                if unlock == []:
                    print('- To No Resolve, You Dont Have The Key -')
                else:
                    print('- Success! The Lock & Key Vanish! -')
                    self.unlock(room_info[0], room_info[-1], cur)
                    self.room = room_info[0:2]
                    print('> You Enter The {} <'.format(self.room[1]))
        print()

    def unlock(self, container_id, unlock_item_id, cur):
        cur.execute("""UPDATE containers 
        SET unlock_item_id = NULL
        WHERE id = %s """, [container_id])
        cur.execute("""DELETE FROM inventory 
            WHERE item_id = %s""", [unlock_item_id])

    def room_look(self, cur):
        cur.execute("""SELECT name FROM containers
            WHERE parent_container_id = %s""", [self.room[0]])
        contents = cur.fetchall()

        print('> Around You See <')
            # Check for npcs
        cur.execute("""SELECT name FROM npcs
            WHERE room_id = %s""", [self.room[0]])
        npc_query = cur.fetchall()
        if npc_query == [] and contents == []:
            print('-Nothing-')
        else:
            if npc_query != []:
                npc_query.sort()
                for people in npc_query:
                    print(':{}'.format(people[0]))
            if contents != []:
                contents.sort()
                for items in contents:
                    print('-{}'.format(items[0]))
        print()

    def room_ground(self, cur):
        cur.execute("""SELECT name FROM items 
            WHERE container_id = %s""", [self.room[0]])
        contents = cur.fetchall()

        print('> On The Ground You See <')
        if contents == []:
            print('-Nothing-')
        else:
            for items in contents:
                print('-{}'.format(items[0]))
        print()

    def room_take(self, combo, cur):
        thing = combo[0].lower().title()
        container = combo[1].lower().title()
        cur.execute("""SELECT items.id, containers.unlock_item_id
            FROM items, containers
            WHERE containers.name = %s AND items.name = %s AND
                containers.id = items.container_id AND 
                containers.parent_container_id = %s""", 
                [container, thing, self.room[0]])
        item_id = cur.fetchall()
        if item_id == []:
            print('Not a valid command, type help for help')
        elif len(item_id) == 1 and item_id[0][1] == None:
            cur.execute("""INSERT INTO inventory VALUES (NULL, %s, FALSE)""",
                [item_id[0][0]])
            cur.execute("""UPDATE items 
                SET map_name = NULL, container_id = NULL
                WHERE items.id = %s""", [item_id[0][0]])
            print('> You Took {} From {} <'.format(thing, container))
        elif item_id[0][1] != None:
            print('-The {} Is Locked, Consider Unlocking-'.format(container))
        print()
        
    def room_pickup(self, thing, cur):
        thing = thing.lower().title()
        cur.execute("""SELECT items.id FROM items
            WHERE items.name = %s AND items.container_id = %s""", 
            [thing, self.room[0]])
        items_query = cur.fetchall()

        if items_query == []:
            print('Not a valid command, type help for help.')
        else:
            cur.execute("""INSERT INTO inventory VALUES (NULL, %s, FALSE)""",
                items_query[0])
            cur.execute("""UPDATE items SET container_id = NULL, map_name = NULL 
                WHERE items.id = %s""", items_query[0])
            print('> You Picked Up The {} <'.format(thing))
        print()

    def room_drop(self, thing, cur):
        thing = thing.lower().title()
        cur.execute("""SELECT items.id FROM items, inventory
            WHERE items.id = inventory.item_id AND items.name = %s AND
            inventory.name IS NULL AND backpack = FALSE""", [thing])
        items_query = cur.fetchall()
        if items_query == []:
            print('Not a valid command, type help for help.')
        else:
            cur.execute("""DELETE FROM inventory WHERE item_id = %s""",
                items_query[0])
            cur.execute("""UPDATE items 
                SET container_id = %s, map_name = %s
                WHERE items.id = %s""",
                [self.room[0], self.map, items_query[0][0]])
            print('> You Dropped {} To The Ground! <'.format(thing))
        print()

    def room_examine(self, thing, cur):
        thing = thing.lower().title()
        # First check for NPCs
        cur.execute("""SELECT description FROM npcs
            WHERE room_id = %s AND name = %s""", [self.room[0], thing])
        npc_query = cur.fetchall()
        if npc_query == []:
            # Check those containers
            cur.execute("""SELECT id, description, unlock_item_id FROM containers
                WHERE room_flag = FALSE AND containers.name = %s AND parent_container_id = %s""",
                [thing, self.room[0]])
            container_query = cur.fetchall()
            if container_query == []:
                # Then look at an item on the person
                cur.execute("""SELECT description FROM items, inventory
                    WHERE items.id = inventory.item_id AND backpack = FALSE AND inventory.name IS NULL
                    AND items.name = %s""", [thing])
                personal_query = cur.fetchall()

                if personal_query == []:
                    print('Invalid: try -examine object-, or type help examine for more.')
                else:
                    print('-{}\n++{}'.format(thing, personal_query[0][0]))
            else:
                # Locked checks if item id is present or None
                locked = container_query[0][2] != None
                if locked:
                    # Check inventory for the key
                    cur.execute("""SELECT * FROM inventory
                        WHERE item_id = %s AND backpack = FALSE AND name IS NULL""",
                        [container_query[0][2]])
                    unlocking = cur.fetchall()
                    # Means you can't unlock it
                    if unlocking == []:
                        print('-{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[0][1]))
                    # If the list isn't empty you have the key
                    else:
                        # Calls the unlocking method
                        self.unlock(container_query[0][0], container_query[0][2], cur)
                        print('-{}\n-Locked: False\n++{}'.format(thing, container_query[0][1]))
                        print('> Inside You See <')
                        # Pulls chest contents
                        cur.execute("""SELECT name FROM items
                            WHERE items.container_id = %s""", [container_query[0][0]])
                        contents = cur.fetchall()
                        contents.sort()
                        if contents != []:
                            for items in contents:
                                print('-{}'.format(items[0]))
                        else:
                            print('-Empty-')
                # If not locked displays contents of the container
                else:
                    print('-{}\n-Locked: {}\n++{}'.format(thing, locked, container_query[0][1]))
                    # Pulls contents from items table
                    print('> Inside You See <')
                    cur.execute("""SELECT name FROM items
                        WHERE items.container_id = %s""", [container_query[0][0]])
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

    def talk(self, npc_name, cur):
        npc_name = npc_name.lower().title()
        if self.room == None:
            # Pulls NPCs current talk counter and total dialogue number
            cur.execute("""SELECT npcs.counter_value, COUNT(*) FROM npc_dialogue
                INNER JOIN npcs ON npcs.name = npc_dialogue.npc_name
                WHERE name = %s AND x = %s AND y = %s
                GROUP BY npcs.name""",
                [npc_name, self.pos[0], self.pos[1]])
            counters = cur.fetchall()
            
            # Pull down their conditions
            cur.execute("""SELECT condition, action FROM npc_conditionals, npcs
                WHERE npc_name = %s AND x = %s AND y = %s AND npc_name = name""",
                [npc_name, self.pos[0], self.pos[1]])
            conditionals = cur.fetchall()
            
            # Then their dialogue
            cur.execute("""SELECT counter, dialogue FROM npc_dialogue
                INNER JOIN npcs ON npc_dialogue.npc_name = npcs.name
                WHERE npc_name = %s AND x = %s AND y = %s""",
                [npc_name, self.pos[0], self.pos[1]])
            dialogue = cur.fetchall()
        else:
            # If not outside then they must be in a room
            # Pulls down current talk counter and dialogue total
            cur.execute("""SELECT npcs.counter_value, COUNT(*) FROM npc_dialogue
                INNER JOIN npcs ON npcs.name = npc_dialogue.npc_name
                WHERE npc_name = %s AND room_id = %s
                GROUP BY npcs.name""",
                [npc_name, self.room[0]])
            counters = cur.fetchall()
            # Pulls down NPC's conditionals
            cur.execute("""SELECT condition, action FROM npc_conditionals, npcs
                WHERE npc_name = %s AND room_id = %s AND name = npc_name""",
                [npc_name, self.room[0]])
            conditionals = cur.fetchall()
            # Pulls down NPC counter and dialogue
            cur.execute("""SELECT counter, dialogue FROM npc_dialogue, npcs
                WHERE npc_name = %s AND room_id = %s AND npc_name = name""",
                [npc_name, self.room[0]])
            dialogue = cur.fetchall()
        # This means the target NPC is not at location
        if counters == []:
            print('Not a valid command, type help for help')
            print()
            return 
        # Sets counters to the current counter value
        counters = counters[0]
        # Prevent same dialgue from printing twice
        duplication = False
        # Begins combing through conditionals
        for item_id, condition in conditionals:
            # Conditionals are labeled and split by blank space
            condition = condition.split()
            # Checks that you have the needed item for the conditional
            if self.has(npc_name, item_id, cur):
                duplication = True
                # Stops you from trigger conditionals that are dialogue based
                if counters[0] < counters[1] - len(conditionals):
                    counters = (counters[1] - len(conditionals), counters[1])
                # If conditional is triggered, allows you keep trigger if needed
                elif counters[0] < counters[1] - 1:
                    counters = (counters[0] + 1, counters[1])
                # Updates the current talk counter in the database
                cur.execute("""UPDATE npcs 
                    SET counter_value = %s
                    WHERE name = %s""", [counters[0], npc_name])
                # Prints dialogue you are currently on
                for value, phrase in dialogue:
                    if value == counters[0]:
                        print(phrase)
                # Allows you to win
                if condition[0] == 'score()':
                    self.victory = True
                    self.death = True
                # Gives you items
                elif condition[0] == 'give':
                    self.give(int(condition[1]), cur)
        # Prints the most recent phrase conditional/non-conditional you are on
        for value, phrase in dialogue:
            if value == counters[0] and duplication:
                duplication = False
            elif value == counters[0] and not duplication:
                print(phrase)
        # Allows for an infinite number of conditionals by keeps the counter
        # In line with conditional number while preventing overflow
        if counters[0] < counters[1] - len(conditionals) - 1:
            cur.execute("""UPDATE npcs
                SET counter_value = counter_value + 1
                WHERE name = %s""", [npc_name])
        print()

    def has(self, npc_name, item_id, cur):
        cur.execute("""SELECT * FROM inventory
            WHERE name IS NULL AND item_id = %s""", [item_id])
        filler = cur.fetchall()
        if filler == []:
            return False
        # Removes item from inventory to the npc's inventory
        else:
            cur.execute("""UPDATE inventory 
                SET name = %s
                WHERE item_id = %s""", [npc_name, item_id])
            return True

    def give(self, item_id, cur):
        # Moves item to your inventory
        cur.execute("""UPDATE inventory
            SET name = NULL
            WHERE item_id = %s""", [item_id])
        # Displays the moving of item
        cur.execute("""SELECT name FROM items
            WHERE id = %s""", [item_id])
        thing = cur.fetchall()[0][0]
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
