
# testing interface

import graph
import matrix

while True:
  matrix.write(8)
  g = graph.Graph(open("1.in").read())
  print "------------------------------------"
  print "Best cost from TSP: {0}".format(g.best_cost())
  print "Greedy cost: {0}".format(g.path_cost(g.greedy()))
  print "Smart greedy cost: {0}".format(g.path_cost(g.smart_greedy()))
  print "Greedy w/ reweighting: {0}".format(g.path_cost(g.reweight().greedy()))
  print "Smart greedy w/ reweighting: {0}".format(g.path_cost(g.reweight().smart_greedy()))
