import os
# performance analyst interface

from graph import Graph
import matrix
from multiprocessing import *
import validator
import scorer_multiple

def validate(s):
    fin = open(s, "r")
    line = fin.readline().split()
    if len(line) != 1 or not line[0].isdigit():
        return "Line 1 must contain a single integer."
    N = int(line[0])
    if N < 4 or N > 50 or N % 2 != 0:
        return "N must be an even integer between 4 and 50, inclusive."

    d = [[0 for j in range(N)] for i in range(N)]
    for i in xrange(N):
        line = fin.readline().split()
        if len(line) != N:
            return "Line " + `i + 2` + " must contain N integers."
        for j in xrange(N):
            if not line[j].isdigit():
                return "Line " + `i + 2` + " must contain N integers."
            d[i][j] = int(line[j])
            a = int(line[j])
            if d[i][j] < 0 or d[i][j] > 100:
                return "All edge weights must be between 0 and 100, inclusive."
    for i in xrange(N):
        if d[i][i] != 0:
            return "The distance from a node to itself must be 0."
        for j in xrange(N):
            if d[i][j] != d[j][i]:
                return "The distance matrix must be symmetric."

    line = fin.readline()
    if len(line) != N:
        return "Line " + `N + 2` + " must be a string of length N."
    r = 0
    b = 0
    for j in xrange(N):
        c = line[j]
        if c != 'R' and c != 'B':
            return "Each character of the string must be either R or B."
        if c == 'R':
            r += 1
        if c == 'B':
            b += 1

    if r != b:
        return "The number of red and blue cities must be equal."
    return "ok"


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

