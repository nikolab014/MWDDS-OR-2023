import networkx as nx
import random
from greedy import ghmwdds
from itertools import combinations
from Graph_gen import random_weighted_graph

def initial_domatic_partition(G):
    domatic_partition = [list(ds) for ds in ghmwdds(G)]
    # domatic_partition = [[0,2,4,6], [1,3,5]]
    return domatic_partition

def objective_function(G, solution):
    total_weight = sum(min(G.nodes[node]['lifetime'] for node in ds) for ds in solution)
    return total_weight

def shake(G, solution, k):
    if not solution:
        return solution
    ds_to_modify = random.choice(solution)
    if len(ds_to_modify) <= 1:
        return solution
    potential_nodes_to_remove = list(ds_to_modify)
    random.shuffle(potential_nodes_to_remove)
    for node in potential_nodes_to_remove:
        temp_ds = ds_to_modify.copy()
        temp_ds.remove(node)
        if nx.is_dominating_set(G, temp_ds):
            ds_to_modify.remove(node)
            k -= 1
        if k == 0:
            break
    return solution


def local_search(G, solution):
    def min_pair(G, ds1, ds2):
        return min([G.nodes[node]["lifetime"] for node in ds1]) + min([G.nodes[node]["lifetime"] for node in ds2])

    improvement = True
    temp_solution = solution.copy()
    while improvement:
        improvement = False
        for ds1, ds2 in combinations(temp_solution, 2):
            for node1 in ds1:
                for node2 in ds2:
                    temp_ds1 = ds1.copy()
                    temp_ds2 = ds2.copy()
                    temp_ds1.remove(node1)
                    temp_ds2.remove(node2)
                    temp_ds1.append(node2)
                    temp_ds2.append(node1)
                    if nx.is_dominating_set(G, temp_ds1) and nx.is_dominating_set(G, temp_ds2) and min_pair(G, temp_ds1,
                                                                                                            temp_ds2) > min_pair(
                            G, ds1, ds2):
                        improvement = True
                        ds1.remove(node1)
                        ds2.remove(node2)
                        ds1.append(node2)
                        ds2.append(node1)
                        break
    return temp_solution


def vns(G, max_iterations, k_max):
    solution = initial_domatic_partition(G)
    best_solution = solution.copy()
    #best_value = sum(min(G.nodes[node]['lifetime'] for node in ds) for ds in best_solution)
    best_value = objective_function(G, best_solution)
    for _ in range(max_iterations):
        k = 1
        while k <= k_max:
            s_prime = shake(G, solution.copy(), k)
            s_double_prime = local_search(G, s_prime)
            s_double_prime_value =  objective_function(G, s_double_prime)
            if s_double_prime_value > best_value:
                best_solution = s_double_prime
                best_value = s_double_prime_value
                k = 1
            else:
                k += 1
        solution = best_solution
    return best_value

if __name__ == '__main__':
    G = random_weighted_graph(10)
    result = vns(G,100,10)
    print(result)