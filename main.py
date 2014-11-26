from player import *
from battle import *
from maps import *

materials = {'wood':10}

def mainloop():
    with open('intro', 'r') as intro:
        print(intro.read())
    protag = Player('Admin Istrator', [], (0, 0))
    protag.person.append(Sword('aSword', 5, 3, (10, 11)))
    while True:
        action = input('ACTION > ')
        action = action.lower().strip().split()
        if len(action) < 1:
            print('')
        
        elif  action[0].lower() == 'quit':
            if input('Are you sure? (y/n): ').lower() == 'y':
                return
        
        elif action[0] == 'm' and len(action) == 2:
            protag.move(action[1])
        
        elif action[0] == 'backpack' or action[0] == 'pack':
            protag.pack_view()
        
        elif action[0] == 'me':
            protag.person_view()
        
        elif action[0] == 'put':
            protag.put(action[1])
        
        elif action[0] == 'pull':
            protag.pull(action[1])
        
        elif action[0] == 'examine':
            protag.examine(action[1])
        
        elif action[0] == 'enter':
            if protag.room != None:
                print("You're already in {}".format(protag.room.name))
            else:
                for item in mapp.check(protag.pos):
                    if action[1] == item.name.lower():                
                            protag.enter(action[1])
        else:
            print('')


if __name__ == '__main__':
    mainloop()