import psycopg2
import getpass
from player import *
from maps import *
from time import perf_counter

# from introduction import *


def startup():
    answer = input('Is this your first time running "Academic Conclusions"?\n(y/n):').lower()
    default = input('Use default server login?\n(y/n): ').lower()
    if default[0] == 'n':
        zhost = input('PostgreSQL Host IP: ')
        zdatabase = input('PostgreSQL Database Name: ')
        zuser = input('Username: ')
        zpass = getpass.getpass('Password: ')
    else:
        zhost='localhost'
        zdatabase='cs350'
        zuser='student'
        zpass='student'
    print('Connecting . . .')
    
    try:
        con = psycopg2.connect(host=zhost, database=zdatabase, user=zuser, password=zpass)
        print('Connnected! Ready for use!')
    except psycopg2.Error as problem:
        print(problem)
        return False
    with con.cursor() as cur:
        if answer[0] == 'y':
            with open('tables.sql') as tables:
                cur.execute(tables.read())
                con.commit()
            with open('data.sql') as data_to_use:
                cur.execute(data_to_use.read())
                con.commit()
        
        elif answer[0] == 'n':      
            answer = input('New Game?\n(y/n): ').lower()
            if answer == 'y':
                with open('refresh.sql') as refresh:
                    cur.execute(refresh.read())
                    con.commit()
    return True



def maploop(currentmap):
    """(Mapp) -> None

    These function is used for running movement and actions on a generic
    Mapp object. The protag is stored in the global frame and is then
    used and mutated in relation to the Mapp object and the commands that
    are input by the user."""
    inmap = True
    while inmap and not protag.death:
        action = input('={}=> '.format(currentmap.name))
        action = action.lower().strip().split()
        with con.cursor() as cur:
            if len(action) > 1:
                action = [action[0], ' '.join(action[1:])]
            if len(action) < 1:
                print('')
            
            elif  action[0].lower() == 'quit':
                if input('Are you sure? (y/n): ').lower() == 'y':
                    return True
            
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
                # check to make sure item / room / door in question is in the area
                protag.examine(action[1])

            elif action[0] == 'enter' and len(action) > 1:
                # checks for any rooms in the area that might be enterable
                player.enter(action[1])

            elif action[0] == 'exit':
                print(">You're already outside!<\n")

            elif action[0] == 'look':
                protag.look()

            elif action[0] == 'ground':
                protag.ground()

            elif action[0] == 'pickup' and len(action) == 2:
                protag.pickup(action[1])

            elif action[0] == 'drop':
                protag.drop(action[1])
            
            elif action[0] == 'talk':
                # if user types wrong name somevar will help print a newline
                protag.talk(action)

            elif action[0] == 'take':
                # take requires a second marker called from. This requiers action
                # to be reconfigured
                if 'from' in action[1]:
                    action = ' '.join(action).split()
                    action = [action[0],
                            ' '.join(action[1:action.index('from')]),
                            ' '.join(action[action.index('from') + 1:])]
                    protag.take(action[1:])
            
            elif action[0] == 'help' and len(action) == 2:
                cur.execute("""SELECT name, syntax, description FROM help
                                WHERE name = %s""", [action[1]])
                info = cur.fetchall()
                for item in info:
                    print(info)
            
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
                    somevar += perf_counter()
                    if isinstance(item, NPC):
                        somevar -= 1
                        print('<>{}:\n{}'.format(item.name, item.talk(protag)))
                if somevar == len(currentroom.contents[0]):
                    print('')

        # elif action[0] == 'help' and len(action) == 2:
        #     print(helpcom(action[1]))
        
        else:
            print('Not a valid command, type help for help\n')



def main(protag, startingmap):
    protag.map = startingmap
    protag.pos = protag.map.start
    while protag.death != True:
        maploop(protag.map)

def score(protag):
    pass

if __name__ == '__main__':
    if input('Do you have PostgreSQL 9.4.1 installed?\n(y/n):').lower()[0] == 'y':    
        ready = startup()
        if ready:
            exit() #to be deleted
            # name = introduction()
            protag = Player(name, map0.start)
            main(protag, map0)
    else:
        print('Please install PostgreSQL 9.4.1 or later')
        print('http://www.postgresql.org/download/')