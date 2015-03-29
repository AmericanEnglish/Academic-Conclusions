-- Maps first
INSERT INTO maps (name, max_x, max_y, description) VALUES
    ('Small Town', 2, 2, 'A rural town that sees few travelers');

INSERT INTO item_worth (name, value) VALUES
    ('Key', 20.00),
    ('Final Key', 100.00);

INSERT INTO containers (id, name, x, y, map_name, parent_container_id, description, unlock_item_id) VALUES
    (1, 'inventory', NULL, NULL, NULL, NULL, 'Your bare hands and pockets', NULL ),
    (2, 'backpack' , NULL, NULL, NULL, NULL, 'Your pack of many things'   , NULL),
    (300, 'Town Hall', 2, 2, 'Small Town', NULL, 'A rustic town hall that has seen better days', NULL);

INSERT INTO items (id, name, x, y, map_name, container_id, description) VALUES
    (1, 'Key'  ,    2,    2, 'Small Town', NULL, 'A plain metal key good for unlocking'),
    (2, 'Key', NULL, NULL, NULL,  300, 'A smaller plainer key' ),
    (3, 'Final Key', NULL, NULL, NULL, 2, 'The only key youll ever wear' );