--Player's Personal Items
CREATE TABLE items
(
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    x INTEGER,
    y INTEGER,
    map INTEGER,
    description VARCHAR,
    -- value MONEY,
    PRIMARY KEY (id)
    FOREIGN KEY (name)
        REFERENCES item_worth (name)
);

CREATE TABLE containers
( 
    id INTEGER,
    locked BOOLEAN,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    keys_item_id INTEGER,
    map INTEGER, 
    PRIMARY KEY (id),
    FOREIGN KEY (keys_item_id)
        REFERENCES items (id)
);

CREATE TABLE npcconditionals
(
    npc_name VARCHAR(20),
    condition VARCHAR,
    action VARCHAR,
    PRIMARY KEY (npc_name, condition)
);

CREATE TABLE item_worth
(
    name VARCHAR(20)
    price MONEY
    PRIMARY KEY (name)
);
-- DROP TABLE items;
-- DROP TABLE containers;
