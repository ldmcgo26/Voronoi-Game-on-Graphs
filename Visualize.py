import igraph as ig
import matplotlib.pyplot as plt
from Graph import Graph
import math as m

def showGraph(g: Graph, facilities: list[int]):

    graph = ig.Graph(directed=False)

    # Add vertices
    num_vertices = len(g._edgeDists)
    graph.add_vertices(num_vertices)

    # Add edges with distances
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if g._edgeDists[i][j] < m.inf:
                graph.add_edge(i, j, weight=g._edgeDists[i][j])

    fig, ax = plt.subplots(figsize=(5,5))
    ig.plot(
        graph,
        target=ax,
        layout="circle", # print nodes in a circular layout
        vertex_size=30,
        vertex_color=["blue" if vertex.index in facilities else "red" for vertex in graph.vs],
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        edge_width=[.5],
        edge_color=["#7142cf"]
    )

    plt.show()