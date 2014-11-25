from player import *
from battle import *

def mainloop():
    with open('intro', 'r') as intro:
        print(intro.read())
    protag = Player('Admin Istrator', [], (0, 0))
    protag.person.append(Sword('aSword', 5, 3, (10, 11)))
    while True:
        action = input('ADVENTURE TIME> ')
        action = action.split()
        if  action[0].lower() == 'quit':
            return
        elif action[0] == 'm':
            protag.move(action[1])
        elif action[0] == 'backpack' or action[0] == 'pack':
            protag.pack_view()
        elif action[0] == 'me':
            protag.person_view()
        elif action[0] == 'put':
            protag.put(action[1])
        elif action[0] == 'pull':
            protag.pull(action[1])


if __name__ == '__main__':
    mainloop()