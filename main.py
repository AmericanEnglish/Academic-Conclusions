from player import *
from battle import *
from maps import *
materials = {'wood':10}

map1 = Mapp('Small Town',
                {(0,0): [[
                            Room('A Room',
                                [[Table('Garbage Table', 'wood', [Sword('Meow Blade')])],
                                [Sword('Plain')]],
                                 Door('Room Door', False, 'wood'))],[Sword('Cooler Sword')]],
                (0,1): [[],[]]
                }
            )

def maploop(currentmap):
    inmap = True
    while inmap:
        action = input('={}=> '.format(currentmap.name))
        action = action.lower().strip().split()
        if len(action) > 1:
            action = [action[0], ' '.join(action[1:])]
        if len(action) < 1:
            print('')
        
        elif  action[0].lower() == 'quit':
            if input('Are you sure? (y/n): ').lower() == 'y':
                return
        
        elif action[0] == 'm':
            protag.move(action[1])
        
        elif action[0] == 'pack':
            protag.pack_view()
        
        elif action[0] == 'me':
            protag.person_view()
        
        elif action[0] == 'put':
            protag.put(action[1])
        
        elif action[0] == 'pull':
            protag.pull(action[1])
        
        elif action[0] == 'examine' and len(action) == 2:
            for item in currentmap.check(protag.pos)[0]:
                if isinstance(item, Room) and 'door' in action[1]:
                    item.door.examine()
                    break
                elif action[1] == item.name.lower():
                    item.examine()
                    break
            protag.examine(action[1])
            print('')

        
        elif action[0] == 'enter' and len(action) > 1:
            for item in currentmap.check(protag.pos)[0]:
                if action[1] == item.name.lower() and isinstance(item, Room):
                    roomloop(protag, item)
                elif action[1] == item.name.lower() and isinstance(item, Mapp):
                    inmap = False
                    protag.map = item

        elif action[0] == 'exit':
            print(">You're already outside!<\n")

        elif action[0] == 'look':
            print('>Around you see<')
            for item in currentmap.check(protag.pos)[0]:
                if 'door' not in item.name:
                    print(item.name)
            print('')
        
        elif action[0] == 'ground':
            if currentmap.check(protag.pos)[1] == []:
                print('>There is nothing on the ground<\n')
            else:
                print('>On the ground you see<')
                for item in currentmap.check(protag.pos)[1]:
                    print('{}'.format(item.name))
                print('')

        elif action[0] == 'pickup':
            for item in currentmap.check(protag.pos)[1]:
                if action[1] == item.name.lower():
                    protag.person.append(item)
                    currentmap.check(protag.pos)[1].remove(item)
                    print('You picked up {}\n'.format(item.name))

        elif action[0] == 'drop':
            for item in protag.person:
                if action[1] == item.name.lower():
                    protag.person.remove(item)
                    currentmap.check(protag.pos)[1].append(item)
                    print('You dropped {} on the ground\n'.format(item.name))

        else:
            print('Not a valid command\n')

def roomloop(protag, currentroom):
    protag.room = currentroom
    print("You entered {}\n".format(currentroom.name))
    while True:
        action = input('={}=> '.format(currentroom.name))
        action = action.lower().strip().split()
        if len(action) > 1:
            action = [action[0], ' '.join(action[1:])]
        
        if len(action) < 1:
            print('')

        elif action[0] == 'pack':
            protag.pack_view()
        
        elif action[0] == 'me':
            protag.person_view()
        
        elif action[0] == 'put':
            protag.put(action[1])
        
        elif action[0] == 'pull':
            protag.pull(action[1])
        
        elif action[0] == 'examine' and len(action) == 2:
            for item in currentroom.contents[0]:
                if action[1] in item.name.lower():
                    item.examine()
                    break
            protag.examine(action[1])
        
        elif action[0] == 'enter':
            print(">You're already in the {}<\n".format(currentroom.name))
        
        elif action[0] == 'exit':
            print(">You exit the {}<\n".format(currentroom.name))
            return

        elif action[0] == 'look':
            print('>Around you see<')
            for item in currentroom.contents[0]:
                print(item.name)
            print('')
        
        elif action[0] == 'ground':
            if currentroom.contents[1] == []:
                print('>There is nothing on the ground<\n')
            else:
                print('>On the ground you see<')
                for item in currentroom.contents[1]:
                    print('{}'.format(item.name))
                print('')

        elif action[0] == 'pickup':
            for item in currentroom.contents[1]:
                if action[1] == item.name.lower():
                    protag.person.append(item)
                    currentroom.contents[1].remove(item)
                    print('>You picked up {}<\n'.format(item.name))

        elif action[0] == 'drop':
            for item in protag.person:
                if action[1] == item.name.lower():
                    protag.person.remove(item)
                    currentroom.contents[1].append(item)
                    print('>You dropped {} on the ground<'.format(item.name))
            print('')
        elif action[0] == 'take':
            action = ' '.join(action).split()
            action = [action[0],
                    ' '.join(action[1:action.index('from')]),
                    ' '.join(action[action.index('from') + 1:])]
            for item in currentroom.contents[0]:
                if action[2] == item.name.lower():
                    pass

        else:
            print('Not a valid command, type help for help')

def main(protag):
    protag.map = map1
    while True:
        maploop(protag.map)



if __name__ == '__main__':
    with open('intro', 'r') as intro:
        print(intro.read())
    protag = Player('Admin Istrator', [], (0, 0))
    protag.map = map1
    main(protag.map)