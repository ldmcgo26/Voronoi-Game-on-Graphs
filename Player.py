class Player:

    def __init__(
            self, 
            values: dict[int, float] = {}, 
            controlled_vertices: list[int] = []
        ):
        #maps vertices to values for this player
        self.values = values

        #list of ints referring to the vertices this player controlls
        self.controlled_vertices = controlled_vertices
