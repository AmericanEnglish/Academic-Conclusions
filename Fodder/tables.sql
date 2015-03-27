CREATE TABLE items
(
    id INTEGER NOT NULL,
    name VARCHAR(20),
    x INTEGER, -- If both x and y are NULL 
    y INTEGER, -- then item must be on the ground in a room
    map_name VARCHAR(20),
    container_id INTEGER, -- If NULL then item is on ground
    description VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (name)
        REFERENCES item_worth (name),
    FOREIGN KEY (container_id)
        REFERENCES containers (id),
    FOREIGN KEY (map_name)
        REFERENCES maps (name)
);

-- These tables will not be altered after initial insertion
CREATE TABLE containers
( 
    id INTEGER,
    name VARCHAR(20),
    x INTEGER, -- If x, y are NULL then container is in a room
    y INTEGER, -- Noting that rooms can also be 'containers'
    map_name VARCHAR(20),
    parent_container_id INTEGER,
    description VARCHAR,
    unlock_item_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (unlock_item_id)
        REFERENCES items (id),
    FOREIGN KEY (parent_container_id)
        REFERENCES containers (id)
        ON UPDATE SET NULL,
    FOREIGN KEY (map_name)
        REFERENCES maps (name)
);

CREATE TABLE npc_conditionals
(
    npc_name VARCHAR(20),
    condition VARCHAR,
    action VARCHAR, --This is a python command such as protag.give(thing)
    PRIMARY KEY (npc_name, condition),
    FOREIGN KEY (npc_name)
        REFERENCES npcs (name)
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

CREATE TABLE npcs
(
    name VARCHAR(20),
    x INTEGER, -- If x, y are null then the npc is
    y INTEGER, -- in a room.
    map_name VARCHAR(20),
    room_id INTEGER,
    description VARCHAR,
    PRIMARY KEY (name),
    FOREIGN KEY (room_id)
        REFERENCES containers (id),
    FOREIGN KEY (map_name)
        REFERENCES maps (name)
);

CREATE TABLE maps
(
    name VARCHAR(20),
    max_x INTEGER,
    max_y INTEGER,
    description VARCHAR,
    PRIMARY KEY (name)
);

CREATE TABLE item_worth
(
    name VARCHAR(20),
    value MONEY,
    PRIMARY KEY (name)
);

--DROP TABLE containers;
--DROP TABLE items;