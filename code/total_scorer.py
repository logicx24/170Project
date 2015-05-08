import sys
from graph import Graph

NUM_FILES = 495

def total_score(answer_file="answers/answer.out", start=1):

	inputs = open(answer_file, 'r').read().split("\n")	
	total = 0
	for input_file_index in range(NUM_FILES):
		path = [int(x) for x in inputs[input_file_index].split()]
		graph = Graph(open("instances/{0}.in".format(input_file_index + 1)).read())

		if not graph.is_valid_hamiltonian(path):
			return None

		total += graph.path_cost(path)

	return total


# 
# Main Execution
#

print "Total Score: " + str(total_score())


