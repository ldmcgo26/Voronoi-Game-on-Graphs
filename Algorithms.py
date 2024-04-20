from PlayerAlgorithm import PlayerAlgorithm
from Graph import Graph
from Player import Player
import random as r
from Visualize import showGraph

num_players = 3
num_vertices = 15
edge_density = 0.4
num_rounds = 3

#random algorithm
def pick_random_facility(playerAlgorithm: PlayerAlgorithm) -> int:
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for player in playerAlgorithm.players:
        facility_vertices.update(player.facilities)

    available_vertices = all_vertices - facility_vertices
    return r.choice(list(available_vertices))

#picks maximum value vertex (it can under player's control already)
def pick_max_vertex(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for player in playerAlgorithm.players:
        facility_vertices.update(player.facilities)

    available_vertices = list(all_vertices - facility_vertices)
    max_value = 0
    max_vertex = None
    for vertex in available_vertices:
        if player.values[vertex] > max_value:
            max_value = player.values[vertex]
            max_vertex = vertex
    return max_vertex

#picks maximum value vertex that isn't already under player's control
def pick_max_uncontrolled(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices - set(playerAlgorithm.controlled_vertices[player]))

    max_value = 0
    max_vertex = None
    for vertex in available_vertices:
        if player.values[vertex] > max_value:
            max_value = player.values[vertex]
            max_vertex = vertex
    return max_vertex

#picks vertex that has the maximum total value between itself and all of its immediate neighbors
def pick_max_neighbors(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for player in playerAlgorithm.players:
        facility_vertices.update(player.facilities)
    available_vertices = all_vertices - facility_vertices
    
    max_total_value = float('-inf')
    max_vertex = None
    for vertex in available_vertices:
        total_value = player.values[vertex]
        for neighbor in playerAlgorithm.graph._adjVerts[vertex]:
            if neighbor in available_vertices:
                total_value += player.values[neighbor]
        if total_value > max_total_value:
            max_total_value = total_value
            max_vertex = vertex
    return max_vertex

#picks vertex that has maximum total value for all vertices within a certain distance of the facility
def pick_max_within_distance(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    pass

def greedy(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    pass

if __name__ == "__main__":

    g = Graph(num_vertices, edge_density)
    pa = PlayerAlgorithm(g)
    pa.gen_players(num_players, num_vertices)

    #holds the algorithm each player (index) will use 
    player_algs = []
    for i in range(num_players):
        player_algs.append('neighbors')

    #plays the game
    for i in range(num_rounds):
        for j in range(num_players):
            if player_algs[j] == 'random':
                next_facility = pick_random_facility(pa)
            elif player_algs[j] == 'max':
                next_facility = pick_max_vertex(pa, pa.players[j])
            elif player_algs[j] == 'uncontrolled max':
                next_facility = pick_max_uncontrolled(pa, pa.players[j])
            elif player_algs[j] == 'neighbors':
                next_facility = pick_max_neighbors(pa, pa.players[j])
            pa.makeMove(next_facility, j)
            pa.calc_controlled_vertices()
            showGraph(g, pa)

    #Calculates who owns every vertex and prints out each player's controlled vertices
    pa.calc_controlled_vertices()
    for i in (pa.controlled_vertices.values()):
        print(i)
    
    #Maybe calculate each players total value here? Go through each player's controlled vertices and count up their values
    for player in pa.players:
        player_total = 0
        for vertex in pa.controlled_vertices[player]:
            player_total += player.values[vertex]
        print(player_total)