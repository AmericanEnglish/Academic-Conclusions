-- Maps first
INSERT INTO maps (name, max_x, max_y, description) VALUES;

INSERT INTO item_worth (name, value) VALUES;

INSERT INTO containers (id, name, x, y, map_name, parent_container_id, description, unlock_item_id, room_flag) VALUES;

INSERT INTO items (id, name, x, y, map_name, worth_ty[e, container_id, description) VALUES
    (1, 'Key' ,  2,    2, 'Small Town', NULL, 'A plain metal key good for unlocking'),
    (2, 'Key', NULL, NULL, NULL,  300, 'A smaller plainer key' ),
    (3, 'Final Key', NULL, NULL, NULL, 2, 'The only key youll ever wear' );



INSERT INTO help (name, syntax, description) VALUES 
    ('help', 'help *action*', 'Displays the functionality of an action command and the needed syntax for correct execution'),
    ('m', 'm *direction*', 'This function only works outside of rooms, typing this inside of a room while \nresult in an invalid command. You can move North, East, South, and West.'),
    ('pack', 'pack', 'This action checks your backpack. Your backpack has no capacity'),
    ('me', 'me', 'This displays the contents of what your holding in your hands. NPCs wont check your pack but they can definitely spot what your holding'),
    ('put', 'put *item*', 'Puts an item into your backpack.'),
    ('pull', 'pull *item*', 'Pulls items from your pack.'),
    ('examine', 'examine *object*', 'Examines an item around you. If you lack the know about what is around you just use the [look] command. Example command for Note you cannot examine things that are on the ground or in your pack. Only containers, rooms, doors, and things on your person.'),
    ('enter',  'enter *place*', 'Enters a room or the next area/previous area. This command does not work when you are already in a room.'),
    ('exit', 'exit *place*', 'You exit a room. This command does not do anything while outside a room.'),
    ('look', 'look', 'Checks the room/area your for contents at eye level'),
    ('ground', 'ground', 'Checks the ground, after all it is dark! Seeing the ground without effort is not something everyone can do. You are part of everyone.'),
    ('pickup', 'pickup *item*', 'Pickups an item from the ground if you are carrying five or more items you will drop whatever you tried to pickup. You are no pack mule! Dont try to man handle everything.'),
    ('drop', 'drop *item*', 'Drops item from your person onto the ground.'),
    ('talk', 'talk [*NPC NAME*]', 'Talks to an NPC in the same area as you. **talk** will talk to all NPCs in the space where as [talk name] will only talk to that specific NPC. If you have an item that an NPC wants, they will forcibly take it from you. If you have something you value be weary of talking to all of them.'),
    ('take', 'take *item* from *container*', 'Take will take and item from a container inside a room and outside a room. Any other format will be considered wrong and invalid.');