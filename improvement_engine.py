import sys

from graph import Graph
from dynamic_programming import dynamicSolver

def compare_paths(graph_to_change, new_path, answer_file='answers/answer.out', start=1, print_output=False):
	"""
		This method takes in a new path for a graph and checks to see if it is better than the current
		path that is stored in the answer_file. If the path is better, we change the output file to have
		that path.

		:param: graph_to_change - the graph num to change. For example, to change file 121.in, pass in 121
		:param: new_path - the new path to replace in the file, if it is better
		:param: answer_file - the output file where the answers are stored that needs changing
		:param: start - the file number at line 1 of the output file. For example, if the output
						file has the path for 121.in on line 1, then pass in 121
		:param: print_output - boolean that reflects whether you want this function to print information
	"""
	index = graph_to_change - start
	inputs = open(answer_file, 'r').read().split("\n")
	old_path = [int(x) for x in inputs[index].split()]
	best_path = find_best(old_path, new_path, graph_to_change, print_output)
	inputs[index] = ' '.join([str(x) for x in best_path])
	open(answer_file, 'w').write("\n".join(inputs))


def find_best(old_path, new_path, graph_num, print_output=False):
	"""
		This method finds the best of the two input paths for the graph with number graph_num, 
		and returns it.

		:param: old_path - our current answer for this graph
		:param: new_path - the new path to check
		:param: graph_num - the graph file number. For example, for file 121.in, pass in 121
		:param: print_output - boolean that reflects whether you want this function to print information
		:return: the best path of the input paths
	"""
	graph = Graph(open('instances/{0}.in'.format(graph_num)).read())

	new_path_cost = graph.path_cost(new_path)
	old_path_cost = graph.path_cost(old_path)

	if print_output:
		print "New Path: ", new_path, " with cost: ", new_path_cost
		print "Old Path: ", old_path, " with cost: ", old_path_cost

	if not graph.is_valid_hamiltonian(new_path):
		if print_output:
			print "New path is not a valid hamiltonian"
		return old_path
	elif new_path_cost < old_path_cost:
		if print_output:
			print "New path selected"
		return new_path
	else:
		print "Old path selected"
		return old_path

