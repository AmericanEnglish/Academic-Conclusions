# Official README

## Word of Warning
This is loosely adapted from the campaign **Academic Conclusions** from [Roll20.net](https://roll20.net) You as a random stranger are more than welcome to download and play this game. Be warned the code that is not inside the *Fodder* folder was source code written before my plans to use a database. There could be small trace errors that occur because I didn't have time to test absolutely everything. 

## Requirements
This program was coded in python3.4 and uses the following additional packages:
- [PostgreSQL 9.4.1](http://www.postgresql.org/)
- [psycopg2](http://initd.org/psycopg/)
    * This is used for executing PostgreSQL with Python3

## Progress
- Done
    * Base Program Written
    * All maploop functions written
    * All maploop functions, so far, are bugless
- To Do
    * Continue to condense main.py while slowly expanding player.py
    * Write all queries that will have room related information
    * Maps.py will be eliminated and all functionality moved to player.py
    * Finish the 'enter' function and in doing so finally tie maps to rooms.

## Finally . . .
To run the program simply:
```
$ python3.4 Academic-Conclusions/main.py
```

### In-game Information
Functions:
- help
    - help *action*
    - Displays the functionality of an action command and the needed syntax for correct execution
- m
    - m *direction*
    - This function only works outside of rooms, typing this inside of a room while \nresult in an invalid command. You can move North, East, South, and West.
- pack
    - pack
    - This action checks your backpack. Your backpack has no capacity
- me
    - This displays the contents of what your holding in your hands. NPCs won't check your pack but they can definitely spot what your holding
- put
    - put *item*
    - Puts an item into your backpack.
- pull
    - pull *item*
    - Pulls items from your pack.
- examine
    - examine *object*
    - Examines an item around you. If you lack the know about what is around you just use the [look] command. Example command for Note you cannot examine things that are on the ground or in your pack. Only containers, rooms, doors, and things on your person.
- enter
    - enter *place*
    - Enters a room or the next area/previous area. This command does not work when you are already in a room.
- exit
    - exit *place*
    - You exit a room. This command does not do anything while outside a room.
- look
    - look
    - Checks the room/area your for contents at eye level
- ground
    - ground
    - Checks the ground, after all it is dark! Seeing the ground without effort is not something everyone can do. You are part of everyone.
- pickup
    - pickup *item*
    - Pickups an item from the ground if you are carrying five or more items you will drop whatever you tried to pickup. You are no pack mule! Don't try to man handle everything. 
- drop
    - drop *item*
    - Drops item from your person onto the ground.
- talk
    - talk [*NPC NAME*]
    - Talks to an NPC in the same area as you. **talk** will talk to all NPCs in the space where as [talk name] will only talk to that specific NPC. If you have an item that an NPC wants, they will forcibly take it from you. If you have something you value be weary of talking to all of them.
- take
    - take *item* from *container*
    - Take will take and item from a container inside a room and outside a room. Any other format will be considered wrong and invalid.