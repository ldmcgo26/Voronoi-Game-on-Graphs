if __name__ == "__main__":

    g = Graph(15, 0.2)
    print(g._dists)

    graph = ig.Graph(directed=False)

    # Add vertices
    num_vertices = len(g._dists)
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
        vertex_color=["steelblue"],
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        edge_width=[.5],
        edge_color=["#7142cf"]
    )

    plt.show()