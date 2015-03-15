import psycopg2
from os import listdir
from player import *
from maps import *
from time import perf_counter
from helper import helpcom
from introduction import *

#for home use
con = psycopg2.connect(host='120.0.0.1', database='postgres', user='postgres', password='password')

#for class use
#con = psycopg2.connect(host='120.0.0.1', database='cs350', user='student', password='student')
cursor = con.cursor()
if 'donotdelete' in listdir():
    with open('donotdelete', 'a+') as test:
        fod = test.read()
        if 'R28gZ28gcG93ZXIgcmFuZ2Vycw==' in fod:
            answer = input('Start a new game? (y/n)').lower()
            if 'y' in answer :
                with open('data/eraseall.sql') as nukedata:
                    cur.execute(nukedata.read())
                with open('data/tables.sql', 'r') as execution:
                    cur.execute(execution.read())
        elif 'R28gZ28gcG93ZXIgcmFuZ2Vycw==' not in fod:
            with open('data/tables.sql', 'r') as execution:
                cur.execute(execution.read())
            test.append('\nR28gZ28gcG93ZXIgcmFuZ2Vycw==')
else:
    print('Creating database . . .')
    with open('data/tables.sql', 'r') as execution:
        cur.execute(execution.read())


cur.close()
maps = Mapp(con)


def maploop(currentmap):
    """(Mapp) -> None

    These function is used for running movement and actions on a generic
    Mapp object. The protag is stored in the global frame and is then
    used and mutated in relation to the Mapp object and the commands that
    are input by the user."""
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
                return True
        
        elif action[0] == 'm':
            protag.move(action[1])
            if protag.pos[0] > currentmap.x or protag.pos[0] < 0:
                # Provides a warning if the map is left
                if protag.pos[0] > currentmap.x + 1 or protag.pos[0] < -1:
                    print('You were eaten by wolves')
                    return True
                elif protag.pos[0] == currentmap.x + 1 or protag.pos[0] == -1:
                    print('You have left the saftey of the {}, move farther and you might not move'.format(
                                                        currentmap.name))
                    print('at all. Quickly there is no time, head back from whence you came.\n')
            elif protag.pos[1] > currentmap.y or protag.pos[1] < 0:
                # Provides a warning if the map is left
                if protag.pos[1] > currentmap.y + 1 or protag.pos[1] < -1:
                    print('You were eaten by cannibals')
                    return True
                elif protag.pos[1] == currentmap.y + 1 or protag.pos[1] == -1:
                    print('You have left the saftey of the {}, move farther and you might not move'.format(
                                                        currentmap.name))
                    print('at all. Quickly there is no time, move back from whence you came.\n')
        
        elif action[0] == 'pack':
            protag.pack_view()
        
        elif action[0] == 'me':
            protag.person_view()
        
        elif action[0] == 'put':
            protag.put(action[1])
        
        elif action[0] == 'pull':
            if len(protag.person) < 5:
                protag.pull(action[1])
            else:
                print("As you try to pull {} from your pack, you can't seem to grab it")
                print("perhaps you should put items into your pack first. Free up those hands")
        
        elif action[0] == 'examine' and len(action) == 2:
            # check to make sure item / room / door in question is in the area
            for item in currentmap.check(protag.pos)[0]:
                if isinstance(item, Room) and 'door' in action[1]:
                    item.door.examine()
                    break
                # if the item in question isn't a door it's a room
                elif action[1] == item.name.lower():
                    item.examine()
                    break
            # if item is neither a door or room, search's player's person
            protag.examine(action[1])

        
        elif action[0] == 'enter' and len(action) > 1:
            # checks for any rooms in the area that might be enterable
            for item in currentmap.check(protag.pos)[0]:
                # allows for room entry
                if action[1] == item.name.lower() and isinstance(item, Room):
                    roomloop(protag, item)
                # allows for Mapps to be entered
                elif action[1] == item.name.lower() and isinstance(item, Mapp):
                    inmap = False
                    protag.map = item
                    protag.pos = item.start
            print('')

        elif action[0] == 'exit':
            print(">You're already outside!<\n")

        elif action[0] == 'look':
            if protag.pos[0] < currentmap.x + 1 and protag.pos[0] >= 0:
                if protag.pos[1] < currentmap.y + 1 and protag.pos[1] >= 0:
                    print('>Around you see<')
                    for item in currentmap.check(protag.pos)[0]:
                        print(item.name)
                    print('')
                else:
                    print('You took too long and were eaten by wolves AND cannibals')
                    return True
            else:
                print('You took too long and were eaten by wolves AND cannibals')
                return True
            
        elif action[0] == 'ground':
            if currentmap.check(protag.pos)[1] == []:
                print('>There is nothing on the ground<\n')
            else:
                print('>On the ground you see<')
                for item in currentmap.check(protag.pos)[1]:
                    print('{}'.format(item.name))
                print('')

        elif action[0] == 'pickup' and len(action) == 2:
            for item in currentmap.check(protag.pos)[1]:
                if action[1] == item.name.lower() and len(protag.person) < 5:
                    # this will be put into the Player methods later, maybe
                    protag.person.append(item)
                    currentmap.check(protag.pos)[1].remove(item)
                    print('You picked up {}\n'.format(item.name))
                elif action[1] == item.name.lower() and len(protag.person) >= 5:
                    print('You fumble the {} and it falls back on the ground.'.format(item.name))
                    print('It would seem you are carrying too much in your hands to hold anymore.')

        elif action[0] == 'drop':
            for item in protag.person:
                if action[1] == item.name.lower():
                    # this will be put into the player methods later
                    protag.person.remove(item)
                    currentmap.check(protag.pos)[1].append(item)
                    print('You dropped {} on the ground\n'.format(item.name))
        
        elif action[0] == 'talk':
            # if user types wrong name somevar will help print a newline
            somevar = 0
            if len(action) > 1:
                for item in currentmap.check(protag.pos)[0]:
                    somevar += 1
                    if isinstance(item, NPC) and action[1] == item.name.lower():
                        #somevar now knows an NPC was found and no extra \n
                        somevar -= 1
                        print('<>{}:\n{}'.format(item.name, item.talk(protag)))
                if somevar == len(currentmap.check(protag.pos)[0]):
                    print('')
            # if just talk is typed, protag talks to all NPCs in area.   
            else:
                somevar = 0
                for item in currentmap.check(protag.pos)[0]:
                    somevar += 1
                    if isinstance(item, NPC):
                        somevar -= 1
                        print('<>{}:\n{}'.format(item.name, item.talk(protag)))
                if somevar == len(currentmap.check(protag.pos)[0]):
                    print('Not a valid command, type help for help\n')
        
        elif action[0] == 'take':
            # take requires a second marker called from. This requiers action
            # to be reconfigured
            if 'from' in action:
                action = ' '.join(action).split()
                action = [action[0],
                        ' '.join(action[1:action.index('from')]),
                        ' '.join(action[action.index('from') + 1:])]
                for item in currentmap.contents[protag.pos][0]:
                    if action[2] == item.name.lower():
                        # will be added as table/object method later
                        for thing in item.contents:
                            if thing.name.lower() == action[1]:
                                protag.person.append(thing)
                                item.contents.remove(thing)
                                print('You took {} from {}'.format(thing.name, item.name))
        
        elif action[0] == 'help' and len(action) == 2:
            print(helpcom(action[1]))
        
        else:
            print('Not a valid command, type help for help\n')
    main(protag, protag.map)

def roomloop(protag, currentroom):
    """(Player, Room) -> None

    This function is used for a player's interaction with the room and its 
    contents. Although some 'action' words are the same the objects some
    interactions are not exactly the same."""
    protag.room = currentroom
    #If the door is locked they are 'kicked' from the room
    if not currentroom.door.open(protag):
        return
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
            print('')
        
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
            # take requires a second marker called from. This requiers action
            # to be reconfigured
            if 'from' in action:
                action = ' '.join(action).split()
                action = [action[0],
                        ' '.join(action[1:action.index('from')]),
                        ' '.join(action[action.index('from') + 1:])]
                for item in currentroom.contents[0]:
                    if action[2] == item.name.lower():
                        # will be added as table/object method later
                        for thing in item.contents:
                            if thing.name.lower() == action[1]:
                                protag.person.append(thing)
                                item.contents.remove(thing)
                                print('You took {} from {}'.format(thing.name, item.name))
            print('')
        
        elif action[0] == 'talk':
            # if user types wrong name somevar will help print a newline
            somevar = 0
            if len(action) > 1:
                for item in currentroom.contents[0]:
                    somevar += 1
                    if isinstance(item, NPC) and action[1] == item.name.lower():
                        #somevar now knows an NPC was found and no extra \n
                        somevar -= 1
                        print('<>{}:\n{}'.format(item.name, item.talk(protag)))
                if somevar == len(currentroom.contents[0]):
                    print('')
            # if just talk is typed, protag talks to all NPCs in area.   
            else:
                somevar = 0
                for item in currentroom.contents[0]:
                    somevar += 1
                    if isinstance(item, NPC):
                        somevar -= 1
                        print('<>{}:\n{}'.format(item.name, item.talk(protag)))
                if somevar == len(currentroom.contents[0]):
                    print('')

        elif action[0] == 'help' and len(action) == 2:
            print(helpcom(action[1]))
        
        else:
            print('Not a valid command, type help for help\n')



def main(protag, startingmap):
    protag.map = startingmap
    protag.pos = protag.map.start
    death = False
    while death != True:
        death = maploop(protag.map)
    print('----Score: {}----\n'.format(score(protag)))
    answer = input('Try again?: ')
    if answer[0].lower() == 'y':
        main(protag, map0)
    else:
        print('Better luck next time!')

def score(protag):
    score = 0
    for item in protag.person:
        print('{}: {}'.format(str(item), materialvalue[item.madeof]))
        score += materialvalue[item.madeof]
    for item in protag.pack:
        print('{}: {}'.format(str(item), materialvalue[item.madeof]))
        score += materialvalue[item.score]
    print('Goodness Points: {}'.format(protag.score))
    return score + protag.score

materialvalue = {
                'wood':10, 'stone':15, 'metal': 20, 'gold':30, 'flesh':-30,
                'bone':-20, 'meat':-10, 'evil':-5, 'curse':-50, 'cat':0,
                'paper': 40, 'glass': 20, 'platinum': 100, 'cursed':-50,
                'cloth':15
                }

if __name__ == '__main__':
    name = introduction()
    protag = Player(name, map0.start)
    main(protag, map0)