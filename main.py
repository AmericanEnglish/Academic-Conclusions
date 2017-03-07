import sqlite3
from getpass import getpass
from player import *
from time import sleep
from platform import platform
import os
import logging

directions = {
    'north': {'x': 0, 'y': 1},
    'south': {'x': 0, 'y': -1},
    'east': {'x': 1, 'y': 0},
    'west': {'x': -1, 'y': 0}
    }

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
    try:
        con = sqlite3.connect(database="database.db")
        print('Connnected! Ready for use!')
    except sqlite3.Error as problem:
        print(problem)
        return False, None, False
    with con.cursor() as cur:
        try:
            cur.execute("""SELECT * FROM items""")
            cur.fetchall()
            print('Data Refreshed To Defaults!')
            with open('refresh.sql','r') as refresh:
                cur.execute(refresh.read())
            with open('data.sql','r') as data_to_use:
                cur.execute(data_to_use.read())
            skip = input('Skip Intro?\n(y/n):').lower()
            if len(skip) > 0 and skip[0] =='y':
                skip = True
            else:
                skip = False
        except sqlite3.Error:
            con.rollback()
            print('No Previous Data Detected!')
            print('Creating Tables & Data!')
            with open('tables.sql') as tables:
                cur.execute(tables.read())
            with open('data.sql') as data_to_use:
                cur.execute(data_to_use.read())
            print('Success!')
            skip = False
    con.commit()
    hos = platform()
    if 'windows' in hos.lower():
        os.system('cls')
    else:
        os.system('clear')
    return True, con, skip


def maploop(protag, con):
    """(Mapp) -> None

    These function is used for running movement and actions on a generic
    Mapp object. The protag is stored in the global frame and is then
    used and mutated in relation to the Mapp object and the commands that
    are input by the user."""
    while not protag.death:
        # Display Input
        if protag.room is not None:
            action = input("={}=> ".format(protag.room))
        else:
            action = input('={}=> '.format(protag.map))
        action = action.lower().strip().split()
        # Prescreen Action
        if len(action) > 1:
            action = [action[0], ' '.join(action[1:])]
        if len(action) < 1:
            print('Not a valid command, type help for help.')
        # Process Action
        elif action[0].lower() == 'quit':
            if input('Are you sure? (y/n): ').lower() == 'y':
                protag.kill()
        elif action[0] in directions: # done
            protag.move(action[0], directions)
        elif action[0] == 'pack': # done
            protag.pack_view()
        elif action[0] == 'me': # done
            protag.onhand()
        elif action[0] == 'put' and len(action) == 2: # done
            protag.put(action[1])
        elif action[0] == 'pull' and len(action) == 2: # done
            protag.pull(action[1])
        elif action[0] == 'examine': # done
            protag.examine(action)
        elif action[0] == 'enter' and len(action) > 1: # update for Mapp's
            # Player can enter map or room
            if protag.room is None:
                protag.enter(action[1])
            else:
                print('> Youre Already In {} <'.format(protag.room[1]))
        elif action[0] == 'exit': # done
            protag.exit()
        elif action[0] == 'look': # done
            protag.look()
        # elif action[0] == 'ground':
        #     if protag.room is None:
        #         protag.ground()
        #     else:
        #         protag.room_ground()
        elif action[0] == 'pickup' and len(action) == 2:
            if protag.room is None:
                protag.pickup(action[1])
            else:
                protag.room_pickup(action[1])
        elif action[0] == 'drop' and len(action) == 2:
            if protag.room is None:
                protag.drop(action[1])
            else:
                protag.room_drop(action[1])
        elif action[0] == 'talk' and len(action) == 2:
            protag.talk(action[1])
        elif action[0] == 'take' and len(action) > 1:
            # take requires a second marker called from. This requiers action
            # to be reconfigured
            if 'from' in action[1]:
                action = ' '.join(action).split()
                action = [action[0],
                        ' '.join(action[1:action.index('from')]),
                        ' '.join(action[action.index('from') + 1:])]
                if protag.room is None:
                    protag.take(action[1:])
                else:
                    protag.room_take(action[1:])
            else:
                print('Not a valid command, type help for help')
        elif action[0] == 'help' and len(action) == 2:
            help(action[1])
        elif action[0]== 'help':
            help('all')
        else:
            print('Not a valid command, type help for help\n')


def introduction():
    print()
    with open('intro', 'r') as intro:
        print(intro.readline().strip())
        for line in intro:
            sleep(1.5)
            print(line, end='')
    choice = None
    while choice.lower()[0] != 'y':
        name = input('Can you at least tell me your name before I go? ')
        choice = input("""*{}*\nAre you sure? (y/n): """.format(name))
        if len(choice) < 1:
            choice = None
    return name


def main(protag, con):
    while protag.death != True:
        while protag.death != True and protag.room == None:
            maploop(protag, con)
        while protag.death != True and protag.room != None:
            roomloop(protag, con)
    score(protag, con)


def score(protag, con):
    pass


if __name__ == '__main__':
    # Return as an actual tuple
    ready, connection, skip_intro = startup()
    if ready:
        if not skip_intro:
            name = introduction()
        else:
            name = input('Name: ').strip()
        protag = Player(name)
        try:
            logging.basicConfig(filename='error.txt', level=logging.DEBUG)
            logging.debug('Logged Message:')            
            main(protag, connection)
        except:
            logging.exception('Some error, who knows')
    else:
        print('Please install PostgreSQL 9.4.1 or later')
        print('http://www.postgresql.org/download/')
