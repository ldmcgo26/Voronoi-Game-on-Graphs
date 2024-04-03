class Edge:
    def __init__(self, u, v, distance):
        self.distance = distance
        self.v1 = u
        self.v2 = v

    def distance(self):
        return self.distance

    def other(self, vertex):
        if vertex == self.v1:
            return self.v2
        elif vertex == self.v2:
            return self.v1
        return None

    def vertices(self):
        return [self.v1, self.v2]
