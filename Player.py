class Player:

    def __init__(
            self, 
            values: dict[int, float]
        ):
        #maps vertices to values for this player
        self.values = values

        #list of ints referring to the vertices this player has facilities on
        self.facilities: list[int] = []

    def add_facility(self, vertex: int):
        self.facilities.append(vertex)