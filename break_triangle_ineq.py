from graph import Graph
import random

class CoordGraph(Graph):
  # a class that has nodes with embedded coordinates
  def __init__(self, graph_array, n, red_blue_str):
    super(self, graph_array, n, red_blue_str) # TODO figure out how to make empty adj matrix for edge weights
    self.coordinates = [0] * n

  def __init__(self, n):
    # randomly initializes nodes and make all weights 0
    rand_string = random.shuffle(["R","B"]*(n/2))
    super(self, [[0]*n]*n, n, rand_string)

  def set_coord(self, node, new_coords):
    self.coordinates[node] = new_coords

  def set_rand_coords(self):
    for node in range(self.num_nodes):
      coordinates = (random.randint(0, 20), random.randint(0, 20))
      self.set_coord(node, coordinates)

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


def break_triangle_inequality(n):
  # produces an output file specifically designed to mess with MST-based algorithms.
  graph = CoordGraph(n)
  graph.set_rand_coords()
  for node1 in range(n):
    for node2 in range(node1, n):
      expected_dist = graph.find_dist(node1, node2)
      if random.choice([True, False]):
        graph.set_weight(random.randint(2) * expected_dist, node1, node2)
      else:
        graph.set_weight(expected_dist)
  return graph
