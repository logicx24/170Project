import numpy
import itertools
from graph import Graph

def sort_to_tuple(my_set):
	return tuple(sorted(list(my_set)))

def dynamicSolver(graph):
	print graph

  	n = graph.num_nodes
	best_val = float("inf")
	best_path = None
	for start in range(n):
		path, val = dynamicSolverFromStart(graph, start)
		if val < best_val:
			best_val = val
			best_path = path
	return best_path, best_val

def dynamicSolverFromStart(graph, start):
  	n = graph.num_nodes
	all_nodes = set(range(n))

	collection = {}
	collection[((start,), start)] = DynamicNode({start})   ### set to a dynamic node
	for s in range(2, n+1):
		all_nodes_but_one = all_nodes - {start}
		for subset in itertools.combinations(all_nodes_but_one, s-1):
			subset = set(subset).union({start}) 								# add in the first node to the subset
			collection[(sort_to_tuple(subset), start)] = DynamicNode(subset, value=float("inf"))  	### set to a DynamicNode
			for j in sort_to_tuple(subset):
				if j == start:
					continue
				else:
					min_node, min_val = smallest_valued_node([(collection[(sort_to_tuple(subset - {j}), i)], collection[(sort_to_tuple(subset - {j}), i)].value + graph.get_weight(i, j)) for i in sort_to_tuple(subset) if i != j])
					collection[(sort_to_tuple(subset), j)] = DynamicNode(subset, value=min_val, prev=min_node)

	min_node, val = smallest_valued_node([(collection[(sort_to_tuple(all_nodes), j)], collection[(sort_to_tuple(all_nodes), j)].value) for j in (all_nodes - {start})])
	return retrace_steps(min_node), val 


def smallest_valued_node(node_lst):
    	argmin = node_lst[0][0]
    	min_val = node_lst[0][1]

    	for node in node_lst[1:]:
    		if node[1] < min_val:
    			min_val = node[1]
    			argmin = node[0]

    	return argmin, min_val


def retrace_steps(node):
	ptr = node
	lst = []
	while ptr.prev != None:
		difference = ptr.node_set - ptr.prev.node_set
		lst += list(difference)
		ptr = ptr.prev

	lst += list(ptr.node_set)
	return lst


class DynamicNode():

    def __init__(self, node_set, value=0.0, blue_count=0, red_count=0, prev=None):
        self.value = value
        self.prev = prev
        self.blue_count = blue_count
        self.red_count = red_count
        self.node_set = node_set


g = Graph(open('1.in').read())
print dynamicSolver(g)
