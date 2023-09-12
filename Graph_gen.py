import networkx as nx
import random

def random_weighted_graph(num_nodes):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    weights = [random.uniform(0.0, 1.0) for _ in range(num_nodes)]

    for i in range(num_nodes):
        G.nodes[i]["lifetime"] = weights[i]

    for node1 in range(num_nodes):
        for node2 in range(node1 + 1, num_nodes):
            if random.choice([True, False]):
                G.add_edge(node1, node2)
    return G


def create_list_of_random_graphs(num_graphs, num_nodes):
    random_graphs = []
    for _ in range(num_graphs):
        random_graph = random_weighted_graph(num_nodes)
        random_graphs.append(random_graph)
    return random_graphs