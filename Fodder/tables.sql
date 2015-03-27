CREATE TABLE items
(
    id INTEGER NOT NULL,
    name VARCHAR(20),
    x INTEGER, -- If both x and y are NULL 
    y INTEGER, -- then item must be on the ground in a room
    -- map INTEGER,
    container_id INTEGER, -- If NULL then item is on ground
    description VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (name)
        REFERENCES item_worth (name),
    FOREIGN KEY (container_id)
        REFERENCES containers (id)
);

-- These tables will not be altered after initial insertion
CREATE TABLE containers
( 
    id INTEGER,
    -- locked BOOLEAN,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    keys_item_id INTEGER,
    map INTEGER,
    type VARCHAR(20),
    description VARCHAR,
--    room_id INTEGER
    PRIMARY KEY (id),
    FOREIGN KEY (keys_item_id)
        REFERENCES items (id)
--  FOREIGN KEY (room_id)
--      REFERENCES containers (id)
);

CREATE TABLE npc_conditionals
(
    npc_name VARCHAR(20),
    condition VARCHAR,
    action VARCHAR, --This is a python command such as protag.give(thing)
    PRIMARY KEY (npc_name, condition)
);

CREATE TABLE npc_dialogue
(
    npc_name VARCHAR(20),
    counter INTEGER,
    dialogue VARCHAR
    PRIMARY KEY (npc_name, counter)
    FOREIGN KEY (npc_name)
        REFERENCES npcs (name)
);

CREATE TABLE npcs
(
    name VARCHAR(20),
    x INTEGER,
    y INTEGER,
    map VARCHAR(20),
    room_id VARCHAR(20),
    description VARCHAR,
    PRIMARY KEY (name)
    FOREIGN KEY (room_id)
        REFERENCES containers (id)
);

CREATE TABLE item_worth
(
    name VARCHAR(20)
    value MONEY
    PRIMARY KEY (name)
);

--DROP TABLE containers;
--DROP TABLE items;