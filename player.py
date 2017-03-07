import sqlite3


class Player:
    """Creates the player"""
    def __init__(self, name):
        """(Player, str, list of nums, tuple of nums)"""
        self.name = name
        self.pos = {'x': 0, 'y': 1}
        self.map = None
        self.room = None
        self.totalmoves = 0
        self.death = False
        self.victory = False
        self.backpack = []
        self.onhands = []
        self.capacity = {"backpack": 25, "hands": 10}

    def exit(self):
        if self.room is None:
            print("> You cannot exit {} like that! <".format(self.map))
        else:
            print("> You exit {} <".format(self.room))
            self.room = None

    def kill(self):
        self.death = True

    def OffGrid(self):
        """Checks play position and determines if they've left the map"""
        if self.pos['x'] == -1 or self.pos['x'] == self.map.x + 1:
            return 0
        elif self.pos['y'] == -1 or self.pos['y'] == self.map.y + 1:
            return 0
        elif self.pos['y'] < -1 or self.pos['x'] < -1:
            return 1
        elif self.pos['y'] > self.map.y + 1 or self.pos['x'] > self.map.x + 1:
            return 1
        else:
            return -1

    def move(self, cmd, motion):
        """(str) -> None

        Moves the player in one direction:

        North
        South
        East
        West

        All other input is ignored
        """
        if self.room is None:
            self.totalmoves += 1
            # if self.totalmoves == 300:
            #     print('>Dead<\n')
            #     self.death = True
            #     return
            # Changes coordinates
            self.pos['x'] += motion['x']
            self.pos['y'] += motion['y']
                # Checks if player ignore the turn back warning
                # Checks your pos compared to map boundaries
            if self.OffGrid() == 0:
                print("Consider moving back the way you came!")
            elif self.OffGrid() == 1:
                self.death = True
                print('> Dead <')
                return
            else:
                print('You have moved {}!'.format(cmd.lower()))
                self.look()

            # print("-You see the torch flicker and the wind begins to pick up any further and you might not be going back.\n")
        else:
            print('> You are aleady in a room! Try "exit"! <')

    def pull(self, thing):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """
        # Find item in backpack first, user should use the index
        if not thing.isnumeric():
            print("> Refer to items by their number! <")
        else:
            thing = int(thing)
            if len(self.backpack) - 1 < thing:
                print("> No such item exists! <")
            else:
                thing = self.backpack.pop(thing)
                # Attempt to pull from pack
                if len(self.onhands) >= self.capacity["hands"]:
                    print('> You attempt to use your pack but you fumble your \
                        items. You cant carry anymore in your hands, consider \
                        putting something away... <')
                    # Drop it to the ground!
                    if self.room is None:
                        self.map.give(thing)
                    else:
                        self.room.give(thing)
                    print("> You dropped {} to the floor! <".format(thing))
                else:
                    print('Youve pulled {} from your pack!'.format(thing))
                    self.onhands.append(thing)

    def put(self, thing):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        if not thing.isnumeric():
            print("> Refer to items by number! <")
        else:
            thing = int(thing)
            if len(self.onhands) - 1 < thing:
                print("> No such item exists! <")
            else:
                thing = self.onhands.pop(thing)
                if len(self.backpack) >= self.capcity["backpack"]:
                    print("> You fumble around with the items in your \
                            pack. It appears to be full! <")
                    if self.room is None:
                        self.map.give(thing)
                    else:
                        self.room.give(thing)
                    print("> You drop {} to the ground! <".format(thing))
                else:
                    print("> You put {} into your backpack! <".format(thing))
                    self.backpack.append(thing)

    def pack_view(self):
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
            # Just index the items!
            for index, item in self.backpack:
                print("-{}-| {}".format(index + 1, item))

    def onhand(self):
        # Selects items that are on person and collects their names'
        # Displays information in uniform fashion
        print('> You Hold <')
        if self.hands == []:
            print('-Nothing-')
        else:
            for index, item in self.hands:
                print("-{}-| {}".format(index + 1, item))

    def look(self):
        # Gathers the names of surrounding containers
        # Display information in uniform fashion
        print('> Around You See <')
        if self.room is not None:
            self.map.reveal()
        else:
            self.room.reveal()

    def pickup(self, thing, cur):
        thing = thing.lower().title()
        # Selecting item from items
        # 'Removes' item from map
        pass

    def drop(self, thing, cur):
        pass

    def examine(self, action):
        # Examine spans items, npcs, and containers
        # Starting with the smaller relation first
        if len(action) == 1:
            if self.room is None:
                self.look()
            else:
                self.room.examine_inside()
        else:
            if action[1][0] not in symbols.values():
                print("> Use the Symbol and Number for examine! <")
                print("> +0 -0 $0 #0 <")
            elif not action[1][1:].isnumeric():
                print("> Use the Symbol and Number for examine! <")
                print("> +0 -0 $0 #0 <")
            else:
                tocheck = action[1][0]
                checknum = action[1][1:]
                # Cannot examine "Items" not in your hands
                # Maybe fix by saying onhands checks omit the "-"
                if tocheck[0] == "-":
                    # Check hands
                    if len(self.onhands) - 1 < checknum:
                        print("> You are not holding such an item! <")
                    else:
                        self.onhands[checknum].examine()
                else:
                    for cat in symbols.keys():
                        if cat == tocheck:
                            if self.room is None:
                                self.map.examine(checknum, cat)
                            else:
                                self.room.examine(checknum, cat)

    def take(self, combo, cur):
        item = combo[0]
        item = item.lower().title()
        container = combo[1]
        container = container.lower().title()
        # Isolates the tuple from the list
        print('> You took {} from {} <'.format(item, container))
        print('-The {} Is Locked, Consider Unlocking-'.format(container))
        print('Not a valid command, type help for help.')

    def enter(self, room_name):
        # Only works for Rooms. Must be updated to work for Mapp's
        if self.room is not None:
            print("> You are already in a room! <")
        else:
            if not room_name.isnumeric():
                print("> Refer to rooms by their number! <")
            else:
                room_name = int(room_name)
                if len(self.map.contents["Rooms"]) - 1 < room_name:
                    print("> No such room exists! <")
                else:
                    entering = self.map.contents["Rooms"][room_name]
                    if entering.islocked:
                        success = self.unlock(entering)
                        if success:
                            self.room = entering
                            print("> You enter {}! <".format(entering))
                        else:
                            print("> {} is locked! Find a key? <\
                                    ".format(entering))
                    else:
                        self.room = entering
                        print("> You enter {}! <".format(entering))

    def unlock(self, container_id, unlock_item_id, cur):
        pass

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
