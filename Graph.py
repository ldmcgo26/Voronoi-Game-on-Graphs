import random as r
import math as m


class Graph:

    def __init__(
        self,
        numInitVertices: int = 0,
        randomDensity: float = 0.5,
        edgeDistGen: "function" = lambda a, b: r._inst.uniform(1, 10),
    ):
        """Graph Class Constructor

        Initializes a Graph according to the given args.

        Args:
            numInitVertices (int, optional): The desired number of initial vertices. Defaults to 0.
            randomDensity (float, optional): The probability there exists an edge between any two vertices. Defaults to 0.5.
            edgeDistGen (function, optional): A function that specifies how to set distances of edges. Defaults to random floats between 1 and 10.
        """

        self._edgeDists: list[list[float]] = []
        """ 
        A matrix of the distances of the edge between any two vertices. 
        self._edgeDists[i][j] denotes the distance of the edge between vertices i and j. 
        Note that the distance will be 0 if they are the same vertex and m.inf (infinity) if they have no edge between them.
        """
        self._adjVerts: dict[int, set[int]] = {}
        """
        A Hashmap mapping vertices to the sets of vertices they are adjacent to.
        """
        self._numEdges: int = 0
        """
        A field for storing the number of edges.
        """
        self._dists: list[list[float]]
        """
        Records the actual distances between two vertices 
        (which may be quite less between the _edgeDist, especially in the case where they are connected but not adjacent)
        """

        for u in range(numInitVertices):
            self._edgeDists.append([])
            self._adjVerts[u] = set()
            for v in range(u):
                if r.random() < 1 - m.sqrt(1 - randomDensity):
                    self._edgeDists[u].append(edgeDistGen(u, v))
                    self._edgeDists[v].append(edgeDistGen(u, v))
                    self._adjVerts[u].add(v)
                    self._adjVerts[v].add(u)
                    self._numEdges += 1
                else:
                    self._edgeDists[u].append(m.inf)
                    self._edgeDists[v].append(m.inf)
            self._edgeDists[-1].append(0)

        self._calculateDists()

    def _calculateDists(self):
        self._dists = self._edgeDists.copy()
        for k in range(len(self._edgeDists)):
            for u in range(len(self._edgeDists)):
                for v in range(len(self._edgeDists)):
                    self._dists[u][v] = min(
                        self._dists[u][v], self._dists[u][k] + self._dists[k][v]
                    )
                    self._dists[v][u] = self._dists[u][v]

    # I just made this for testing purposes, probably not helpful
    def getDiameter(self) -> float:
        if not self._dists:
            self._calculateDists()

        return max(sum(self._dists, start=[]))


if __name__ == "__main__":
    g = Graph(4, 0.5)
    print(g._dists)
