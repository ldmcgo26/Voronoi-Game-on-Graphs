class Vertex:
    def __init__(self):
        self.edges = []

    def get_edge_to(self, vertex):
        for edge in self.edges:
            if edge.other(self) == vertex:
                return edge
        return None

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        return False

    def adjacent_vertices(self):
        out = []
        for cur_edge in self.edges:
            out.append(cur_edge.other(self))
        return out

    def incident_edges(self):
        return self.edges