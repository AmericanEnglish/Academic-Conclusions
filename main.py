from player import *
from battle import *
from maps import *

materials = {'wood':10}
map1 = Mapp(
                {(0,0): [
                            Room('Room',
                                Door(
                                    'Medium Door', 
                                    20, 
                                    False, 
                                    'wood',
                                    1),
                                [],
                                1,
                                ),
                            Sword('Sweet Sword', 5, 3, (10, 11))
                        ],
                (0,1): []
                }
            )

def mainloop():
    while True:
        action = input('=OUTSIDE=> ')
        action = action.lower().strip().split()

        if len(action) < 1:
            print('')
        
        elif len(action) <= 2:
            if  action[0].lower() == 'quit':
                if input('Are you sure? (y/n): ').lower() == 'y':
                    return
            
            elif action[0] == 'm' and len(action) == 2:
                protag.move(action[1])
            
            elif action[0] == 'pack':
                protag.pack_view()
            
            elif action[0] == 'me':
                protag.person_view()
            
            elif action[0] == 'put':
                protag.put(action[1])
            
            elif action[0] == 'pull':
                protag.pull(action[1])
            
            elif action[0] == 'examine' and len(action) > 1:
                protag.examine(action[1])
            
            elif action[0] == 'enter':
                protag.enter(action[1])
                inroom(protag, protag.room)

            elif action[0] == 'exit':
                print("You're already outside!\n")

            elif action[0] == 'look':
                print('Around you see:')
                for item in protag.map.check(protag.pos):
                    print(item.name)
                print('')
        
        else:
            print('')


if __name__ == '__main__':
    with open('intro', 'r') as intro:
        print(intro.read())
    protag = Player('Admin Istrator', [], (0, 0))
    protag.map = map1
    protag.person.append(Sword('aSword', 5, 3, (10, 11)))
    protag.person.append(Sword('SuperSword', 5, 3, (10, 11)))
    mainloop()