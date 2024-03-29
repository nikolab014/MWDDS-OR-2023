import networkx as nx
import random
import pandas as pd
import time
#from Graph_gen import *
from fast_graph_gen import *
from VNS import vns
from LP_solver import solver
from greedy import *


def func1(arg):
    return solver(arg)


def func2(arg):
    return vns(arg,100,3)


def func3(arg):
    return objective_function(ghmwdds(arg), arg)


def benchmark_function(func, args_list):
    runtimes = []
    results = []

    for arg in args_list:
        if func == func2:
            temp_runtimes = []
            temp_results = []

            for _ in range(10):
                start_time = time.time()
                result = func(arg)
                end_time = time.time()

                temp_runtimes.append(end_time - start_time)
                temp_results.append(result)

            runtimes.append(temp_runtimes)
            results.append(temp_results)

        else:
            start_time = time.time()
            result = func(arg)
            end_time = time.time()

            runtimes.append(end_time - start_time)
            results.append(result)

    return runtimes, results


def main():
    args_list = create_list_of_random_graphs()

    functions = [func1, func2, func3]  # Solveri

    all_runtimes = []
    all_results = []

    for func in functions:
        runtimes, results = benchmark_function(func, args_list)
        all_runtimes.append(runtimes)
        all_results.append(results)

    data = {
        'Arguments': list(range(len(args_list))),
        'Func1_Runtime': all_runtimes[0],
        'Func1_Result': all_results[0]
    }

    for i in range(10):
        data[f"Func2_Runtime_{i + 1}"] = [runtimes[i] for runtimes in all_runtimes[1]]
        data[f"Func2_Result_{i + 1}"] = [result[i] for result in all_results[1]]

    data['Func3_Runtime'] = all_runtimes[2]
    data['Func3_Result'] = all_results[2]

    df = pd.DataFrame(data)
    csv_filename = "benchmark_results.csv"
    df.to_csv(csv_filename, index=False)


if __name__ == "__main__":
    main()