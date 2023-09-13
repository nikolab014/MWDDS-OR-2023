import networkx as nx
import numpy as np
from Graph_gen import random_weighted_graph

def whitescore(G, v, colors):
    score = 0
    if not colors[v]:
        score += 1
    for x in G.neighbors(v):
        if not colors[x]:
            score += 1
    score *= G.nodes[v]["lifetime"]
    return score
def objective_function(D, G):
    total_weight = 0
    for dominating_set in D:
        min_lifetime = min(G.nodes[v]["lifetime"] for v in dominating_set)
        total_weight += min_lifetime
    return total_weight
def ghmwdds(G):
    D = []
    Vrem = set(G.nodes)
    Vdone = set()
    while True:
        for node in G.nodes:
            nhd = set(G.neighbors(node))
            nhd.add(node)
            if nhd.issubset(Vdone):
                return D
        # 0-white 1-grey 2-black
        colors = np.zeros(G.order(), dtype=np.int8)
        Dk = set()
        while not nx.is_dominating_set(G, Dk):
            candidates = [x for x in Vrem if colors[x] != 2]
            scores = np.array([whitescore(G, x, colors) for x in candidates])
            v = candidates[np.argmax(scores)]
            Dk.add(v)
            Vrem.remove(v)
            colors[v] = 2
            for n in G.neighbors(v):
                if not colors[n]:
                    colors[n] = 1
            # optional reduce
        D.append(Dk)
        Vdone = Vdone.union(Dk)
    return D


if __name__ == '__main__':
    G = random_weighted_graph(10)
    result =objective_function(ghmwdds(G), G)
    print(result)
