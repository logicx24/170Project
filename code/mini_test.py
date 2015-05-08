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
from dynamic_programming import dynamicSolver


DYNAMIC_THRESHOLD = 12

answers = []

should_parallelize = False
i = 253
g = Graph(open("instances/{0}.in".format(i)).read())
results = []
mapping = {}
heuristics = [Graph.BASIC, Graph.SMART, Graph.BINOCULARS]
for index, graph in enumerate([g, g.reweight()]):
    for heuristic in heuristics:
        try:
            #print should_parallelize
            path = graph.greedy(heuristic, should_parallelize=should_parallelize)
            # path = graph.greedy(heuristic, printer=True) # use this instead if you want to see how each heuristic is building up its path
            if path is not None:
              results.append(path)

              # instantiate a list for an empty path
              try:
                  a = mapping[g.path_cost(tuple(path))]
              except KeyError:
                  mapping[g.path_cost(tuple(path))] = []

              t = " Reweighted" if index == 1 else ""

              if heuristic == Graph.BASIC:
                  mapping[g.path_cost(tuple(path))] += ["Basic" + t]
                  print "path with cost {0} found by {1}".format(g.path_cost(tuple(path)), "Basic" + t)
              elif heuristic == Graph.SMART:
                  mapping[g.path_cost(tuple(path))] += ["Smart" + t]
                  print "path with cost {0} found by {1}".format(g.path_cost(tuple(path)), "Smart" + t)
              elif heuristic == Graph.BINOCULARS:
                  mapping[g.path_cost(tuple(path))] += ["Binoculars" + t]
                  print "path with cost {0} found by {1}".format(g.path_cost(tuple(path)), "Binoculars" + t)

            else:
              print "{0} found no valid path".format(heuristic)
        except ValueError as e:
            print "\t\tERROR in {0}".format(heuristic)
            continue
#
# Trying other algorithms:
#

# Kruskals
kruskals_path, kruskals_cost = kruskalsSolver(g)
if kruskals_path == None or not g.is_valid_hamiltonian(kruskals_path):
    print "\t\tERROR in KRUSKALS"
else:
    results.append(kruskals_path)
                    # instantiate a list for an empty path
    try:
        a = mapping[g.path_cost(tuple(kruskals_path))]
    except KeyError:
        mapping[g.path_cost(tuple(kruskals_path))] = []

    mapping[g.path_cost(tuple(kruskals_path))] += ["Kruskals"]

# Direct Dynamic Solver (if applicable)
if g.num_nodes <= DYNAMIC_THRESHOLD:
    print "USING DYNAMIC SOLVER for " + str(i)
    dynamic_path, dynamic_cost = dynamicSolver(g)
    if dynamic_path == None or not g.is_valid_hamiltonian(dynamic_path):
        print "\t\tERROR in DIRECT DYNAMIC SOLVER"
        print dynamic_path
    else:
        results.append(dynamic_path)

        try:
            a = mapping[g.path_cost(tuple(dynamic_path))]
        except KeyError:
            mapping[g.path_cost(tuple(dynamic_path))] = []

        mapping[g.path_cost(tuple(dynamic_path))] += ["Dynamic"]

# Null heuristic
null_path = list(range(g.num_nodes))
if g.is_valid_hamiltonian(null_path):
    results.append(list(range(g.num_nodes)))
    if g.path_cost(tuple(list(range(g.num_nodes)))) not in mapping:
        mapping[g.path_cost(tuple(list(range(g.num_nodes))))] = []
    mapping[g.path_cost(tuple(list(range(g.num_nodes))))] += ["Null"]

if len(results) > 0:
    best = min(results, key=lambda path: g.path_cost(path))
    best_algs = mapping[g.path_cost(tuple(best))]
    answers.append(best)
    print "Answer found for {0} with ".format(i) + str(best_algs)
else:
    print "********** MISSING ANSWER FOR {0} **********".format(i)

print "PATH: ", answers[0]
print "COST: ", g.path_cost(answers[0])
print "ALGS: ", best_algs