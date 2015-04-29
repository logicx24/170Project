from graph import Graph
import random

class CoordGraph(Graph):
  # a class that has nodes with embedded coordinates

  def __init__(self, n):
    # initializes with weights of -1, random colors, and coordinates of None
    self.num_nodes = n
    self.weights_matrix = [[0]*n]*n
    self.colors = random.shuffle(["R","B"]*(n/2))
    self.coordinates = [None]*n

  def set_coord(self, node, new_coord):
    self.coordinates[node] = new_coord

  def get_coord(self, node):
    return self.coordinates[node]

  def set_rand_coords(self):
    # FIXME here be magic numbers
    for node in range(self.num_nodes):
      coordinates = (random.randint(0, 20), random.randint(0, 20))
      self.set_coord(node, coordinates)

  def add_edge_without_weight(self, node1, node2):
    # use -1 to indicate that edge weight hasn't been established yet
    self.weights_matrix[node1][node2] = -1
    self.weights_matrix[node2][node1] = -1

  def find_dist(self, node1, node2):
    # calculates the distance between 2 nodes based on their coordinates
    node1_coord = self.coordinates[node1]
    node2_coord = self.coordinates[node2]
    return ((node1_coord[0] - node2_coord[0])**2 + (node1_coord[1] - node2_coord[1])**2)**0.5

  def print_coords(self):
    # print "\n".join([" ".join([str(item) for item in self.coordinates[i]]) for i in range(len(self.coordinates))])
    print self.coordinates


def break_triangle_inequality(n):
  # produces an output file specifically designed to mess with MST-based algorithms.
  graph = CoordGraph(n)
  graph.set_rand_coords()
  for node1 in range(n):
    for node2 in range(node1, n):
      expected_dist = graph.find_dist(node1, node2)
      if random.choice([True, False]):
        # FIXME here be more magic numbers
        graph.set_weight(random.randint(1, 2) * expected_dist, node1, node2)
      else:
        graph.set_weight(expected_dist, node1, node2)
  return graph
