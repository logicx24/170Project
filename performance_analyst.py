import os
# performance analyst interface

from graph import Graph
import matrix
from multiprocessing import *
import validator
import scorer_multiple


def perTest(filename):
  g = Graph(open("./instances/" + filename).read())
  mappings = {}

  #tsps = g.best_cost()
  greedy = g.greedy()
  smart_greedy = g.greedy(Graph.SMART)
  greedy_reweighted = g.reweight().greedy()
  smart_greedy_reweighted = g.reweight().greedy(Graph.SMART)

  paths = [greedy, smart_greedy, greedy_reweighted, smart_greedy_reweighted]
  names = ["greedy", "smart_greedy", "greedy_reweighted", "smart_greedy_reweighted"]

  #greedy_with_binoculars = g.path_cost(g.greedy(Graph.BINOCULARS))
  #greedy_with_binoculars_reweighted = g.path_cost(g.reweight().greedy(Graph.BINOCULARS))
  #guru = g.path_cost(g.greedy(Graph.GURU))

  # use defaultdict instead
  #mappings[tsps] = []
  # mappings[greedy] = []
  # mappings[smart_greedy] = []
  # mappings[greedy_reweighted] = []
  # mappings[smart_greedy_reweighted] = []
  #mappings[greedy_with_binoculars] = []
  #mappings[greedy_with_binoculars_reweighted] = []
  #mappings[guru] = []

  #mappings[tsps].append("TSP")
  # mappings[greedy].append("Greedy")
  # mappings[smart_greedy].append("Smart Greedy")
  # mappings[greedy_reweighted].append("Greedy Reweighted")
  # mappings[smart_greedy_reweighted].append("Smart Greedy Reweighted")
  #mappings[greedy_with_binoculars].append("Greedy With Binoculars")
  #mappings[greedy_with_binoculars_reweighted].append("Greedy With Binoculars Reweighted")
  #mappings[guru].append("GURU")

  #scores = sorted(mappings.keys())
  print "------------------------------------"
  for index, path in enumerate(paths):
    open('answer.out', 'w').write(" ".join(str(integ) for integ in path))
    print names[index] + ": " + scorer_multiple.main()
  

if __name__ == "__main__":
  #pool = Pool(processes=cpu_count())
  #pool.map(validate, os.listdir('./instances'))
  print(os.listdir('./instances'))
  for name in os.listdir('./instances'):
    print validate('./instances/' + name)
    perTest(name)
  #pool.map(perTest, os.listdir('./instances'))
  #pool.close()

