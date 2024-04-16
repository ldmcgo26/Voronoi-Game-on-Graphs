from Graph import Graph
from Player import Player
import random as r

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
        self.controlled_vertices: dict[Player, list[int]] = {}

    #calculates each player's controlled vertices, maybe not necessary to do here? Maybe do in player class and pass the graph there as well?
    def calc_controlled_vertices(self):
        for player in self.players:
            controlled_vertices = set()
            for vertex in range(len(self.graph._dists)):
                closest_player = self._find_closest_player(vertex)
                if closest_player == player:
                    controlled_vertices.add(vertex)
            self.controlled_vertices[player] = list(controlled_vertices)

    def _find_closest_player(self, vertex: int) -> Player:
        min_distance = float('inf')
        closest_player = None
        for player in self.players:
            for facility in player.facilities:
                distance = self.graph._dists[vertex][facility]
                if distance < min_distance:
                    min_distance = distance
                    closest_player = player
        return closest_player

    #This should make an untaken vertex one of the player's facilities.
    #QUESTION: Should this check whether or not the vertex is not already controlled by another player?
    #Should this do anything else?
    def makeMove(self, vertex: int, playerIndex: int):
        self.players[playerIndex].add_facility(vertex)

    #randomly generate players with values assessments ranging from 1 to 5
    def gen_players(self, num_players, num_vertices):
        for i in range(num_players):
            values = {}
            for j in range(num_vertices):
                values[j] = r.randint(1,5)
            self.players.append(Player(values))
