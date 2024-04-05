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

        #list of ints referring to the vertices this player controls
        #this includes all the vertices it has as facilities on and all the vertices
        #that are closer to one of this players facilities than any other. 
        self.controlled_vertices: list[int] = []

        #set the controlled vertices
        

    def calc_total_value(self):
        total = 0
        for i in self.controlled_vertices:
            total += self.values[i]
        return total
