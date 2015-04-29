
class Graph(object):

    # the file in this case is passed in as one big string seperated by \n

    def __init__(self, file):
        lines = file.split("\n")
        last_index = len(lines) - 1
        self.num_nodes = int(lines[0])
        self.colors = lines[last_index].split("")
        self.weights_matrix = [
            [int(weight) for weight in line.split(" ")] for line in lines[1:last_index]]

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
        return True

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
        return sum([self.weights_matrix[u][v] for u, v in zip(path[:-1], path[1:])])
