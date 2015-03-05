--Player's Personal Items
CREATE TABLE inventory
(
    name VARCHAR(20),
    id INTEGER,
    PRIMARY KEY (name, id)
);

CREATE TABLE items
(
	name VARCHAR(20) NOT NULL,
	id INTEGER NOT NULL,
	x INTEGER,
	y INTEGER,
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
	PRIMARY KEY (id, locked),
	FOREIGN KEY (reqkey)
		REFERENCES items (id)
);

-- DROP TABLE inventory;
-- DROP TABLE items;
-- DROP TABLE containers;
