from player import *

def mainloop():
    with open('intro', 'r') as intro:
        print(intro.read())
    protag = Player('Admin Istrator', [], (0, 0))
    while True:
        action = input('ADVENTURE TIME> ')
        action = action.split()
        if  action[0].lower() == 'quit':
            return
        elif action[0] == 'm':
            protag.move(action[1])
            print(protag.pos)
        elif action[0] == 'backpack':
            if len(action) == 1:
                protag.backpack.view()

if __name__ == '__main__':
    mainloop()