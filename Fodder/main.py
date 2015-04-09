import psycopg2
import getpass
from player import *
from maps import *
from time import perf_counter

# from introduction import *


def startup():
    """(None) -> Bool

    This helps determine all the connection settings for the PostgreSQL
    server. If there are any errors FOR ANY REASON the startup function
    will drop the error message into the command line and return False
    preventing the game from continuing. Otherwise startup will connect
    to the server.

    Startup will then go through and insert all data if the user hasn't
    played before, or refresh the data if the user wants a new game.
    """
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
            with open('data.sql') as data_to_use:
                cur.execute(data_to_use.read())
        
        elif answer[0] == 'n':      
            answer = input('New Game?\n(y/n): ').lower()
            if answer == 'y':
                with open('refresh.sql') as refresh:
                    cur.execute(refresh.read())
    con.commit()
    return True, con



def maploop(protag, con):
    """(Mapp) -> None

    These function is used for running movement and actions on a generic
    Mapp object. The protag is stored in the global frame and is then
    used and mutated in relation to the Mapp object and the commands that
    are input by the user."""
    inmap = True
    while inmap and not protag.death and protag.room == None:
        action = input('={}=> '.format(protag.map))
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
                protag.move(action[1], cur)
            
            elif action[0] == 'pack':
                protag.pack_view(cur)
            
            elif action[0] == 'me':
                protag.person_view(cur)
            
            elif action[0] == 'put':
                protag.put(action[1], cur)
            
            elif action[0] == 'pull':
                protag.pull(action[1], cur)
            
            elif action[0] == 'examine' and len(action) == 2:
                # check to make sure item / room / door in question is in the area
                protag.examine(action[1], cur)

            elif action[0] == 'enter' and len(action) > 1:
                # Player can enter map or room
                protag.enter(action[1], cur)

            elif action[0] == 'exit':
                print("> Youre Already Outside! <")
                print()

            elif action[0] == 'look':
                protag.look(cur)

            elif action[0] == 'ground':
                protag.ground(cur)

            elif action[0] == 'pickup' and len(action) == 2:
                protag.pickup(action[1], cur)

            elif action[0] == 'drop' and len(action) == 2:
                protag.drop(action[1], cur)
            
            elif action[0] == 'talk':
                protag.talk(action[1], cur)

            elif action[0] == 'take':
                # take requires a second marker called from. This requiers action
                # to be reconfigured
                if 'from' in action[1]:
                    action = ' '.join(action).split()
                    action = [action[0],
                            ' '.join(action[1:action.index('from')]),
                            ' '.join(action[action.index('from') + 1:])]
                    protag.take(action[1:], cur)
                else:
                    print('Not a valid command, type help for help\n')
            
            elif action[0] == 'help' and len(action) == 2:
                help(action[1], cur)
            
            else:
                print('Not a valid command, type help for help\n')
            con.commit()


def roomloop(protag, con):
    """(Player, Room) -> None

    This function is used for a player's interaction with the room and its 
    contents. Although some 'action' words are the same the objects some
    interactions are not exactly the same."""
    with con.cursor() as cur:
        while protag.room != None and protag.death != True:
            action = input('={}=> '.format(protag.room[1]))
            action = action.lower().strip().split()
            if len(action) > 1:
                action = [action[0], ' '.join(action[1:])]
            
            if len(action) < 1:
                print('')

            elif action[0] == 'pack':
                protag.pack_view(cur)
            
            elif action[0] == 'me':
                protag.person_view(cur)
            
            elif action[0] == 'put':
                protag.put(action[1], cur)
            
            elif action[0] == 'pull':
                protag.pull(action[1], cur)
            
            elif action[0] == 'examine' and len(action) == 2:
                protag.room_examine(action[1], cur)
            
            elif action[0] == 'enter':
                print("> Youre Already In The {} <".format(protag.room[1]))
                print()
            
            elif action[0] == 'exit':
                print("> You Exit The {} <".format(protag.room[1]))
                print()
                protag.room = None

            elif action[0] == 'look':
                protag.room_look(cur)
            
            elif action[0] == 'ground':
                protag.room_ground(cur)

            elif action[0] == 'pickup':
                protag.room_pickup(action[1], cur)

            elif action[0] == 'drop':
                protag.room_drop(action[1], cur)
            
            elif action[0] == 'take':
                # take requires a second marker called from. This requiers action
                # to be reconfigured
                if 'from' in action[1]:
                    action = ' '.join(action).split()
                    action = [action[0],
                            ' '.join(action[1:action.index('from')]),
                            ' '.join(action[action.index('from') + 1:])]
                    protag.room_take(action[1:], cur)
            
            elif action[0] == 'talk':
                # if user types wrong name somevar will help print a newline
                protag.talk(action[1], cur)
            elif action[0] == 'help' and len(action) == 2:
                help(action[1], cur)
            
            else:
                print('Not a valid command, type help for help\n')



def main(protag, con):
    while protag.death != True:
        while protag.death != True and protag.room == None:    
            maploop(protag, con)
        while protag.death != True and protag.room != None:
            roomloop(protag, con)
    score(protag, con)

def score(protag, con):
    with con.cursor() as cur:
        cur.execute("""SELECT value FROM inventory
            INNER JOIN items ON items.id = inventory.item_id
            INNER JOIN worth ON worth.name = items.worth_type
            WHERE inventory.name IS NULL""")
        final = cur.fetchall()
        placeholder = 0
        if final != []:    
            for value in final:
                placeholder += value[0][0]
        print('Final Score: {}'.format(placeholder))


if __name__ == '__main__':
    # Temporary auto-drop and login for debug purposes
    #ready = startup()
    print('Forcing Data . . .')
    zhost='localhost'
    zdatabase='cs350'
    zuser='student'
    zpass='student'
    con = psycopg2.connect(host=zhost, database=zdatabase, user=zuser, password=zpass)
    with con.cursor() as cur:
        with open('erase.sql', 'r') as delete:
            cur.execute(delete.read())
        with open('tables.sql', 'r') as tables:
            cur.execute(tables.read())
        with open('data.sql', 'r') as data:
            cur.execute(data.read())
    ready = (True, con)
    print('Success!')
    if ready[0]:
        name = input('Name: ')
        protag = Player(name)
        main(protag, ready[1])
    else:
        print('Please install PostgreSQL 9.4.1 or later')
        print('http://www.postgresql.org/download/')