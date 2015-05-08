import sys

from graph import Graph
from dynamic_programming import dynamicSolver, quickDynamicSolver, dynamicSolverParallel
from improvement_engine import compare_paths

NUM_FILES = 495

for file_to_change in range(1, NUM_FILES + 1):
	graph = Graph(open("instances/{0}.in".format(file_to_change)).read())

	if graph.num_nodes == 20: 
		print "Running Dynamic Solver on {0}.in of size {1}".format(file_to_change, graph.num_nodes)  
		new_path, new_cost = dynamicSolverParallel(graph)
		compare_paths(file_to_change, new_path, print_output=True)
		print "\n"
