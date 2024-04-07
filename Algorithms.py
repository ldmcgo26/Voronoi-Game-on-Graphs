from PlayerAlgorithm import PlayerAlgorithm
from Graph import Graph
from Player import Player

if __name__ == "__main__":
    g = Graph(10)
    p1 = Player({0:1.0,1:1.0,2:1.0}, [])
    p2 = Player({0:1.0,1:1.0,2:1.0}, [])
    pa = PlayerAlgorithm(g, [p1,p2])
    pa.makeMove(1, p1)
    pa.makeMove(2, p2)
    pa.calc_controlled_vertices()
    print(pa.controlled_vertices[p1], pa.controlled_vertices[p2])
