class Player:

    def __init__(
            self, 
            values: dict[int, float] = {}, 
            facilities: list[int] = [],
        ):
        #maps vertices to values for this player
        self.values = values

        #list of ints referring to the vertices this player has facilities on
        self.facilities = facilities
