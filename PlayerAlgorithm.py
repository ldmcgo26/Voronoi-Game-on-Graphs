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

        #maps players to their controlled vertices (includes their facilities and all vertices closest to their facilities)
        self.controlled_vertices: dict[Player, list[int]]

    #calculates each player's controlled vertices, maybe not necessary to do here? Maybe do in player class and pass the graph there as well?
    def calc_controlled_vertices():
        pass
    
    #This should make an untaken vertex one of the player's facilities.
    #QUESTION: Should this check whether or not the vertex is not already controlled by another player?
    #Should this do anything else?
    def makeMove(self, vertex: int, player: Player):
        player.facilities.append(vertex)
    