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
        
        #list of the players, which gives us each players controlled vertices and their value assessments
        self.players = players
    
    #This should add an untaken vertex to one of the player's list of controlled vertices.
    #QUESTION: Should this check whether or not the vertex is not already controlled by another player?
    #Should this do anything else?
    def makeMove(self, vertex: int, player: Player):
        player.controlled_vertices.append(vertex)
    