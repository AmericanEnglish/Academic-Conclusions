class Mapp:
    def __init__(self, name, contents, start):
        self.name = name
        self.contents = contents
        self.start = start
            #contents is a dict of tuple: list objects
            # {(0, 0):[[Room, Enemey][Ground Things, Here]], (0,1): [[],[]]} 
    
    def check(self, pos):
        return self.contents[pos]


class Room:
    def __init__(self, name, contents, door):
        self.name = name
        #self.num = num
        self.contents = contents
        self.door = door

    def examine(self):
        print("You examine the building, it is solid")


class Interactable:
    
    def __init__(self, name, composition):
        #(self, name, weight, composition, num)
        self.name = name
        #self.weight = weight
        self.madeof = composition
        #self.num = num

class Door(Interactable):
    
    def __init__(self, name, locked, composition, key=None):
        super().__init__(name, composition)
        self.locked = locked
        self.key = key
        if locked:
            self.lcked = 'locked'
        else:
            self.lcked = 'unlocked'
    
    #def open(self, thing, toon):
    #    thingobj = None
    #    for item in toon:
    #        if item.name == thing:
    #            thingobj = item
    #    if thingobj == None:
    #        return False
    #    
    #    if self.locked:
    #        print('You try to open the door with the {}'.format(thingobj.name))
    #        if isinstance(thingobj, Key):
    #            if thingobj.unlock == self.num:
    #                return True
    #            return False
    #        elif isinstance(thingobj, Sword):
    #            return thingobj.pry(self.madeof)
    #        return False
    #    return True


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
            print('>On the {} {} is<'.format(self.madeof, self.name))
            for item in self.contents:
                print('{}'.format(item.name))
            print('')

class NPC():
    """Generates NPC objects"""
    def __init__(self, name, dialogfile, keyitem=None):
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
        KEY
        Thank you for finding my animal

        """
        self.name = name
        self.dialog = []
        temp = ''
        key = False
        self.convo = 0
        self.keyitem = keyitem
        # dissects character's dialogue file
        with open(dialogfile, 'r') as scrapfile:
            for line in scrapfile:
                line = line.split()
                if line[0] == 'NAME':
                    self.name = ' '.join(line[1:]).strip()
                elif line[0] == 'NEWTXT':
                    self.dialog.append(temp)
                    temp = ''
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
                if item.name.lower() == self.keyitem.lower():
                    protag.person.remove(item)
                    self.dialog = ['Thank you so much for you help']
                    return self.keyconvo
        # if player has item in question they are thanked and no additional
        # dialogue needed
        if self.dialog == ['Thank you so much for you help\n']:
            return self.dialog[0]

        elif self.convo < len(self.dialog) - 1:
            self.convo += 1
            return self.dialog[self.convo - 1]
        return self.dialog[self.convo]


def map_gen(filename):
    running = {}
    with open(filename, 'r') as somefile:
        mapname = somefile.readline().strip().split()[1]
        
        nextline = somefile.readline().strip()
        dimensionx = (int(nextline[1]), int((nextline[2])))
        
        nextline = somefile.readline().strip()
        dimensiony = (int(nextline[1]), int(nextline[2]))
        
        nextline = somefile.readline().strip().split()
        #generates empty map contents and all the coordinates
        for x in range(dimensionx[1] + 1):
            for y in range(dimensiony[1] + 1):
                running[(x , y)] = [[],[]]

        for line in somefile:
            line = line.strip().split()
            if line[0] = 'INTER':
                # INTER GROUND X Y NAME COMP
                #   0     1    2 3  4    5
                if line[1] == 'GROUND':
                    x = int(line[2])
                    y = int(line[3])
                    name = line[4].replace('_', ' ')
                    composition = line [5]
                    running[(x, y)][1].append(Interactable(name, composition))
                else:
                    x = int(line[1])
                    y = int(line[2])
                    name = line[3].replace('_', ' ')
                    composition = line [4]
                    running[(x, y)][0].append(Interactable(name, composition))

            elif line[0] == 'NPC':
                # NPC X Y NAME FILE KEYITEM
                #  0  1 2  3    4     5
                if len(line) == 5:
                    keyitem = line[5]
                else:
                    keyitem = None
                running[((int(line[1]), int(line[2])))][0].append(
                            NPC(line[3].replace('_', ' '), line[4], keyitem))

            elif line[0] == 'CONT':
                # CONT X Y NAME COMP
                #  0   1 2  3    4
                running[((int(line[1]), int(line[2])))][0].append(Container(line[3], line[4]. []))

            elif line[0] == 'INSI':
                # INSIDE CONTNAME OBJCLASS X Y NAME COMP
                #   0       1       2      3 4  5    6 
                x, y = int(line[3]), int(line[4])
                for item in running[(x, y)][0]:
                    if item.name.lower() == line[1].lower():
                        # Put interactable on ground in room
                        if isinstance(item, Room) and line[2] == 'INTER':
                            item.contents[1].append(Interactable(line[5], line[6]))
                            break
                        # Puts container inside room
                        elif isinstance(item, Room) and line[2] == 'CONT':
                            item.contents[0].append(Container(line[5], line[6], []))
                            break
                        elif isinstance(item, Container):
                            item.contents.append(Interactable(line[5], line[6]))
                            break

            elif line[0] == 'SPEC':
                # SPEC ROOMNAME CONTNAME INTER X Y NAME COMP
                #  0      1        2       3   4 5  6    7
                x, y = line[4], line[5]
                for item in running[(x, y)]:
                    if item.name.lower() == line[1].lower():
                        for entity in item.contents[0]:
                            if entity.name.lower() == line[2].lower():
                                entity.append(Interactable(line[6], line[7]))
                                break
                        break