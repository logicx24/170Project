from graph import Graph
from kruskal_path import kruskalsSolver
import numpy as np

g = Graph(open("instances/129.in").read())
# print g

path, cost = kruskalsSolver(g)
print "Path: ", path
print "Cost: ", cost
print "Valid Rudrata w/Color: ", g.is_valid_hamiltonian(path)
