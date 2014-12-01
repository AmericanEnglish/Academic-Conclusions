#LABEL THING THING NAME_NAME
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

def writemaps(outputfile):
    mapname = input('Map name: ').strip()
    dimensions = input('Max X Y: ').strip().split()
    start = input('Start: ').strip().split()
    with open(outputfile, 'w') as fileout:
        fileout.write('NAME {}\n'.format(mapname))
        fileout.write('DIMX 0 {}\n'.format(dimensions[0]))
        fileout.write('DIMY 0 {}\n'.format(dimensions[1]))
        fileout.write('START {} {}'.format(start[0], start[1]))
    convert_to(outputfile, outputfile + '.bak')
