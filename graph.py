
class Graph(object):

	def __init__(self, graph_array, n, red_blue_str):
		self.adj_matrix = graph_array
		self.num_nodes = n 
		self.colors = red_blue_str.split("")

	def add_edge(self, weight, node1, node2):
		self.adj_matrix[node1][node2] = weight
		self.adj_matrix[node2][node1] = weight

	def remove_edge(self, node1, node2):
		self.adj_matrix[node1][node2] = None
		self.adj_matrix[node2][node1] = None

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
		return self.is_valid_path(seq)

	def is_valid_path(self, path):
		for u, v in zip(path[:-1], path[1:]):
			if not self.has_edge(u, v):
				return False
		return True

	def has_edge(self, node1, node2):
		return self.adj_matrix[node1][node2] != None

	def is_valid_hamiltonian(self, path):
		return len(list(set(path))) == self.num_nodes and len(list(set(path))) == len(path) and self.is_valid_sequence(path)

	def __repr__(self):
		return "\n".join([" ".join([str(item) for item in self.adj_matrix[i]]) for i in range(len(self.adj_matrix))]) 



				



