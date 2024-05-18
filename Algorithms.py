from PlayerAlgorithm import PlayerAlgorithm
from Graph import Graph
from Player import Player
import random as r
import pandas as pd
from Visualize import showGraph
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np

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

    if (len(facility_vertices) == 0):
        return pick_max_vertex(playerAlgorithm, player)
    
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

#predictive algorithm assumes all other players are playing greedy alg
def predictive(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices)

    max_total_value = float('-inf')
    max_vertex = None

    for vertex in available_vertices:
        # Simulate the player picking this vertex
        player.add_facility(vertex)
        playerAlgorithm.calc_controlled_vertices()

        # Simulate the next player (assuming it's player 1 if current is player 0, and so on)
        next_player = playerAlgorithm.players[(playerAlgorithm.players.index(player) + 1) % len(playerAlgorithm.players)]
        next_move = greedy(playerAlgorithm, next_player)
        next_player.add_facility(next_move)
        playerAlgorithm.calc_controlled_vertices()

        # Calculate the total value for the current player after the next move
        total_value = sum(player.values[v] for v in playerAlgorithm.controlled_vertices[player])

        # Revert the simulated moves
        next_player.remove_facility(next_move)
        player.remove_facility(vertex)

        # Check if this is the best move
        if total_value > max_total_value:
            max_total_value = total_value
            max_vertex = vertex

    return max_vertex

#sabotage
def sabotage(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices)

    max_total_value = float('-inf')
    max_vertex = None

    for vertex in available_vertices:
        # Calculate the sabotage value
        sabotage_value = player.values[vertex]
        other_players_total = sum(p.values[vertex] for p in playerAlgorithm.players if p != player)
        sabotage_value += other_players_total / (len(playerAlgorithm.players) - 1)

        # Check if this is the best vertex to sabotage
        if sabotage_value > max_total_value:
            max_total_value = sabotage_value
            max_vertex = vertex

    return max_vertex

#adaptive: changes strategy based on the players current rank
def adaptive(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices)

    # Calculate the current score and rank of the player
    ranked_payoff = playerAlgorithm.calc_ranked_payoff()
    current_score = ranked_payoff[player]
    player_rank = list(ranked_payoff.keys()).index(player) + 1

    if (len(facility_vertices) == 0):
        return pick_max_vertex(playerAlgorithm, player)

    # Determine the strategy based on the player's rank
    if player_rank == 1:
        # Leading strategy: focus on consolidating control
        max_vertex = greedy(playerAlgorithm, player)
    else:
        # Trailing strategy: focus on disrupting the leading player
        leading_player = list(ranked_payoff.keys())[0]
        max_disruption_value = float('-inf')
        max_vertex = None
        for vertex in available_vertices:
            # Simulate picking this vertex
            player.add_facility(vertex)
            playerAlgorithm.calc_controlled_vertices()
            # Calculate the value for the player
            player_value = sum(player.values[v] for v in playerAlgorithm.controlled_vertices[player])
            # Calculate the disruption value for the leading player
            leading_value = sum(leading_player.values[v] for v in playerAlgorithm.controlled_vertices[leading_player])
            disruption_value = player_value - leading_value
            # Revert the move
            player.remove_facility(vertex)
            # Check if this is the best move
            if disruption_value > max_disruption_value:
                max_disruption_value = disruption_value
                max_vertex = vertex

    return max_vertex

def adaptive2(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices)

    max_total_value = float('-inf')
    max_vertex = None

    for vertex in available_vertices:
        # Calculate the gap between the next player's value of the vertex and their second most valued vertex value
        next_player = playerAlgorithm.players[(playerAlgorithm.players.index(player) + 1) % len(playerAlgorithm.players)]
        next_player_available_vertices = list(all_vertices - facility_vertices - set(playerAlgorithm.controlled_vertices[next_player]))
        next_player_values = [next_player.values[v] for v in next_player_available_vertices]
        next_player_values.sort(reverse=True)
        gap = next_player_values[0] - (next_player_values[1] if len(next_player_values) > 1 else 0)

        # Calculate the adjusted value for the current player
        adjusted_value = player.values[vertex] + gap

        # Update the maximum total value and the corresponding vertex if this vertex yields higher total value
        if adjusted_value > max_total_value:
            max_total_value = adjusted_value
            max_vertex = vertex

    return max_vertex

def McGoldrick(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices)

    max_total_value = float('-inf')
    max_vertex = None

    for vertex in available_vertices:
        # Simulate the player picking this vertex
        player.add_facility(vertex)
        playerAlgorithm.calc_controlled_vertices()

        curPlayerIdx = playerAlgorithm.players.index(player)
        movesToRevert = []
        for numTurn in range(len(playerAlgorithm.players)-1):
            nextPlayer = playerAlgorithm.players[(playerAlgorithm.players.index(player) + numTurn) % len(playerAlgorithm.players)]
            next_move = greedy(playerAlgorithm, nextPlayer)
            nextPlayer.add_facility(next_move)
            movesToRevert.append(next_move)
            playerAlgorithm.calc_controlled_vertices()

        # Calculate the total value for the current player after the next move
        total_value = sum(player.values[v] for v in playerAlgorithm.controlled_vertices[player])

        # Revert the simulated moves
        player.remove_facility(vertex)
        for numTurn in range(len(playerAlgorithm.players)-1):
            playerAlgorithm.players[(playerAlgorithm.players.index(player) + numTurn) % len(playerAlgorithm.players)].remove_facility(movesToRevert[numTurn])

        # Check if this is the best move
        if total_value > max_total_value:
            max_total_value = total_value
            max_vertex = vertex

    return max_vertex

def Bingham(playerAlgorithm: PlayerAlgorithm, player: Player) -> int:
    playerAlgorithm.calc_controlled_vertices()
    all_vertices = set(range(num_vertices))
    facility_vertices = set()
    for p in playerAlgorithm.players:
        facility_vertices.update(p.facilities)
    available_vertices = list(all_vertices - facility_vertices)

    x = 0.5
    y = 1/len(playerAlgorithm.players)

    # Calculate the current score and rank of the player
    ranked_payoff = playerAlgorithm.calc_ranked_payoff()
    player_rank = list(ranked_payoff.keys()).index(player) + 1
    
    if player_rank == 1:
        x = x/1.5
    
    newValues = player.values.copy()

    # Calculate the gap between the next player's value of the vertex and their second most valued vertex value
    next_player = playerAlgorithm.players[(playerAlgorithm.players.index(player) + 1) % len(playerAlgorithm.players)]
    next_player_available_vertices = list(all_vertices - facility_vertices)
    next_player_values = [next_player.values[v] for v in next_player_available_vertices]
    next_player_values_copy = next_player_values.copy()
    next_player_values.sort(reverse=True)
    gap = next_player_values[0] - (next_player_values[1] if len(next_player_values) > 1 else 0)
    next_player_max_index = next_player_values_copy.index(next_player_values[0])
    newValues[next_player_max_index] = newValues[next_player_max_index] + gap*y


    for vertex in available_vertices:
        maxValue = 0
        for v in available_vertices:
            if player.values[v] > maxValue:
                maxValue = player.values[v]
        minValue = float('inf')
        for v in available_vertices:
            if player.values[v] < minValue:
                minValue = player.values[v]

        if player.values[vertex] > (maxValue - minValue)*x:
            other_players_total = sum(p.values[vertex] for p in playerAlgorithm.players if p != player)
            newValues[vertex] = newValues[vertex] + other_players_total*y

            avgEdgeWt = playerAlgorithm.graph.get_average_edge_length()
            newValues[vertex] = newValues[vertex] - (avgEdgeWt / (len(available_vertices)/(len(facility_vertices)/len(playerAlgorithm.players))))

    oldValues = player.values
    player.values = newValues
    move = pick_max_vertex(playerAlgorithm, player)
    player.values = oldValues
    return move

    


if __name__ == "__main__":
    #list of possible algorithms
    algs = ['random', 'max', 'uncontrolled max', 'neighbors', 'greedy', 'predictive', 'sabotage', 'adaptive', 'adaptive2']
    #CSV
    results = [['Player #', '# Rounds', '# Vertices', '# Players', 'Edge Density', 'Algorithm', 'Ranking', 'Score', '# Controlled Vertices']]

    # for z in range(100):
    num_players = 5
    num_vertices = 100
    edge_density = .3
    num_rounds = 5
    # num_players = r.randint(2, 6)
    # num_vertices = r.randint(50, 100)
    # edge_density = r.random()/2
    # num_rounds = r.randint(2,5)

    g = Graph(num_vertices, edge_density)
    pa = PlayerAlgorithm(g, players=[])
    pa.gen_players(num_players, num_vertices)

    #holds the algorithm each player (index) will use 
    # player_algs = []
    # for i in range(num_players):
    #     player_algs.append(r.choice(algs))
    player_algs = ['adaptive', 'McGoldrick', 'adaptive2', 'greedy', 'greedy']

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
            elif player_algs[j] == 'predictive':
                next_facility = predictive(pa, pa.players[j])
            elif player_algs[j] == 'sabotage':
                next_facility = sabotage(pa, pa.players[j])
            elif player_algs[j] == 'adaptive':
                next_facility = adaptive(pa, pa.players[j])
            elif player_algs[j] == 'adaptive2':
                next_facility = adaptive2(pa, pa.players[j])
            elif player_algs[j] == 'McGoldrick':
                next_facility = McGoldrick(pa, pa.players[j])
            elif player_algs[j] == 'Bingham':
                next_facility = Bingham(pa, pa.players[j])
            elif player_algs[j] == 'player':
                next_facility = int(input('Pick your next facility: '))-1
            pa.makeMove(next_facility, j)
            pa.calc_controlled_vertices()
            # visualize the graph
            # showGraph(g, pa)

    #Calculates who owns every vertex and prints out each player's controlled vertices
    # pa.calc_controlled_vertices()
    # for i in (pa.controlled_vertices.values()):
    #     print(i)
    
    ranked_payoff = pa.calc_ranked_payoff()
    for player, score in ranked_payoff.items():
        print(f"Player {pa.players.index(player)+1}: {round(score*10)}") 
    
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

