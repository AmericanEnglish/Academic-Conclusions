class Mapp:
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents
            #contents is a dict of tuple: list objects
            # {(0, 0):[Room, Enemey], (0,1): []} 
    
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
    
    def __init__(self, name, locked, composition):
        super().__init__(name, composition)
        self.locked = locked
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


class Table(Interactable):
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

class Chair(Interactable):
    pass

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

