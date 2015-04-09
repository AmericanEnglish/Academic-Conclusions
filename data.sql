-- Maps first
INSERT INTO maps (name, max_x, max_y, description) VALUES
    ('Small Town', 0, 2, E'A small, unfriendly, town that doesnt see many travelers'),
    ('Graveyard', 2, 2, E'A massive graveyard, graves and mausoleums riddled with the bones and bodies. Graves amess and the smell of freshly unearthed dirt riddles the air. You cant help but wonder who would linger in such places.'),
    ('Mausoleum', 2, 2, E'Large enough to house what could be hundreds of bodies. The door appears unlocked and open. The smell of death, decay, and wallowing eminate from the insides. Proceed with caution.'),
    ('Mausoleum: 2nd Floor', 3, 3, E'The second floor of the dead. Who knows how deep this figurative dungeon may span.');

INSERT INTO warp_points (from_map, to_map, from_point, to_point) VALUES
    ('Small Town', 'Graveyard', '{0, 0}', '{2, 0}'),
    ('Graveyard', 'Small Town', '{2, 0}', '{0, 0}'),
    ('Graveyard', 'Mausoleum', '{1, 2}', '{1, 1}'),
    ('Mausoleum', 'Graveyard', '{1, 1}', '{1, 2}'),
    ('Mausoleum', 'Mausoleum: 2nd Floor', '{2, 2}', '{0, 0}'),
    ('Mausoleum: 2nd Floor', 'Mausoleum', '{0,0}', '{2,2}');

INSERT INTO worth (name, value) VALUES
    ('inhumane', -6),
    ('questionable', -4),
    ('tainted', -2),
    ('valueless', 0),
    ('bronze', 2),
    ('silver', 4),
    ('gold', 6),
    ('platinum', 10);

-- This is mainly things don't go into a container
INSERT INTO items (id, name, x, y, map_name, worth_type, container_id, description) VALUES
    (1, 'Skull Key', 0, 2, 'Graveyard', 'silver', NULL, E'The hilt of the key has a skull crafted in it, almost as if you shouldnt be where it leads.'),
    (100, 'Small Money Pouch', NULL, NULL, NULL, 'silver', NULL, E'A small pouch of silver coins. A sign of a hard days work.' ),
    (50, 'Teddy Bear', NULL, NULL, NULL, 'valueless', NULL, E'Small but worn. This teddy lasted someone a lot of years in good care or maybe a few years in constant use. Hard to tell.'),
    (13, 'Red Key', 2, 2, 'Mausoleum', 'tainted', NULL, E'A red key. Thats it.'),
    (75, 'Paper Note', NULL, NULL, NULL, 'inhumane', NULL, E'Dear mom, teddy said he wanted to play with the ghosts. Ill be back before dinner, honest! ~ Pookey');
-- Containers and Rooms
INSERT INTO containers (id, name, x, y, map_name, parent_container_id, description, unlock_item_id, room_flag) VALUES
    (1, 'Town Hall', 0, 2, 'Small Town', NULL, E'A rustic and acient hall constructed far before you were born',  NULL, TRUE),
    (2, 'Crypt', 0, 0, 'Graveyard', NULL, E'An old, dust covered, tomb, cold to the touth. The tomb forgives no one who dare to enter.', 1, TRUE),
    (3, 'Cracked Urn', NULL, NULL, NULL, 2, E'A dust filled urn. It yURNS to be investigated.', NULL, FALSE),
    (4, 'Unmarked Grave 302', 0, 1, 'Graveyard', NULL, E'This towns cemetary is full of more dead people than you thought. To make matters worse they dont even label the dead.', NULL, FALSE),
    (5, 'Rotting Chest', 0, 0, 'Mausoleum', NULL, E'Decaying like a biological hurricane this chest doesnt seem to have much else going for it. Even the false lock is in need of repair.', NULL, FALSE),
    (8, 'Red Room', 2, 1, 'Mausoleum', NULL, E'The door is red, it is safe to assume this place paints the drapes on the inside the same color, and the floor, and walls, you get the drift.', 13, TRUE),
    (9, 'Odd Room', 0, 1, 'Mausoleum: 2nd Floor', NULL, E'Something about, be it the circular door or whatever tacky interior may wait. This whole thing is just out of place in the mausoleum.', NULL, TRUE),
    (10, 'Dark Room', 2, 1, 'Mausoleum: 2nd Floor', NULL, E'The from your torch dims as you peer in on the room. The very evil that flows forth seems to draing the energy from the very light that illuminates it.', NULL, TRUE);

INSERT INTO items (id, name, x, y, map_name, worth_type, container_id, description) VALUES 
    (6, 'Ribbed Key', NULL, NULL, NULL, 'silver', 2, E'A strange, metal ribbed, key. This sort of thing would be used to open something you wanted to protect. Whether it be your family or your selfishness.'),
    (14, 'Decorative Necklace', NULL, NULL, NULL, 'tainted', 8, E'The necklacke has a picture of Queen Mary on it. Not the fun one. The bath in the blood of young girls one. Yours now you guess.'),
    (15, 'Flask', NULL, NULL, NULL, 'bronze', 8, E'An alcoholic flask with a horse etched into the side.'),
    (16, 'Slipper', NULL, NULL, NULL, 'gold', 8, E'A slipper made of a glass. Although there is only one, these are rare to find nevertheless.');

INSERT INTO containers (id, name, x, y, map_name, parent_container_id, description, unlock_item_id, room_flag) VALUES
    (6, 'Small Den', 0, 2, 'Mausoleum', NULL, E'A fork in a mausoleum? What could possible be in there? Something or someone important?', 6, TRUE),
    (7, 'Fresh Barrel', NULL, NULL, NULL, 6, E'This barrel appears to be the newest thing added to the collection of spiders and remnants that litter the area.', NULL, FALSE),
    (11, 'Ominious Room', 1, 3, 'Mausoleum: 2nd Floor', NULL, E'This should be it. An insanely creepy feeling of being watched. Just one chest lies in wait beyond the door it seems.', NULL, TRUE),
    (12, 'Colorful Chest', NULL, NULL, NULL, 11, E'A brightly colored chest. Its the peacock of chests. A showman amongst less chest rivals. Crafted by a holy being almost.', NULL, FALSE);


-- Anything that requires a container
INSERT INTO items (id, name, x, y, map_name, worth_type, container_id, description) VALUES
    (2, 'Skull', NULL, NULL, NULL, 'tainted', 3, E'A human skull, how often do you see one of these babies detached? Too. Frequently.'),
    (3, 'Hand', NULL, NULL, NULL, 'tainted', 3, E'Although dead for what might be centuries, you feel an essence lingering around it when you examine it.'),
    (4, 'Whiskers The Cat', NULL, NULL, NULL, 'platinum', 2, E'A small feline of meowing variety. He attempts to wriggle out of your hands. Find his owner quickly?'),
    (5, 'Human Skeleton', NULL, NULL, NULL, 'questionable', 4, E'Its, well it used to be, a full human skeleton. Complete with skull, legs, and those other bones too!'),
    (7, 'Small Deformed Skull', NULL, NULL, NULL, 'questionable', 7, E'This skull is small in stature and human in nature. Most likely is belonged to a child. It seems . . . fresher than the rest.'),
    (8, 'Small Legs', NULL, NULL, NULL, 'questionable', 7, E'Small human-like legs. They arent grey and blackened. These seem recently deposited.'),
    (9, 'Short Arms', NULL, NULL, NULL, 'questionable', 7, E'Arms. Small but definitely human. Maybe . . . Maybe dont touch them.'),
    (10, 'Dead Torso', NULL, NULL, NULL, 'questionable', 7, E'This is a human torso. Dead of course. Although not too dead. Dont stick around long enough to know the difference.'),
    (11, 'Gold Coins', NULL, NULL, NULL, 'silver', 6, E'A few gold coins. They have a nicer sheen to them. Legit? Probably.'),
    (12, 'Wooden Chisel', NULL, NULL, NULL, 'bronze', 6, E'Small but convient chisel. It might be worth something if you know the right person that is.'),
    (17, 'Gold Bracelet', NULL, NULL, NULL, 'gold', 9, E'A small gold chain that can fit the wrist of a small adult or perhaps a very large child.'),
    (18, 'Glass Orb', NULL, NULL, NULL, 'valueless', 12, E'An orb with a sand like swirl etched into the glass. When you shake it lights up subtly but dimly.');

-- For keys that go into containers
-- and etc
INSERT INTO npcs (name, x, y, map_name, room_id, counter_value, description) VALUES 
    ('Oracle Wyma', NULL, NULL, NULL, 1, 0, E'An old wisey man, who seems to project a sense of self-importance and dishonesty but he is still dressed like a priest'),
    ('Diana', 2, 1, 'Graveyard', NULL, 0, E'She seems upset. In a graveyard. So far: normal'),
    ('Old Man Jack', 1, 0, 'Graveyard', NULL, 0, E'A suspiciously old man. Not suspicious because hes old. He seems to be looking through the grass.' ),
    ('Lola', 1, 1, 'Mausoleum', NULL, 0, E'An elderly woman. her face appears to be convered in blemishes and what might be plague spots. Something just doesnt sit well about her.'),
    ('Lazlo', NULL, NULL, NULL, 10, 0, E'A young boy, hair desheveled. He looks a bit weird. Acts a bit weird. Hes obviously a local.');

INSERT INTO inventory (name, item_id, backpack) VALUES
    ('Diana', 100, FALSE),
    ('Lola', 50, FALSE),
    ('Lazlo', 75, FALSE);

INSERT INTO npc_conditionals (npc_name, condition, action) VALUES
    ('Oracle Wyma', 18, 'score()'),
    ('Diana', 75, 'give 100'),
    ('Lola', 4, 'give 50'),
    ('Lazlo', 50, 'give 75');

INSERT INTO npc_dialogue (npc_name, counter, dialogue) VALUES
    ('Oracle Wyma', 0, E'Hello there, you look familiar, do I know you? . . . Not much of a talker\nI see. Either way you look like you might need some help. Now on a normal\nday I might just give you some money and tell you to do it in the faith of\nthe lord but I have no time. Ill give you one hundred gold if you retrieve\nan item for me. I need a small glass-like key from the graveyard. Fetch it.'),
    ('Oracle Wyma', 1, E'Im a clergy I cant just go robbing graves! Im pretty sure its on the 3rd floor or something. Just grab it and hurry back, time is of the essence.'),
    ('Oracle Wyma', 2, E'Aaaaahh yes, this is the orb i was looking for! Thank you. Now take this\nbullion and never come back'),
    ('Diana', 0, E'Have you seen my son? He went into a crypt earlier to look for his teddy. He hasnt come back in a couple hours. I think something might have happened to him.'),
    ('Diana', 1, E'No matter what I need my son back, id give almost anything to hold him again.'),
    ('Diana', 2, E'OH THANK CTHULU YOU FOUND HIM. It seems hes scribbled his where abouts on here.'),
    ('Old Man Jack', 0, E'I saw a strange mass grave about 20 meters north of here. I wonder if the bodies have any liftable valuables . . . I MEAN GRANDPA NEEDS YOUR HELP SON! CANT FIND THE SHOES!'),
    ('Old Man Jack', 1, E'OH MY, WHERE COULD THOSE SNEAKY SUCKERS BE.'),
    ('Lola', 0, E'Have you seen my cat? I thought I saw him near a grave somewhere.'),
    ('Lola', 1, E'I thought he would come in here looking for shelter. I guess not.'),
    ('Lola', 2, E'ERHMAHGERD WHISKERS!!! If you ever run away again little guy, I WILL KILL you.'),
    ('Lazlo', 0, E'Have you seen my teddy? I set him down around here somewhere to play . . .'),
    ('Lazlo', 1, E'Oh gosh! You found him! Thanks! Could you tell me mommy Im in here and totes ok? Ill write a note.');

INSERT INTO help (name, syntax, description) VALUES 
    ('help', 'help *action*', E'Displays the functionality of an action command and the needed syntax for correct execution'),
    ('m', 'm *direction*', E'This function only works outside of rooms, typing this inside of a room will result in an invalid command. You can move North, East, South, and West.'),
    ('pack', 'pack', E'This action checks your backpack. Your backpack has no capacity'),
    ('me', 'me', E'This displays the contents of what your holding in your hands. NPCs wont check your pack but they can definitely spot what your holding'),
    ('put', 'put *item*', E'Puts an item into your backpack.'),
    ('pull', 'pull *item*', E'Pulls items from your pack.'),
    ('examine', 'examine *object*', E'Examines an item around you. If you lack the know about what is around you just use the [look] command. Example command for Note you cannot examine things that are on the ground or in your pack. Only containers, rooms, doors, and things on your person.'),
    ('enter',  'enter *place*', E'Enters a room or the next area/previous area. This command does not work when you are already in a room.'),
    ('exit', 'exit *place*', E'You exit a room. This command does not do anything while outside a room.'),
    ('look', 'look', E'Checks the room/area your for contents at eye level'),
    ('ground', 'ground', E'Checks the ground, after all it is dark! Seeing the ground without effort is not something everyone can do. You are part of everyone.'),
    ('pickup', 'pickup *item*', E'Pickups an item from the ground if you are carrying five or more items you will drop whatever you tried to pickup. You are no pack mule! Dont try to man handle everything.'),
    ('drop', 'drop *item*', E'Drops item from your person onto the ground.'),
    ('talk', 'talk [*NPC NAME*]', E'Talks to an NPC in the same area as you. **talk** will talk to all NPCs in the space where as [talk name] will only talk to that specific NPC. If you have an item that an NPC wants, they will forcibly take it from you. If you have something you value be weary of talking to all of them.'),
    ('take', 'take *item* from *container*', E'Take will take and item from a container inside a room and outside a room. Any other format will be considered wrong and invalid.');