
# performance analyst interface

from graph import Graph
import matrix

i = 0
while i == 0:
  i += 1
  #matrix.write(26)

  g = Graph(open("4.in").read())
  print "------------------------------------"
  mappings = {}

  #tsps = g.best_cost()
  greedy = g.path_cost(g.greedy())
  smart_greedy = g.path_cost(g.greedy(Graph.SMART))
  greedy_reweighted = g.path_cost(g.reweight().greedy())
  smart_greedy_reweighted = g.path_cost(g.reweight().greedy(Graph.SMART))
  greedy_with_binoculars = g.path_cost(g.greedy(Graph.BINOCULARS))
  greedy_with_binoculars_reweighted = g.path_cost(g.reweight().greedy(Graph.BINOCULARS))
  guru = g.path_cost(g.greedy(Graph.GURU))

  # use defaultdict instead
  #mappings[tsps] = []
  mappings[greedy] = []
  mappings[smart_greedy] = []
  mappings[greedy_reweighted] = []
  mappings[smart_greedy_reweighted] = []
  mappings[greedy_with_binoculars] = []
  mappings[greedy_with_binoculars_reweighted] = []
  mappings[guru] = []

  #mappings[tsps].append("TSP")
  mappings[greedy].append("Greedy")
  mappings[smart_greedy].append("Smart Greedy")
  mappings[greedy_reweighted].append("Greedy Reweighted")
  mappings[smart_greedy_reweighted].append("Smart Greedy Reweighted")
  mappings[greedy_with_binoculars].append("Greedy With Binoculars")
  mappings[greedy_with_binoculars_reweighted].append("Greedy With Binoculars Reweighted")
  mappings[guru].append("GURU")

  scores = sorted(mappings.keys())
  for score in scores:
    print score
    print mappings[score]
