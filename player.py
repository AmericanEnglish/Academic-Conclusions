class Player:
    """Creates the player"""
    def __init__():
        pass


class Backpack:
    """Creates a backpack"""
    def __init__(self):
        self.contents = []

    def pull(thing):
        """(str) -> Obj

        Checks if the item.name is in the pack and if it is then returns
        the Obj in question. Else returns None meaning item not present
        """

        for item in self.contents:
            if thing.lower() == item.name.lower():
                return item
        return None

    def put(thing):
        """(str) -> str

        Takes item off of player's person and put it into backpack
        """

        for item in Player.contents:
            if thing.lower() == item.name.lower():
                self.contents.append(item)
                del Player.contents[item]
                return '{} was put into the pack'.format(thing)
        return None

