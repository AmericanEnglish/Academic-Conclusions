from player import *
from battle import *
from maps import *

materials = {'wood':10}
map1 = Mapp('Small Town',
                {(0,0): [[
                            Room('A Room',
                                [[],[]],
                                 Door('Room Door', False, 'wood'))],[Sword('Cooler Sword')]],
                (0,1): [[],[]]
                }
            )

def maploop(currentmap):
    while True:
        action = input('={}=> '.format(currentmap.name))
        action = action.lower().strip().split()
        if len(action) > 1:
            action = [action[0], ' '.join(action[1:])]
        elif len(action) < 1:
            print('')
        
        if  action[0].lower() == 'quit':
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
                if action[1] in item.name.lower():
                    item.examine()
                    break
            protag.examine(action[1])
        
        elif action[0] == 'enter':
            print('marker1')
            for item in currentmap.check(protag.pos)[0]:
                print('marker2', item.name)
                if action[1] == item.name.lower():
                    roomloop(protag, item)

        elif action[0] == 'exit':
            print("You're already outside!\n")

        elif action[0] == 'look':
            print('Around you see:')
            for item in currentmap.check(protag.pos)[0]:
                if 'door' not in item.name:
                    print(item.name)
            print('')
        
        elif action[0] == 'ground':
            if currentmap.check(protag.pos)[1] == []:
                print('>There is nothing on the ground<\n')
            else:
                print('On the ground you see:')
                for item in currentmap.check(protag.pos)[1]:
                    print('{}\n'.format(item.name))


        elif action[0] == 'pickup':
            for item in currentmap.check(protag.pos)[1]:
                if action[1] == item.name.lower():
                    protag.person.append(item)
                    currentmap.check(protag.pos)[1].remove(item)
                    print('You picked up {}\n'.format(item.name))

        else:
            print('')

def roomloop(protag, roomobj):
    protag.room = roomobj
    while True:
        action = input('={}=>'.format(roomobj.name))
        action = action.lower().strip().split()
        if len(action) > 1:
            action = [action[0], ' '.join(action[1:])]
        
        elif len(action) < 1:
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
            for item in roomobj[0]:
                if action[1] in item.name.lower():
                    item.examine()
                    break
            protag.examine(action[1])
        
        elif action[0] == 'enter':
            print("You're already in {}\n".format(roomobj.name))
        
        elif action[0] == 'exit':
            print("You exit {}\n".format(roomobj.name))
            return

        elif action[0] == 'look':
            print('Around you see:')
            for item in roomobj.contents:
                print(item.name)
            print('')
        
        elif action[0] == 'ground':
            if roomobj.contents[1] == []:
                print('>There is nothing on the ground<\n')
            else:
                print('On the ground you see:')
                for item in roomobj.contents[0]:
                    print('{}\n'.format(item.name))


if __name__ == '__main__':
    with open('intro', 'r') as intro:
        print(intro.read())
    protag = Player('Admin Istrator', [], (0, 0))
    protag.map = map1
    protag.person.append(Sword('a Sword'))
    protag.person.append(Sword('Super Sword'))
    maploop(protag.map)