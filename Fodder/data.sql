-- Maps first
INSERT INTO maps (name, max_x, max_y, description) VALUES
    ('Small Town', 0, 2, 'A small, unfriendly, town that doesnt see many travelers');

INSERT INTO worth (name, value) VALUES
    ('inhumane', -6.00),
    ('questionable', -4.00),
    ('tainted', -2.00),
    ('valueless', 0.00),
    ('bronze', 2.00),
    ('silver', 4.00),
    ('gold', 6.00),
    ('platinum', 10.00);

INSERT INTO containers (id, name, x, y, map_name, parent_container_id, description, unlock_item_id, room_flag) VALUES
    (200, 'Town Hall', 0, 2, 'Small Town', NULL, 'A rustic and acient hall constructed far before you were born',  NULL, TRUE);

INSERT INTO items (id, name, x, y, map_name, worth_type, container_id, description) VALUES
    (1, 'Small Trinket', 0, 0, 'Small Town', 'bronze', NULL, 'A small smooth stone, you found in your pocket just a moment ago'),
    (2, 'Pineapple', NULL, NULL, NULL, 'silver', 200, 'Its a Pineapple . . .');

INSERT INTO npcs (name, x, y, map_name, room_id, counter_value, description) VALUES 
    ('Oracle Wyma', NULL, NULL, NULL, 200, 0, 'An old wisey man, who seems to project a sense of self-importance and dishonesty but he is still dressed like a priest');

INSERT INTO npc_conditionals (npc_name, condition, action) VALUES
    ('Oracle Wyma', 'player.has(1)', 'score()');

INSERT INTO npc_dialogue (npc_name, counter, dialogue) VALUES
    ('Oracle Wyma', 0, 'Hello there, you look familiar, do I know you? . . . Not much a talker\nI see. Either way you look like you might need some help. Now on a normal\nday I might just give you some money and tell you to do it in the faith of\nthe lord but I have no time. Ill give you one hundred gold if you retrieve\nan item for me. I need a small glass-like key from the graveyard. Fetch it.'),
    ('Oracle Wyma', 1, 'Im a clergy I cant just go robbing graves! Im pretty sure its on the 3rd\nfloor or something. Just grab it and hurry back, time is of the essence.'),
    ('Oracle Wyma', 2, 'Aaaaahh yes, this is the orb i was looking for! Thank you. Now take this\nbullion and never come back');

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