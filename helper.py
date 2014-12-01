#LABEL THING THING NAME_NAME
from random import randint
def convert_to(original, output):
    with open(original, 'r') as filein:
        with open(output, 'w') as fileout:
            string = filein.read()
            for char in string:
                if char == ' ':
                    fileout.write('_')
                elif char == '_':
                    fileout.write(' ')
                else:
                    fileout.write(char)
    print('File in: {}'.format(original))
    print('File out: {}'.format(output))

def convert_from(original, output):
    with open(original, 'r') as filein:
        with open(output, 'w') as fileout:
            string = filein.read()
            for char in string:
                if char == ' ':
                    fileout.write('_')
                elif char == '_':
                    fileout.write(' ')
                else:
                    fileout.write(char)
    print('File in: {}'.format(original))
    print('File out: {}'.format(output))

def writemaps():
    outputfile = input('Output name: ')
    mapname = input('Map name: ').strip()
    dimensions = input('Max X Y: ').strip().split()
    start = input('Start: ').strip().split()
    with open(outputfile, 'w') as fileout:
        fileout.write('NAME {}\n'.format(mapname))
        fileout.write('DIMX 0 {}\n'.format(dimensions[0]))
        fileout.write('DIMY 0 {}\n'.format(dimensions[1]))
        fileout.write('START {} {}\n'.format(start[0], start[1]))
        fileout.write('\n')
        answer = None
        while answer != 'done':
            answer = input('Obj Type: ').lower()
            if answer == 'cont':
                x, y = input('x y: ').strip().split()
                name = input('Container name: ')
                composition = input('Composition: ')
                contents = input('Contents? (y/n): ')
                fileout.write('CONT {} {} {} {}\n'.format(x, y, name, composition))
                if contents == 'y':
                    while True:
                        contentname = input('{}|Item Name: '.format(name))
                        contentcomp = input('Item Composition: ')
                        if contentname != 'done':
                            fileout.write('INSI {} INTER {} {} {} {}\n'.format(name, x, y, contentname, contentcomp))
                        elif contentname == 'done':
                            break
            
            elif answer == 'room':
                name = input('Room name: ')
                x, y = input('x y: ').strip().split()
                doornam = input('Door name: ')
                locked = input('Locked?: ')
                if locked[0].lower() != 'y':
                    locked = 1
                composition = input('Composition: ')
                Doorkey = input('Door key (None/name): ')
                if Doorkey.lower() == '':
                    fileout.write('ROOM {} {} {} {} {} {}\n'.format(x, y, name, doornam, locked, composition))
                else:
                    fileout.write('ROOM {} {} {} {} {} {} {}\n'.format(x, y, name, doornam, locked, composition, Doorkey))
                    keyquestion = input('Random gen key location?: ')
                    if keyquestion == 'n':
                        x2, y2 = input('Key x y: ').strip().split()
                        fileout.write('# Key location, Mutable\n')
                        fileout.write('INTER GROUND {} {} {} {}\n'.format(x2, y2, Doorkey, composition))
                    else:
                        x2, y2 = randint(0, int(dimensions[0])), randint(0,  int(dimensions[1]))
                        fileout.write('# Key location, Mutable\n')
                        fileout.write('INTER GROUND {} {} {}\n'.format(x2, y2, Doorkey))
                fodder = input('{} Contents? (y/n): '.format(name))
                if fodder == 'y':
                    while True:
                        objtype = input('CONT, INTER, NPC: ')
                        if objtype == 'cont':
                            contname = input('Container name: ')
                            composition = input('Composition: ')
                            fileout.write('INSI {} CONT {} {} {} {}\n'.format(name, x, y, contname, composition)) 
                            if input('{} Contents? (y/n):'.format(contname)).lower() == 'y':    
                                while True:
                                    contentname = input('Item Name: ')
                                    contentcomp = input('Item Composition: ')
                                    if contentname != 'done':
                                        fileout.write('SPEC {} {} INTER {} {} {} {}\n'.format(name, contname, x, y, contentname, contentcomp))
                                    elif contentname == 'done':
                                        break
                        elif objtype == 'inter':
                            while True:
                                contname = input('{}| Item name: '.format(name))
                                contentcomp = input('Composition: ')
                                if contname == 'done':
                                    break
                                elif contname != 'done':
                                    fileout.write('INSI {} INTER {} {} {} {}\n'.format(name, x, y, contname, contentcomp))
                        elif objtype == 'npc':
                            npc = input('Filename: ')
                            fileout.write('RNPC {} {} {} {}\n'.format(x, y, npc, name))
                        else:
                            break

            elif answer == 'inter':
                name = input('Item name: ')
                x, y = input('x y: ').split()
                composition = input('Composition: ')
                fileout.write('INTER GROUND {} {} {} {}\n'.format(x, y, name, composition))

            elif answer == 'npc':
                x, y = input('x y:')
                npc = input('Filename: ')
                fileout.write('NPC {} {} {}\n'.format(x, y, npc))

            else:
                break
    convert_to(outputfile, outputfile + '.bak')
