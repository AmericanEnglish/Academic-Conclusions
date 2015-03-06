--Player's Personal Items
CREATE TABLE inventory
(
    name VARCHAR(20),
    id INTEGER,
    PRIMARY KEY (name, id)
);

CREATE TABLE pack
(
	name VARCHAR(20)
	id INTEGER,
	PRIMARY KEY (name, id)
);

CREATE TABLE items
(
	name VARCHAR(20) NOT NULL,
	id INTEGER NOT NULL,
	x INTEGER,
	y INTEGER,
	map INTEGER,
	value MONEY,
	PRIMARY KEY (name, id),
	UNIQUE (id)
);

CREATE TABLE containers
( 
	id INTEGER,
	locked BOOLEAN,
	x INTEGER NOT NULL,
	y INTEGER NOT NULL,
	reqkey INTEGER,
	map INTEGER, 
	PRIMARY KEY (id, locked),
	FOREIGN KEY (reqkey)
		REFERENCES items (id)
);

CREATE TABLE rooms
(
	map INTEGER,
	PRIMARY KEY (map)
);

CREATE TABLE npc
(
	name VARCHAR(20)
	PRIMARY KEY (name)
);

CREATE TABLE ground
(
	filler BOOLEAN,
);
-- DROP TABLE inventory;
-- DROP TABLE pack;
-- DROP TABLE items;
-- DROP TABLE containers;
