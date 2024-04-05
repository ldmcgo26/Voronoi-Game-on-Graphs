from Graph import Graph
from Player import Player

class PlayerAlgorithm:

    def __init__(
            self,
            graph: Graph = Graph(),
            players: list[Player] = []
        ):
        #the graph
        self.graph = graph
        
        #list of the players
        self.players = players
    
    def makeMove(self, ):
        pass