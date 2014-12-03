class Mapp:
    def __init__(self, filename):
            #contents is a dict of tuple: list objects
            # {(0, 0):[[Room, Enemey][Ground Things, Here]], (0,1): [[],[]]} 
        running = {}
        with open(filename, 'r') as somefile:
            self.name = somefile.readline().strip().split(',')[1].strip()
            
            nextline = somefile.readline().strip().split(',')
            dimensionx = (int(nextline[1].strip()), int((nextline[2].strip())))
            self.x = dimensionx[1]

            nextline = somefile.readline().strip().split(',')
            dimensiony = (int(nextline[1].strip()), int(nextline[2].strip()))
            self.y = dimensiony[1]

            nextline = somefile.readline().strip().split(',')
            self.start = (int(nextline[1].strip()), int(nextline[2].strip()))
            #generates empty map contents and all the coordinates
            for x in range(dimensionx[1] + 1):
                for y in range(dimensiony[1] + 1):
                    running[(x , y)] = [[],[]]

            for aline in somefile:
                aline = aline.strip().split(',')
                line = []
                for item in aline:
                    line.append(item.strip())

                if line[0] == 'ROOM':
                    # ROOM X Y NAME DOORNAME LOCKED? COMP DOORKEY
                    #  0   1 2  3      4        5     6      7
                    if len(line) == 8:
                        doorkey = line[7]
                    else:
                        doorkey = None
                    x, y = int(line[1]), int(line[2])
                    running[(x, y)][0].append(Room(line[3], [[],[]], Door(line[4], line[5].isalpha(), line[6], doorkey)))
                
                elif line[0] == 'INTER':
                    # INTER GROUND X Y NAME COMP
                    #   0     1    2 3  4    5
                    if line[1] == 'GROUND':
                        x, y = int(line[2]), int(line[3])
                        name = line[4]
                        composition = line[5]
                        running[(x, y)][1].append(Interactable(name, composition))
                    else:
                        # INTER X Y NAME COMP
                        #   0   1 2  3    4
                        x = int(line[1])
                        y = int(line[2])
                        name = line[3]
                        composition = line [4]
                        running[(x, y)][0].append(Interactable(name, composition))

                elif line[0] == 'NPC':
                    # NPC X Y FILE
                    #  0  1 2  3
                    x, y = int(line[1]), int(line[2])
                    running[(x, y)][0].append(NPC(line[3]))

                elif line[0] == 'CONT':
                    # CONT X Y NAME COMP
                    #  0   1 2  3    4
                    x, y = int(line[1]), int(line[2])
                    running[(x, y)][0].append(Container(line[3], line[4], []))

                elif line[0] == 'INSI':
                    # INSI CONTNAME OBJCLASS X Y NAME COMP
                    #   0     1       2      3 4  5    6 
                    x, y = int(line[3]), int(line[4])
                    for item in running[(x, y)][0]:
                        if item.name.lower() == line[1].lower():
                            # Puts interactable on ground in room
                            if isinstance(item, Room) and line[2] == 'INTER':
                                item.contents[1].append(Interactable(line[5], line[6]))
                                break
                            # Puts container inside room
                            elif isinstance(item, Room) and line[2] == 'CONT':
                                item.contents[0].append(Container(line[5], line[6], []))
                                break
                            # Puts interactable in container on map
                            elif isinstance(item, Container):
                                item.contents.append(Interactable(line[5], line[6]))
                                break

                elif line[0] == 'SPEC':
                    # SPEC ROOMNAME CONTNAME INTER X Y NAME COMP
                    #  0      1        2       3   4 5  6    7
                    x, y = int(line[4]), int(line[5])
                    for item in running[(x, y)][0]:
                        if item.name.lower() == line[1].lower():
                            for entity in item.contents[0]:
                                if entity.name.lower() == line[2].lower():
                                    entity.contents.append(Interactable(line[6], line[7]))
                                    break
                            break

                elif line[0] == 'RNPC':
                    # RNPC X Y FILE ROOMNAME
                    #  0  1 2   3    4      
                    x, y = int(line[1]), int(line[2])
                    for item in running[(x, y)][0]:
                        if isinstance(item, Room) and item.name.lower() == line[4].lower():
                            item.contents[0].append(NPC(line[3]))
        self.contents = running
    def check(self, pos):
        return self.contents[pos]

    def link(self, somemap, coordinates):
        """(Mapp, Mapp, tuple of ints) -> None

        Links two existing maps together so that you can travel from one 
        map to another using the enter function in the main.py"""
        self.contents[coordinates][0].append(somemap)


class Room:
    def __init__(self, name, contents, door):
        self.name = name
        #self.num = num
        self.contents = contents
        self.door = door

    def examine(self):
        print("You examine the {}, it is solid maybe look at the {}".format(
                    self.name, self.door.name))


class Interactable:
    
    def __init__(self, name, composition):
        #(self, name, weight, composition, num)
        self.name = name
        #self.weight = weight
        self.madeof = composition
        #self.num = num

    def examine(self):
        print("You examine the {}, it is made of {}\n".format(self.name, self.madeof))

    def __str__(self):
        return '{} {}'.format(self.madeof, self.name).title()


class Door(Interactable):
    
    def __init__(self, name, locked, composition, key=None):
        super().__init__(name, composition)
        self.locked = locked
        self.key = key
        if locked:
            self.lcked = 'locked'
        else:
            self.lcked = 'unlocked'
    
    def open(self, protag):
        if self.locked:
            for item in protag.person:
                if self.key.lower() == str(item).lower():
                    self.locked = False
                    self.lcked = 'unlocked'
                    print('You unlocked the {} with {}'.format(self.name, self.key))
                    return True

            print('The {} is locked'.format(self.name))
            return False
        else:
            return True

    def examine(self):
        print('Door appears to made of {} and is {}'.format(self.madeof, self.lcked))


class Container(Interactable):
    def __init__(self, name, composition, contents):
        self.contents = contents
        self.madeof = composition
        self.name = name

    def examine(self):
        if self.contents == []:
            print('{} is made of {} and is empty'.format(self.name, self.madeof))
        else:
            print('>Contents of the {} {} are<'.format(self.madeof, self.name))
            for item in self.contents:
                print('{}'.format(item.name))

class NPC():
    """Generates NPC objects"""
    def __init__(self, dialogfile):
        """(str, file.ext, str) -> None

        NPCs need a name and a file containing their dialogue trees. The
        dialogues in the file will be in the correct order such that the
        first talk is informative, the second is either a small reminder
        or perhaps exhibits annoyance of the character and in some cases
        a refusal to repeat.

        Coversations that are trigger by keyitems are at the end are marked
        by the word KEY and all dialogue should be typed as to how it will
        appear in the interpreter. NPCs without key items will ignore all
        key item dialogue and just act as direction givers.

        NAME name
        DIALOGUE pew pew pew pew
        NEWTXT
        DIALOGUE meow meow meow
        KEYITEM KITTY
        KEY
        Thank you for finding my animal

        """
        self.dialog = []
        temp = ''
        key = False
        self.convo = 0
        self.give = None
        self.keyitem = None
        # dissects character's dialogue file
        with open(dialogfile, 'r') as scrapfile:
            for line in scrapfile:
                line = line.split()
                if line[0] == 'NAME':
                    self.name = ' '.join(line[1:]).strip()
                elif line[0] == 'NEWTXT':
                    self.dialog.append(temp)
                    temp = ''
                elif line[0] == 'GIVE':
                    self.give = Interactable(line[1], line[2])
                elif line[0] == 'KEYITEM':
                    self.keyitem = ' '.join(line[1:])
                elif line[0] == 'DIALOG':
                    temp += '{}\n'.format(' '.join(line[1:]))
                elif line[0] == 'KEY':
                    key = True
                    break
            self.dialog.append(temp)
            if key:
                self.keyconvo = scrapfile.read()

    def talk(self, protag):
        # if NPC has key item checks player's person, display new dialogue
        if self.keyitem != None:
            for item in protag.person:
                if str(item).lower() == self.keyitem.lower():
                    protag.person.remove(item)
                    self.dialog = ['Thank you {} for your help\n'.format(protag.name)]
                    protag.score += materialvalue[item.madeof] + 10
                    if self.give != None:
                        protag.person.append(self.give)
                        print("You've obtained a {}".format(str(self.give)))
                    return self.keyconvo
        # if player has item in question they are thanked and no additional
        # dialogue needed
        if self.dialog == ['Thank you so much for your help\n']:
            return self.dialog[0]
            # Allows for several 'hint' like dialogs
        elif self.convo < len(self.dialog) - 1:
            self.convo += 1
            return self.dialog[self.convo - 1]
        return self.dialog[self.convo]

    def examine(self):
        print('They step away from you leery of your intentions')

materialvalue = {
                'wood':10, 'stone':15, 'metal': 20, 'gold':30, 'flesh':-30,
                'bone':-20, 'meat':-10, 'evil':-5, 'cursed':-50, 'cat':0,
                'paper': 40, 'glass': 20, 'platinum': 100
                }