class CoordGraph(Graph):
  # a class that has nodes with embedded coordinates
  def __init__(self, n):
    super() # TODO figure out how to make empty adj matrix for edge weights
    self.coordinates = [0] * n

  def set_coord(self, node, new_coords):
    self.coordinates[node] = new_coords

  def add_edge_without_weight(self, node1, node2):
    # use -1 to indicate that edge weight hasn't been established yet
    self.adj_matrix[node1][node2] = -1
    self.adj_matrix[node2][node1] = -1

  def find_dist(self, node1, node2):
    node1_coord = self.coordinates[node1]
    node2_coord = self.coordinates[node2]
    return ((node1[0]-node2[0])**2 + (node1[1]-node2[1])**2)**0.5


  # def add_edge_with_coord(self, weight, node1, node2, coord):
  #   self.add_edge(weight, node1, node2)


def break_triangle_inequality(n, scale):
  # produces an output file specifically designed to mess with MST-based algorithms.
  graph = CoordGraph(n)
  graph.set_coord(0, (0, 0))
  for i in range(1, n):
    graph.add_edge(i*scale, i-1, i)
  for j in range(1, n):
    dist = graph.find_dist(i-1, i)
    graph.add_edge(dist*random.randint(1, 100))
  return graph