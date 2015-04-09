-- Maps first
INSERT INTO maps (name, max_x, max_y, description) VALUES
    ('Small Town', 0, 2, 'A small, unfriendly, town that doesnt see many travelers'),
    ('Graveyard', 2, 2, 'A massive graveyard, graves and mausoleums riddled with the bones and bodies. Graves amess and the smell of freshly unearthed dirt riddles the air. You cant help but wonder who would linger in such places.'),
    ('Mausoleum', 2, 2, 'Large enough to house what could be hundreds of bodies. The door appears unlocked and open. The smell of death, decay, and wallowing eminate from the insides. Proceed with caution.'),

INSERT INTO warp_points (from_map, to_map, from_point, to_point) VALUES
    ('Small Town', 'Graveyard', '{0, 0}', '{2, 0}'),
    ('Graveyard', 'Small Town', '{2, 0}', '{0, 0}'),
    ('Graveyard', 'Mausoleum', '{1, 2}', '{1, 1}'),
    ('Mausoleum', 'Graveyard', '{1, 1}', '{1, 2}'),

INSERT INTO worth (name, value) VALUES
    ('inhumane', -6.00),
    ('questionable', -4.00),
    ('tainted', -2.00),
    ('valueless', 0.00),
    ('bronze', 2.00),
    ('silver', 4.00),
    ('gold', 6.00),
    ('platinum', 10.00);

-- This is mainly things don't go into a container
INSERT INTO items VALUES (id, name, x, y, map_name, worth_type, container_id, description)
    (1, 'Skull Key', 0, 2, 'Graveyard', 'silver', NULL, 'The hilt of the key has a skull crafted in it, almost as if you shouldnt be where it leads.'),
    (100, 'Small Money Pouch', NULL, NULL, NULL, 'silver', 'A small pouch of silver coins. A sign of a hard days work.' ),
    (50, 'Teddy Bear', NULL, NULL, NULL, 'valueless', 'Small but worn. This teddy lasted someone a lot of years in good care or maybe a few years in constant use. Hard to tell.')
-- Containers and Rooms
INSERT INTO containers (id, name, x, y, map_name, parent_container_id, description, unlock_item_id, room_flag) VALUES
    (1, 'Town Hall', 0, 2, 'Small Town', NULL, 'A rustic and acient hall constructed far before you were born',  NULL, TRUE),
    (2, 'Crypt', 0, 0, 'Graveyard', NULL, 'An old, dust covered, tomb, cold to the touth. The tomb forgives no one who dare to enter.', 1, TRUE),
    (3, 'Cracked Urn', NULL, NULL, NULL, 2, 'A dust filled urn. It yURNS to be investigated.', NULL, FALSE),
    (4, 'Unmarked Grave 302', 0, 1, 'Graveyard', NULL, 'This towns cemetary is full of more dead people than you thought. To make matters worse they dont even label the dead.')
-- Anything that requires a container
INSERT INTO items (id, name, x, y, map_name, worth_type, container_id, description) VALUES
    (2, 'Skull', NULL, NULL, NULL, 'tainted', 3, 'A human skull, how often do you see one of these babies detached? Too. Frequently.'),
    (3, 'Hand', NULL, NULL, NULL, 'tainted', 3, 'Although dead for what might be centuries, you feel an essence lingering around it when you examine it.'),
    (4, 'Whiskers The Cat', NULL NULL, NULL, 'inhumane', 2, 'A small feline of meowing variety. He attempts to wriggle out of your hands. Find his owner quickly?'),
    (5, 'Human Skeleton', NULL NULL, NULL, 'questionable', 4, 'Its, well it used to be, a full human skeleton. Complete with skull, legs, and those other bones too!')


-- For keys that go into containers
-- and etc
INSERT INTO npcs (name, x, y, map_name, room_id, counter_value, description) VALUES 
    ('Oracle Wyma', NULL, NULL, NULL, 1, 0, 'An old wisey man, who seems to project a sense of self-importance and dishonesty but he is still dressed like a priest');
    ('Diana', 2, 1, 'Graveyard', NULL, 0, 'She seems upset. In a graveyard. So far: normal'),
    ('Old Man Jack', 1, 0, 'Graveyard', NULL, 0, 'A suspiciously old man. Not suspicious because hes old. He seems to be looking through the grass.' ),

INSERT INTO inventory (name, id, backpack) VALUES
    ('Diana', 100, FALSE)

INSERT INTO npc_conditionals (npc_name, condition, action) VALUES
    ('Oracle Wyma', 1, 'score()');
    ('Diana', 50, 'give 100')

INSERT INTO npc_dialogue (npc_name, counter, dialogue) VALUES
    ('Oracle Wyma', 0, 'Hello there, you look familiar, do I know you? . . . Not much of a talker\nI see. Either way you look like you might need some help. Now on a normal\nday I might just give you some money and tell you to do it in the faith of\nthe lord but I have no time. Ill give you one hundred gold if you retrieve\nan item for me. I need a small glass-like key from the graveyard. Fetch it.'),
    ('Oracle Wyma', 1, 'Im a clergy I cant just go robbing graves! Im pretty sure its on the 3rd floor or something. Just grab it and hurry back, time is of the essence.'),
    ('Oracle Wyma', 2, 'Aaaaahh yes, this is the orb i was looking for! Thank you. Now take this\nbullion and never come back'),
    ('Diana', 0, 'Have you seen my son? He went into a crypt earlier to look for his teddy. He hasnt come back in a couple hours. I think something might have happened to him.'),
    ('Diana', 1, 'No matter what I need my son back, id give almost anything to hold him again.'),
    ('Diana', 2, 'OH THANK CTHULU YOU FOUND HIM. It seems hes scribbled his where abouts on here.'),
    ('Old Man Jack', 0, 'I saw a strange mass grave about 20 meters north of here. I wonder if the bodies have any liftable valuables . . . I MEAN GRANDPA NEEDS YOUR HELP SON! CANT FIND THE SHOES!'),
    ('Old Man Jack', 1, 'OH MY, WHERE COULD THOSE SNEAKY SUCKERS BE.')
INSERT INTO help (name, syntax, description) VALUES 
    ('help', 'help *action*', 'Displays the functionality of an action command and the needed syntax for correct execution'),
    ('m', 'm *direction*', 'This function only works outside of rooms, typing this inside of a room will result in an invalid command. You can move North, East, South, and West.'),
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