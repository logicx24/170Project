import sys

from graph import Graph
from dynamic_programming import dynamicSolver
from improvement_engine import compare_paths

file_to_change = 213
graph = Graph(open("instances/{0}.in".format(file_to_change)).read())
new_path, new_cost = dynamicSolver(graph)
compare_paths(file_to_change, new_path, print_output=True)
