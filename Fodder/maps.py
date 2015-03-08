import psycopg2

class Mapp:
    def __init__(self, connection):
            #contents is a dict of tuple: list objects
            # {(0, 0):[[Room, Enemey][Ground Things, Here]], (0,1): [[],[]]} 
            con = connection
            cur = con.cursor()

    def check(self, pos):
        return self.contents[pos]

    def link(self, somemap, coordinates):
        """(Mapp, Mapp, tuple of ints) -> None

        Links two existing maps together so that you can travel from one 
        map to another using the enter function in the main.py"""
        self.contents[coordinates][0].append(somemap)

    def examine(self):
        print('You see a path leading to a {}'.format(self.name))

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
        """(str, file.ext) -> None

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
        if self.keyitem == 'glass key 5':
            for item in protag.person:
                if str(item).lower() == self.keyitem.lower():
                    protag.person.append(self.give)
                    print("You've obtained a {}".format(self.give))
                    print(self.keyconvo)
                    print(score(protag))
                    print('Run game again to play.')
                    exit()
        
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