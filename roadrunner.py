from graph import Graph

OUTPUT_FILE = "answer.out"

answers = []
for i in range(406,496):
  g = Graph(open("instances/{0}.in".format(i)).read())
  results = []
  heuristics = [Graph.BASIC, Graph.SMART]
  for graph in [g, g.reweight()]:
    for heuristic in heuristics:
      try:
        results.append(graph.greedy(heuristic))
      except IndexError as e:
        print " -- error in {0}".format(heuristic)
        continue
  if len(results) > 0:
    best = min(results, key=lambda path: g.path_cost(path))
    answers.append(best)
    open("{0}".format(OUTPUT_FILE), 'a').write(" ".join([str(node) for node in best]) + "\n")
    print "Answer found for {0}".format(i)
  else:
    print "********** MISSING ANSWER FOR {0} ****************".format(i)

print "Answers finished writing"