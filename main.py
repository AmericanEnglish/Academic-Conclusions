import sqlite3
from getpass import getpass
from player import *
from time import sleep
from platform import platform
import os
import logging

directions = {
                    'north': (0,1),
                    'south':(0,-1), 
                    'east':(1, 0), 
                    'west':(-1, 0)
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
        action = input('={}=> '.format(protag.map))
        action = action.lower().strip().split()
        with con.cursor() as cur:
            if len(action) > 1:
                action = [action[0], ' '.join(action[1:])]
            if len(action) < 1:
                print('Not a valid command, type help for help.')
                print()
            
            elif  action[0].lower() == 'quit':
                if input('Are you sure? (y/n): ').lower() == 'y':
                    protag.death = True
            
            elif action[0] in directions:
                if protag.room == None:
                    protag.move(action[0], cur)
                    protag.look(cur)
                    protag.ground(cur)
                else: 
                    print('> You Are In A Room & Cannot Move <')
                    print()

            elif action[0] == 'pack':
                protag.pack_view(cur)
            
            elif action[0] == 'me':
                protag.person_view(cur)
            
            elif action[0] == 'put'  and len(action) == 2:
                protag.put(action[1], cur)
            
            elif action[0] == 'pull' and len(action) == 2:
                protag.pull(action[1], cur)
            
            elif action[0] == 'examine' and len(action) == 2:
                # check to make sure item / room / door in question is in the area
                if protag.room == None:
                    protag.examine(action[1], cur)
                else:
                    protag.room_examine(action[1], cur)

            elif action[0] == 'enter' and len(action) > 1:
                # Player can enter map or room
                if protag.room == None:
                    protag.enter(action[1], cur)
                else:
                    print('> Youre Already In {} <'.format(protag.room[1]))
                    print()

            elif action[0] == 'exit':
                if protag.room == None:
                    print("> Youre Already Outside! <")
                    print()
                else:
                    protag.room == None
                    print('> You Exit The {} <'.format(protag.room[1]))
                    print()

            elif action[0] == 'look':
                if protag.room == None:
                    protag.look(cur)
                    protag.ground(cur)
                else:
                    protag.room_look(cur)
                    protag.room_ground(cur)

            elif action[0] == 'ground':
                if protag.room == None:
                    protag.ground(cur)
                else:
                    protag.room_ground(cur)

            elif action[0] == 'pickup' and len(action) == 2:
                if protag.room == None:
                    protag.pickup(action[1], cur)
                else:
                    protag.room_pickup(action[1], cur)

            elif action[0] == 'drop' and len(action) == 2:
                if protag.room == None:
                    protag.drop(action[1], cur)
                else:
                    protag.room_drop(action[1], cur)

            elif action[0] == 'talk' and len(action) == 2:
                protag.talk(action[1], cur)

            elif action[0] == 'take' and len(take) > 1:
                # take requires a second marker called from. This requiers action
                # to be reconfigured
                if 'from' in action[1]:
                    action = ' '.join(action).split()
                    action = [action[0],
                            ' '.join(action[1:action.index('from')]),
                            ' '.join(action[action.index('from') + 1:])]
                    if protag.room == None:
                        protag.take(action[1:], cur)
                    else:
                        protag.room_take(action[1:], cur)
                else:
                    print('Not a valid command, type help for help\n')
            
            elif action[0] == 'help' and len(action) == 2:
                help(action[1], cur)
            
            elif action[0]== 'help':
                help('all', cur)
            
            else:
                print('Not a valid command, type help for help\n')
            con.commit()


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
