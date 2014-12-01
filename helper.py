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
        fileout.write('START {} {}'.format(start[0], start[1]))
        answer = None
        while answer != done:
            answer = input('Obj Type: ').lower()
            if answer == 'cont':
                x, y = input('x y').strip().split()
                name = input('Container name: ')
                composition = input('Composition: ')
                contents = input('Contents? (y/n): ')
                fileout.write('CONT {} {} {} {}'.format(x, y, name, composition))
                if contents == 'y':
                    contentname = input('Item Name: ')
                    contentcomp = input('Item Composition: ')
                    fileout.write('INSI {} INTER {} {} {} {}'.format(name, x, y, contentname, contentcomp))
            elif answer == 'room':
                name = input('Room name: ')
                x, y = input('x y').strip().split()
                doornam = input('Door name: ')
                locked = input('Locked?: ')
                if locked[0].lower() != 'y':
                    locked = 1
                composition = input('Composition: ')
                Doorkey = input('Door key (None/name): ')
                if Doorkey.lower() == 'none':
                    fileout.write('ROOM {} {} {} {} {} {} {}'.format(x, y, name, doornam, locked, composition))
                else:
                    fileout.write('ROOM {} {} {} {} {} {} {}'.format(x, y, name, doornam, locked, composition, Doorkey))
                    keyquestion = input('Random gen key location?: ')
                    if keyquestion == 'n':
                        x2, y2 = input('Key x y: ')
                        fileout.write('# Key location, Mutable')
                        fileout.write('INTER GROUND {} {} {}'.format(x2, y2, Doorkey))
                    else:
                        x2, y2 = randint(0, int(dimensions[0])), randint(0,  int(dimensions[1]))
                        fileout.write('# Key location, Mutable')
                        fileout.write('INTER GROUND {} {} {}'.format(x2, y2, Doorkey))
                contents = input('Contents?: ')
                if contents = 'y'


    convert_to(outputfile, outputfile + '.bak')
