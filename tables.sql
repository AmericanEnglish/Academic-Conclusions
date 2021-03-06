-- The first two static tables
CREATE TABLE maps
(
    name VARCHAR(30),
    max_x INTEGER,
    max_y INTEGER,
    description VARCHAR,
    PRIMARY KEY (name)
);

CREATE TABLE warp_points
(
    from_map VARCHAR(30),
    to_map  VARCHAR(30),
    from_point INTEGER[],
    to_point INTEGER[],
    PRIMARY KEY (from_map, to_map),
    FOREIGN KEY (from_map)
        REFERENCES maps (name),
    FOREIGN KEY (to_map)
        REFERENCES maps (name)
);

CREATE TABLE worth
(
    name VARCHAR(20),
    value INTEGER,
    PRIMARY KEY (name)
);


-- Table of changing values
CREATE TABLE items
(
    id INTEGER,
    name VARCHAR(20),
    x INTEGER, -- If both x and y are NULL 
    y INTEGER, -- then item must be on the ground in a room
    map_name VARCHAR(30),
    worth_type VARCHAR(20),
    -- container_id INTEGER, -- If NULL then item is on ground
    description VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (worth_type)
        REFERENCES worth (name),
    -- FOREIGN KEY (container_id)
    --     REFERENCES containers (id),
    FOREIGN KEY (map_name)
        REFERENCES maps (name)
);


CREATE TABLE containers
( 
    id INTEGER,
    name VARCHAR(20),
    x INTEGER, -- If x, y are NULL then container is in a room
    y INTEGER, -- Noting that rooms can also be 'containers'
    map_name VARCHAR(30),
    parent_container_id INTEGER,
    description VARCHAR,
    unlock_item_id INTEGER,
    room_flag BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (unlock_item_id)
        REFERENCES items (id),
    FOREIGN KEY (parent_container_id)
        REFERENCES containers (id)
        ON UPDATE SET NULL,
    FOREIGN KEY (map_name)
        REFERENCES maps (name)
);


-- Alter table is required because of FK overlaps
ALTER TABLE items
	ADD container_id INTEGER;

ALTER TABLE items
	ADD CONSTRAINT container_must_exist
		FOREIGN KEY (container_id)
        	REFERENCES containers (id);


-- npcs are static and unchanging
CREATE TABLE npcs
(
    name VARCHAR(20),
    x INTEGER, -- If x, y are null then the npc is
    y INTEGER, -- in a room.
    map_name VARCHAR(20),
    room_id INTEGER,
    counter_value INTEGER,
    description VARCHAR,
    PRIMARY KEY (name),
    FOREIGN KEY (room_id)
        REFERENCES containers (id),
    FOREIGN KEY (map_name)
        REFERENCES maps (name)
);

CREATE TABLE npc_dialogue
(
    npc_name VARCHAR(20),
    counter INTEGER,
    dialogue VARCHAR,
    PRIMARY KEY (npc_name, counter),
    FOREIGN KEY (npc_name)
        REFERENCES npcs (name)
);

CREATE TABLE npc_conditionals
(
    npc_name VARCHAR(20),
    condition INTEGER,
    action VARCHAR, --This is a python command such as protag.give(thing)
    PRIMARY KEY (npc_name, action),
    FOREIGN KEY (npc_name)
        REFERENCES npcs (name)
);

-- Inventory tables
CREATE TABLE inventory
(
    name VARCHAR(20),-- If NULL then Player's item
    item_id INTEGER,
    backpack BOOLEAN,
    PRIMARY KEY (item_id),
    FOREIGN KEY (item_id)
        REFERENCES items (id),
    FOREIGN KEY (name)
        REFERENCES npcs(name)
);

CREATE TABLE help
(
    name VARCHAR(10),
    syntax VARCHAR(30),
    description VARCHAR,
    PRIMARY KEY (name)
);
