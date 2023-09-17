import networkx as nx
import random

def random_weighted_graph(num_nodes, edge_probability):
    G = nx.fast_gnp_random_graph(num_nodes, edge_probability)

    weights = [random.uniform(0.0, 1.0) for _ in range(num_nodes)]

    for i in range(num_nodes):
        G.nodes[i]["lifetime"] = weights[i]

    return G

def create_list_of_random_graphs():
    random_graphs = []
    for i in range(1,11):
        random_graph = random_weighted_graph(10 * i, 0.3)
        random_graphs.append(random_graph)
        random_graph = random_weighted_graph(10 * i, 0.5)
        random_graphs.append(random_graph)
        random_graph = random_weighted_graph(10 * i, 0.7)
        random_graphs.append(random_graph)
    return random_graphs
