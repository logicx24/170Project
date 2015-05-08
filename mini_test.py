# from graph import Graph
# from kruskal_path import kruskalsSolver
# import numpy as np

# g = Graph(open("instances/357.in").read())
# # print g

# path, cost = kruskalsSolver(g)
# print "Path: ", path
# print "Cost: ", cost
# print "Valid Rudrata w/Color: ", g.is_valid_hamiltonian(path)

import sys

from graph import Graph
from kruskal_path import kruskalsSolver
from dynamic_programming import dynamicSolver, dynamicSolverParallel
from timeit import default_timer


graph = Graph(open('instances/75.in').read())


start = default_timer()
path, cost = dynamicSolverParallel(graph)
end = default_timer()
print "Path: ", path
print "Cost: ", cost
print "Time: ", end - start, " seconds"


