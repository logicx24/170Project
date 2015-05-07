from graph import Graph
from kruskal_path import kruskalsSolver
from dynamic_programming import dynamicSolver

OUTPUT_FILE = "answer1to125.out"
DYNAMIC_THRESHOLD = 12

answers = []
for i in range(6,125):
    g = Graph(open("instances/{0}.in".format(i)).read())
    results = []
    mapping = {}
    heuristics = [Graph.BASIC, Graph.SMART, Graph.BINOCULARS]
    for graph in [g, g.reweight()]:
        for heuristic in heuristics:
            try:
                path = graph.greedy(heuristic)
                # path = graph.greedy(heuristic, printer=True) # use this instead if you want to see how each heuristic is building up its path
                results.append(path)

                # instantiate a list for an empty path
                try:
                    a = mapping[g.path_cost(tuple(path))]
                except KeyError:
                    mapping[g.path_cost(tuple(path))] = []

                if heuristic == Graph.BASIC:
                    mapping[g.path_cost(tuple(path))] += ["Basic"]
                elif heuristic == Graph.SMART:
                    mapping[g.path_cost(tuple(path))] += ["Smart"]
                elif heuristic == Graph.BINOCULARS:
                    mapping[g.path_cost(tuple(path))] += ["Binoculars"]
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

    results.append(list(range(g.num_nodes)))

    if g.path_cost(tuple(list(range(g.num_nodes)))) not in mapping:
      mapping[g.path_cost(tuple(list(range(g.num_nodes))))] = []
    mapping[g.path_cost(tuple(list(range(g.num_nodes))))] += ["Null"]

    if len(results) > 0:
        best = min(results, key=lambda path: g.path_cost(path))
        best_algs = mapping[g.path_cost(tuple(best))]
        answers.append(best)
        open("{0}".format(OUTPUT_FILE), 'a').write(" ".join([str(node) for node in best]) + "\n")
        print "Answer found for {0} with ".format(i) + str(best_algs)
    else:
        print "********** MISSING ANSWER FOR {0} **********".format(i)

print "Answers finished writing"


