from graph import Graph
from kruskal_path import kruskalsSolver
from dynamic_programming import dynamicSolver

OUTPUT_FILE = "answer1to125.out"
DYNAMIC_THRESHOLD = 10

answers = []
for i in range(1,125):
    g = Graph(open("instances/{0}.in".format(i)).read())
    results = []
    mapping = {}
    heuristics = [Graph.BASIC, Graph.SMART, Graph.BINOCULARS, Graph.SMART_BINOCULARS]
    for graph in [g, g.reweight()]:
        for heuristic in heuristics:
            try:
                path = graph.greedy(heuristic)
                # path = graph.greedy(heuristic, printer=True) # use this instead if you want to see how each heuristic is building up its path
                results.append(path)

                # instantiate a list for an empty path
                try:
                    a = mapping[tuple(path)]
                except KeyError:
                    mapping[tuple(path)] = []

                if heuristic == Graph.BASIC:
                    mapping[tuple(path)] += ["Basic"]
                elif heuristic == Graph.SMART:
                    mapping[tuple(path)] += ["Smart"]
                elif heuristic == Graph.BINOCULARS:
                    mapping[tuple(path)] += ["Binoculars"]
                elif heuristic == Graph.SMART_BINOCULARS:
                    mapping[tuple(path)] += ["Smart Binoculars"]

            except IndexError as e:
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
            a = mapping[tuple(kruskals_path)]
        except KeyError:
            mapping[tuple(kruskals_path)] = []

        mapping[tuple(kruskals_path)] += ["Kruskals"]

    # Direct Dynamic Solver (if applicable)
    if g.num_nodes <= DYNAMIC_THRESHOLD:
        dynamic_path, dynamic_cost = dynamicSolver(g)
        if dynamic_path == None or not g.is_valid_hamiltonian(dynamic_path):
            print "\t\tERROR in DIRECT DYNAMIC SOLVER"
        else:
            results.append(dynamic_path)

            try:
                a = mapping[tuple(dynamic_path)]
            except KeyError:
                mapping[tuple(dynamic_path)] = []

            mapping[tuple(dynamic_path)] += ["Dynamic"]

    if len(results) > 0:
        best = min(results, key=lambda path: g.path_cost(path))
        best_algs = mapping[tuple(best)]
        try:
            best_algs += mapping[tuple(best[::-1])]
        except KeyError:
            pass
        answers.append(best)
        open("{0}".format(OUTPUT_FILE), 'a').write(" ".join([str(node) for node in best]) + "\n")
        print "Answer found for {0} with ".format(i) + str(best_algs)
    else:
        print "********** MISSING ANSWER FOR {0} **********".format(i)

print "Answers finished writing"


