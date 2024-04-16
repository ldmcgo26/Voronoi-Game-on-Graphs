from flask import Flask, render_template, jsonify
from Graph import Graph
from PlayerAlgorithm import PlayerAlgorithm
from Visualize import showGraph

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph_data')
def get_graph_data():
    # Create your graph and player algorithm objects
    g = Graph(5)
    pa = PlayerAlgorithm(graph=g)
    pa.gen_players(2, 5)
    graph = showGraph(g, pa)

    print(graph.vs.attributes)
    # Export graph data as JSON
    graph_data = {
        'nodes': graph.vs[graph],  # Define a method in Graph class to get nodes
        'edges': graph.es[graph],  # Define a method in Graph class to get edges
        # Include any additional attributes needed for visualization
    }
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True)
