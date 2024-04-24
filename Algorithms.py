from PlayerAlgorithm import PlayerAlgorithm
from Graph import Graph
from Player import Player
import random as r
import pandas as pd
from Visualize import showGraph

num_players = 5
num_vertices = 200
edge_density = 0.05
num_rounds = 4

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
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)

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

#picks vertex that has the maximum total value between itself and all of its immediate neighbors (can already be under that player's control)
def pick_max_neighbors(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
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

#greedy, picks the vertex that increases the player's value the most
#total value gained = that new vertex and all new vertices controlled by that facility that weren't already
def greedy(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices - set(playerAlgorithm.controlled_vertices[player]))
    
    max_total_value = float('-inf')
    max_vertex = None
    
    for vertex in available_vertices:
        player.add_facility(vertex)
        playerAlgorithm.calc_controlled_vertices()
        total_value = 0
        for v in playerAlgorithm.controlled_vertices[player]:
            total_value += player.values[v]
        if total_value > max_total_value:
            max_total_value = total_value
            max_vertex = vertex
        player.remove_facility(vertex)
                
    return max_vertex

#predictive algorithm
def predictive(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    pass

if __name__ == "__main__":
    #list of possible algorithms
    algs = ['random', 'max', 'uncontrolled max', 'neighbors', 'greedy']
    #CSV
    results = [['Player #', '# Rounds', '# Vertices', '# Players', 'Edge Density', 'Algorithm', 'Ranking', 'Score', '# Controlled Vertices']]

    for z in range(100):
        num_players = r.randint(2, 6)
        num_vertices = r.randint(50, 250)
        edge_density = r.random()/2
        num_rounds = r.randint(2,5)

        g = Graph(num_vertices, edge_density)
        pa = PlayerAlgorithm(g, players=[])
        pa.gen_players(num_players, num_vertices)

        #holds the algorithm each player (index) will use 
        player_algs = []
        for i in range(num_players):
            player_algs.append(r.choice(algs))

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
                elif player_algs[j] == 'greedy':
                    next_facility = greedy(pa, pa.players[j])
                pa.makeMove(next_facility, j)
                # pa.calc_controlled_vertices()
                #visualize the graph
                # showGraph(g, pa)

        #Calculates who owns every vertex and prints out each player's controlled vertices
        # pa.calc_controlled_vertices()
        # for i in (pa.controlled_vertices.values()):
        #     print(i)
        
        ranked_payoff = pa.calc_ranked_payoff()
        # print(ranked_payoff)
        
        for p in range(num_players):
            toAppend = []
            #Player #, # Rounds, # Vertices, # Players, # Edge Density
            toAppend.append(p+1)
            toAppend.append(num_rounds)
            toAppend.append(num_vertices)
            toAppend.append(num_players)
            toAppend.append(edge_density)
            #this player's algorithm
            toAppend.append(player_algs[p])
            #this player's ranking
            toAppend.append(list(ranked_payoff.keys()).index(pa.players[p]) + 1)
            #this player's score
            toAppend.append(ranked_payoff[pa.players[p]])
            #this player's # controlled vertices
            toAppend.append(len(pa.controlled_vertices[pa.players[p]]))

            results.append(toAppend)

    # File path for CSV output
    csv_file_path = "output.csv"

    # Create a DataFrame from the data
    df = pd.DataFrame(results)

    # Write DataFrame to CSV file
    df.to_csv(csv_file_path, index=False, header=False)

