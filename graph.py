
class Graph(object):

	# the file in this case is passed in as one big string seperated by \n
	def __init__(self, file):
		lines = file.split("\n")
		last_index = len(lines) - 1
		self.num_nodes = int(lines[0])
		self.colors = lines[last_index].split("")
		self.weights_matrix = [[int(weight) for weight in line.split(" ")] for line in lines[1:last_index]]

	def set_weight(self, weight, node1, node2):
		self.weights_matrix[node1][node2] = weight
		self.weights_matrix[node2][node1] = weight

	def get_weight(self, node1, node2):
		return self.weights_matrix[node1][node2]

	def is_valid_sequence(self, seq):
		color_count = 0
		last_color = ""
		for node in seq:
			if node > self.num_nodes:
				return False
			color_count += (1 if last_color != self.colors[node] else 0)
			if color_count > 3:
				return False
			last_color = self.colors[node]
		return True

	def is_valid_hamiltonian(self, path):
		return len(list(set(path))) == self.num_nodes and len(list(set(path))) == len(path)






