path_to_cplex = r'C:\Program Files\IBM\ILOG\CPLEX_Studio221\cplex\bin\x64_win64\cplex.exe'
from pulp import *
import networkx as nx
from Graph_gen import random_weighted_graph
def solver(G):

    nodes_list = list(G.nodes)      #imena cvorova od 1 do n
    sortirano = sorted(G.degree, key = lambda x: x[1]) #?
    m = sortirano[0][1]                #cvor sa najmanje susjeda
    M = sortirano[len(sortirano)-1][1]  #cvor sa najvise susjeda


    # defining the problem
    prob = LpProblem("Objective_function", LpMaximize)


    #define problem variables
    x = {(i, j): LpVariable(cat=LpBinary, name=f'x_{i}_{j}') for i in nodes_list for j in range(1, m + 2)} #idk jedino ovako radi vidi mozes li skontati nesto drugo
    y = LpVariable.dict("y", range (1,m+2), 0, 1, LpBinary) #treba li donja i gornja granica ako je binary var?
    z = LpVariable.dict("z", range(1, m + 2), 0, M, LpContinuous)

    #define and add the objective function
    prob += ( lpSum( [z[j] for j in range (1,m+2)] ) )

    #constraints
    #cons 1
    for i in nodes_list:
        prob += lpSum( x[(i,j)] for j in range (1,m+2) ) <= 1
    #cons 2
    for j in range (1,m+2):
        for i in nodes_list:
            prob += lpSum( x[(k,j)] for k in list(G.adj[i]) ) >= y[j] - x[(i,j)] #sta je i
    #cons 3
    for i in nodes_list:
        for j in range (1,m+2):
            prob += y[j] >= x[(i,j)]
    #cons 4
    for i in nodes_list:
        for j in range (1,m+2):
            prob += (x[(i,j)] * G.nodes[i]["lifetime"] + (1- x[(i,j)]) * M) >= z[j]
    #cons 5
    for j in range (1,m+2):
        prob += y[j] * M >= z[j]
    # cons 6
    for j in range (1, m+1):
        prob += y[j] >= y[j+1]
    # cons 7
    for j in range(1, m+1):
        prob += z[j] >= z[j + 1]

    #solving
    solver = CPLEX_CMD(timelimit=600,msg=False,path=path_to_cplex)
    prob.solve(solver)

    #izvuci cvorove da se vidi koji su u kojoj particiji (za potrebe provjere)
    #variable_values = {(i, j): x[i, j].varValue for i in nodes_list for j in range(1, m + 2)}
    #result = [[] for _ in range(m + 1)]
    #for i in nodes_list:
    #    for j in range(1, m + 2):
    #        if variable_values[i, j] == 1:
    #            result[j - 1].append(i)
    result = value(prob.objective)
    # suma min cvorova
    #print("Objective value:", result)

    #print("lp solved")
    return result

if __name__ == '__main__':
    G = random_weighted_graph(10)
    result = solver(G)
    print(result)