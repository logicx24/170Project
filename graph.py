
class Graph(object):

	def __init__(self, file):
		lines = file.split("\n")
		last_index = len(lines) - 1
		self.file = file
		self.num_nodes = int(lines[0])
		self.colors = [color for color in lines[last_index]]
		self.weights_matrix = [[int(weight) for weight in line.split(" ")] for line in lines[1:last_index]]
		self.all_edges = []
		for i in range(self.num_nodes):
			for j in range(i+1, self.num_nodes):
				self.all_edges.append((i,j))

	def set_weight(self, weight, node1, node2):
		self.weights_matrix[node1][node2] = weight
		self.weights_matrix[node2][node1] = weight

	def get_weight(self, node1, node2):
		return self.weights_matrix[node1][node2]

	def remove_edge(self, node1, node2):
		self.weights_matrix[node1][node2] = -1
		self.weights_matrix[node2][node1] = -1

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
		return self.weights_matrix[node1][node2] != -1 and self.weights_matrix[node2][node1] != -1

	def is_valid_hamiltonian(self, path):
		return len(list(set(path))) == self.num_nodes and len(list(set(path))) == len(path) and self.is_valid_sequence(path)

	def __repr__(self):
		return "\n".join([" ".join([str(item) for item in self.weights_matrix[i]]) for i in range(len(self.weights_matrix))])

	def path_cost(self, path):
		return sum([self.weights_matrix[u][v] for u,v in zip(path[:-1], path[1:])])

	def creates_cycle(edge, path):
		if len(path) < 2:
			return False
		return edge[0] in path and edge[1] in path

	def valid_options(path):
		return [edge for edge in self.all_edges if not creates_cycle(edge, path) and (path[0] in edge or path[-1] in edge)]

	# returns a greedy solution
	def greedy_algorithm(self):
		weighter = lambda edge: self.get_weight(edge[0], edge[1])
		path = min(self.all_edges, weighter)
		while not self.is_valid_hamiltonian(path):
			left_endpoint, right_endpoint = path[0], path[-1]
			new_edge = min(valid_options(path), weighter)
			new_node = new_edge[0]
			if left_endpoint in new_edge:
				if left_endpoint == new_edge[0]:
					new_node = new_edge[1]
				path = [new_node] + path
			else:
				if right_endpoint == new_edge[0]:
					new_node = new_edge[1]
				path = path + [new_node]
		return path

	def duplicate(self):
		return Graph(self.file)

	def family(self, node):
		return [edge for edge in self.all_edges if node in edge]

	def avg(self, node):
		edge_weight = lambda edge: self.get_weight(edge[0], edge[1])
		edges = family(node)
		return sum([edge_weight(edge) for edge in edges])/float(len(edges))

	def f(self, edge, node):
		return self.get_weight(edge[0], edge[1])/avg(node)

	def true_weight(self, edge):
		return self.f(edge, edge[0]) + self.f(edge, edge[1])

	def reweight(self):
		graph2 = graph.duplicate()
		for edge in graph2.all_edges:
			graph2.set_weight(graph.true_weight(edge), edge[0], edge[1])
		return graph2
