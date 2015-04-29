import numpy
import itertools
from graph import Graph


def sort_to_tuple(my_set):
	return tuple(sorted(list(my_set)))

def dynamicSolver(graph):
  	n = graph.num_nodes
	all_nodes = set(range(n))

	collection = {}
	collection[((0,), 0)] = 0
	for s in range(2, n+1):
		all_nodes_but_one = all_nodes - {0}
		for subset in itertools.combinations(all_nodes_but_one, s-1):
			subset = set(subset).union({0}) 								# add in the first node to the subset
			collection[(sort_to_tuple(subset), 0)] = float("inf")
			for j in sort_to_tuple(subset):
				if j == 0:
					continue
				else:
					collection[(sort_to_tuple(subset), j)] = min(collection[(sort_to_tuple(subset - {j}), i)] + graph.get_weight(i, j) for i in sort_to_tuple(subset) if i != j)
	return min(collection[(sort_to_tuple(all_nodes), j)] + graph.get_weight(0, j) for j in (all_nodes - {0}))

g = Graph(open('1.in').read())
print dynamicSolver(g)

class DynamicNode():

    def __init__(self, value=0, blue_count=0, red_count=0, prev=None):
        self.value = value
        self.prev = prev
        self.blue_count = blue_count
        self.red_count = red_count
