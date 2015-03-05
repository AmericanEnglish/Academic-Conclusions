--Player's Personal Items
CREATE TABLE inventory
(
    name VARCHAR(20),
    id INTEGER,
    x INTEGER,
    y INTEGER,
    PRIMARY KEY (name, id)
);

--DROP TABLE inventory