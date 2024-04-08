from PlayerAlgorithm import PlayerAlgorithm
from Graph import Graph
from Player import Player
import random as r

num_players = 3
num_vertices = 50
edge_density = 0.5
num_rounds = 3

#generate players with values assessments ranging from 1 to 5
def gen_players(num_players, num_vertices):
    players = []
    for i in range(num_players):
        values = {}
        for j in range(num_vertices):
            values[j] = r.randint(1,5)
        players.append(Player(values))
    return players

def pick_random_facility(playerAlgorithm: PlayerAlgorithm) -> int:
    all_vertices = set(range(len(playerAlgorithm.graph._dists)))
    facility_vertices = set()
    for player in playerAlgorithm.players:
        facility_vertices.update(player.facilities)

    available_vertices = all_vertices - facility_vertices
    return r.choice(list(available_vertices))

def pick_max_vertex(playerAlgorithm: PlayerAlgorithm) -> int:
    pass

def pick_max_uncontrolled(playerAlgorithm: PlayerAlgorithm) -> int:
    pass

if __name__ == "__main__":

    g = Graph(num_vertices, edge_density)
    players = gen_players(num_players, num_vertices)
    pa = PlayerAlgorithm(g, players)

    player_algs = []
    for i in range(num_players):
        player_algs.append('random')

    #Random Algorithm
    for i in range(num_rounds):
        for j in range(num_players):
            if player_algs[j] == 'random':
                next_facility = pick_random_facility(pa)
            elif player_algs[j] == 'max':
                next_facility = pick_max_vertex(pa)
            else:
                next_facility = pick_max_uncontrolled(pa)
            pa.makeMove(next_facility, players[j])

    pa.calc_controlled_vertices()
    
    for i in (pa.controlled_vertices.values()):
        print(i)