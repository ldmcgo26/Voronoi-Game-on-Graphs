import igraph as ig
import matplotlib.pyplot as plt
from Graph import Graph
from PlayerAlgorithm import PlayerAlgorithm
import math as m

def showGraph(g: Graph, pa: PlayerAlgorithm):

    graph = ig.Graph(directed=False)

    # Add vertices
    num_vertices = len(g._edgeDists)
    graph.add_vertices(num_vertices)

    # Add edges with distances
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if g._edgeDists[i][j] < m.inf:
                graph.add_edge(i, j, weight=g._edgeDists[i][j])

    #Assigns each vertex a color
    colors = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"]
    colors_opaque = [color + '50' for color in colors]
    vertex_color = []
    for vertex in graph.vs:
        colored = False
        for i, player in enumerate(pa.players):
            if vertex.index in player.facilities:
                vertex_color.append(colors[i])  # Use the original color for facilities
                colored = True
                break
            elif player in pa.controlled_vertices and vertex.index in pa.controlled_vertices[player]:
                vertex_color.append(colors_opaque[i])  # Use the opaque color for controlled vertices
                colored = True
                break
        if not colored:
            vertex_color.append('gray')  # Default color for other vertices



    #PLOT IT
    fig, ax = plt.subplots(figsize=(12,7.5))
    ig.plot(
        graph,
        target=ax,
        layout="kamada_kawai", # print nodes in a circular layout
        vertex_size=55,
        vertex_color=vertex_color,
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        vertex_label=[i+1 for i in range(len(g._edgeDists))],
        edge_label=[round(g._edgeDists[i][j], 2) for i in range(len(g._edgeDists)) for j in range(i, len(g._edgeDists[0])) if g._edgeDists[i][j] < m.inf and i!=j],
        edge_width=[1],
        edge_color=["#7142cf"]
    )

    plt.show()