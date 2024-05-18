from Graph import Graph
from Player import Player
import random as r
import numpy as np

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
                distance = float('inf')
                if facility:
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
            # Generate random values for the player
            values = np.random.random_sample(num_vertices)+.1
            # Calculate the total sum of the values
            total_sum = np.sum(values)
            # Scale the values to ensure the same total sum for each player
            values = values * (num_vertices * 3) / total_sum  # Adjust the multiplier as needed
            # Convert the NumPy array to a dictionary
            values_dict = {j: value for j, value in enumerate(values)}
            # Create a Player object with the random values
            self.players.append(Player(values_dict))

    #returns a dict the players mapped to their total value
    #run this after the game is over probably
    def calc_ranked_payoff(self) -> dict[Player, int]:
        payoff = {}
        self.calc_controlled_vertices()
        for player in self.players:
            player_total = 0
            for vertex in self.controlled_vertices[player]:
                player_total += player.values[vertex]
            payoff[player] = player_total
        keys = list(payoff.keys())
        values = list(payoff.values())
        sorted_value_index = np.argsort(values)[::-1]
        ranked_payoff = {keys[i]: values[i] for i in sorted_value_index}
        return ranked_payoff
