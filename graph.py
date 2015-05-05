import numpy as np
import time

COLOR_LIMIT = 3

class Edge(object):

    def __init__(self, vertex1, vertex2, weight):
        self.vertices = (vertex1, vertex2)
        self.weight = weight

    def __eq__(self, other):
        return self.weight == other.weight and self.vertices == other.vertices

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.lt(other) or self.weight == other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __le__(self, other):
        return self.gt(other) or self.weight == other.weight

def timer(func):
  start, end = None, None
  def helper(*args):
    start = time.time()
    result = func(*args)
    end = time.time()
    print "Time elapsed: {0}".format(end-start)
    return result

class Graph(object):

  # heuristic keys
  BASIC = 1
  SMART = 2
  BINOCULARS = 3
  GURU = 4
  STUBBORN = 5
  SMART_BINOCULARS = 6

  def __init__(self, file=None, weights_matrix=None, colors_list=None):
      if file:
          lines = [line.strip() for line in file.split("\n") if line != '']
          last_index = len(lines) - 1
          self.file = file
          self.num_nodes = int(lines[0])
          self.colors = [color for color in lines[last_index]]
          self.weights_matrix = [[int(weight) for weight in line.split(" ")] for line in lines[1:last_index]]

          self.all_edges = []
          for i in range(self.num_nodes):
              for j in range(i+1, self.num_nodes):
                  self.all_edges.append((i,j))

      elif weights_matrix and colors_list: # no file!
          self.file = None
          self.num_nodes = len(colors_list)
          self.weights_matrix = weights_matrix
          self.colors = colors_list
          self.all_edges = []
          for i in range(self.num_nodes):
              for j in range(i+1, self.num_nodes):
                  self.all_edges.append((i,j))

      elif colors_list:  # no edges!

          self.file = None
          self.num_nodes = len(colors_list)
          self.colors = colors_list
          self.all_edges = []

          # initialize all edges to -1s
          self.weights_matrix = [([-1]*n)[:] for _ in range(n)]
          for i in range(self.num_nodes):
              self.set_weight(0, i, i)

      else:
          self.file = None
          self.num_nodes = 0
          self.weights_matrix = [[]]
          self.all_edges = []
          self.colors = []

  # TOOLS FOR GRAPH MANIPULATION

  def set_weight(self, weight, node1, node2):
      """
          This method is for changing the the weight of an already
          existing edge in the graph. If you want to add a new edge to
          the graph, use add_edge()
      """
      self.weights_matrix[node1][node2] = weight
      self.weights_matrix[node2][node1] = weight

  # LOL OMG GUYS GET IT ADDEDGE
  def add_edge(self, weight, node1, node2):
      """
          This method is for actually adding an edge to the graph; if
          you just want to set the weight, use the set_weight() method.
      """
      self.set_weight(weight, node1, node2)
      self.all_edges.append(Graph._get_edge_repr(node1, node2))

  def copy_empty(self):
      """
          Creates graph identical to SELF, except with no edges.
      """
      return Graph(graph.colors)

  def get_weight(self, node1, node2):
      weight = self.weights_matrix[node1][node2]
      if weight == -1:
          return None
      else:
          return weight

  def get_degree(self, node):
      """
          This method returns the degree of a particular node.

          :runtime: This methods runs in O(|V|) time, because the representation
                    of the edges is an adjacency matrix not an adjacency list.
      """
      return len(self.get_neighbors(node))

  def get_neighbors(self, node):
      """
          This method returns the neighbors of a particular node.

          :runtime: This methods runs in O(|V|) time, because the representation
                    of the edges is an adjacency matrix not an adjacency list.
      """
      adjacent_nodes = []
      for possible_neighbor in range(self.num_nodes):
          if self.get_weight(node, possible_neighbor) and possible_neighbor != node:
              adjacent_nodes.append(possible_neighbor)
      return adjacent_nodes

  def _get_edge_repr(node1, node2):
      """
          This PRIVATE method takes in two numbers (node indicies) and
          returns a sorted tuple of these numbers.
      """
      return tuple(sorted((node1, node2)))

  def get_avg_weight(self):
      weight_sum = 0.0
      num_edges = 0.5 * self.num_nodes * (self.num_nodes - 1)
      for node1 in range(self.num_nodes):
          for node2 in range(node1+1, self.num_nodes):
              weight_sum += self.get_weight(node1, node2)
      return weight_sum / num_edges

  def remove_edge(self, node1, node2):
      """
          This method completely removes an edge between node1 and node2
          from the graph.
      """
      self.weights_matrix[node1][node2] = -1
      self.weights_matrix[node2][node1] = -1

      # remove the edge from the edge list
      self.all_edges.remove(Graph._get_edge_repr(node1, node2))

  def has_edge(self, node1, node2):
      return self.weights_matrix[node1][node2] != -1 and self.weights_matrix[node2][node1] != -1

  def is_red(self, node):
      return self.colors[node] == 'R'

  def is_blue(self, node):
      return self.colors[node] == 'B'

  def get_color(self, node):
      return self.colors[node]

  def get_sorted_edges(self, node):
      # edge = [Edge() for edge in self.all_edges]
      return sorted(self.all_edges, key=lambda x: self.weights_matrix[x[0]][x[1]])

  def __repr__(self):
      return str(self.num_nodes) + "\n" + \
                   "\n".join([" ".join([str(item) for item in self.weights_matrix[i]]) for i in range(len(self.weights_matrix))]) + "\n" + \
                   "".join(self.colors)

  # PATH AND EDGE RELATED

  def is_valid_sequence(self, seq):
      """ Makes sure that the given sequence has at most 3 of the same color in a row. """
      color_count = 0
      last_color = ""
      for node in seq:
          if node > self.num_nodes:
              return False
          color_count += (1 + color_count if last_color == self.colors[node] else 0)
          if color_count > 3:
              return False
          last_color = self.colors[node]
      return self.is_valid_path(seq)

  def is_valid_path(self, path):
      """ Makes sure that the permutation of nodes passed in is possible given the edges still available. """
      for u, v in zip(path[:-1], path[1:]):
          if not self.has_edge(u, v):
              return False
      return True

  def is_valid_hamiltonian(self, path):
      """ Self explanatory """
      return len(list(set(path))) == self.num_nodes and len(list(set(path))) == len(path) and self.is_valid_coloring(path)

  def is_valid_hamiltonian_and_seq(self, path):
      return len(list(set(path))) == self.num_nodes and len(list(set(path))) == len(path)# and self.is_valid_sequence(path)

  def path_cost(self, path):
      return sum([self.get_weight(u, v) for u,v in zip(path[:-1], path[1:])])

  def trace_path(self, path):
      weights = self.weights_of_path(path)
      path_colors = [self.colors[node] for node in path]
      weights.insert(0, 0) # the first node on the path doesn't have an edge going into it
      return [str(node)+str(color)+":"+str(weight) for node, color, weight in zip(path, path_colors, weights)]

  def creates_cycle(self, edge, path):
      """ Checks to see if adding a given EDGE creates a cycle given a PATH """
      if len(path) < 2:
          return False
      return edge[0] in path and edge[1] in path

  def is_last_color(self, path, edge):
      new_path = self.append_edge(path, edge)
      num_blues = sum([1 for node in new_path if self.is_blue(node)])
      num_reds = sum([1 for node in new_path if self.is_red(node)])
      num_blues_left = self.num_nodes / 2 - num_blues
      num_reds_left = self.num_nodes / 2 - num_reds

      if num_blues_left == 0:
          return num_reds_left > 3
      if num_reds_left == 0:
          return num_blues_left > 3

      if num_reds_left > num_blues_left:
          return (num_reds_left - 3) / num_blues_left > 3

      return (num_blues_left - 3) / num_reds_left > 3

  def valid_options(self, path):
      """ Given a path, the list of edges that extend from the endpoints of the graph
      and do not create cycles AND do not violate the max-3-node constraint."""
      #next_valid_colors = ["R", "B"]
      #if len(path) >= 3:
      #   last_three_node_colors = [self.colors[node] for node in path[-3:]]
      #   if last_three_node_colors[0] == last_three_node_colors[1] == last_three_node_colors[2]:
      #       next_valid_colors.remove(last_three_node_colors[0])

      return [edge for edge in self.all_edges if not self.creates_cycle(edge, path) and (path[0] in edge or path[-1] in edge) and self.is_valid_coloring(self.append_edge(path, edge)) and not self.is_last_color(path, edge)] #(self.colors[path[0]] in next_valid_colors or self.colors[path[-1]] in next_valid_colors)]

  # LOOOOOL OMG GET IT?????????????
  # YES SAHIL WE GET IT
  # NO I DONT THINK YOU DO. ITS FUCKING APPENDAGE. APPENDAGE. APPEEEENDDDAGGEE.
  def append_edge(self, path, edge):
      path = path[:]
      new_edge = (edge[0], edge[1])
      left_endpoint, right_endpoint = path[0], path[-1]
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

  # APPROXIMATION ALGORITHMS

  # todo: allow the selection of the first edge to be different or to even be iterative
  def greedy(self, heuristic=BASIC, path=None):
      """ The implementation of the greedy solution without any special stuff """

      # set the default heurisitic if none are provided
      # if heuristic is Graph.BASIC:
      #   heuristic_func = self.general_heuristic
      # elif heuristic is Graph.SMART:
      #   heuristic_func = self.smart_heuristic
      # elif heuristic is Graph.BINOCULARS:
      #   heuristic_func = self.binoculars_heuristic

      heuristic_func = self.get_heuristic(heuristic)

      cheapest_path = None

      # choose the first edge just as the cheapest one in the graph
      # FIXME breaks if there are no valid options to consider
      print_path = False
      if path is None:
          path = list(min(self.all_edges, key=lambda edge: self.get_weight(edge[0], edge[1])))
          print_path = True

      while not self.is_valid_hamiltonian(path):
          left_endpoint, right_endpoint = path[0], path[-1]

          # using the passed in heuristic, pass in the path up to that point
          new_edge = heuristic_func(path)[0]

          # add the new edge to the proper side of the path
          new_node = new_edge[0]
          if left_endpoint in new_edge:
              if left_endpoint == new_edge[0]:
                  new_node = new_edge[1]
              path = [new_node] + path
          else:
              if right_endpoint == new_edge[0]:
                  new_node = new_edge[1]
              path = path + [new_node]

          if False and print_path:
              print path

      return path

  def is_valid_coloring(self, path):
      """
          :param: path (array) - the array to do things to
          :return: True if the coloring is valid. False otherwise
      """
      colors = [self.colors[city] for city in path]
      colors_string = ''.join(str(x) for x in colors)

      return "R"*(COLOR_LIMIT+1) not in colors_string and "B"*(COLOR_LIMIT+1) not in colors_string

  # HEURISTICS FOR GREEDY ALGORITHMS

  def general_heuristic(self, path, edges=None):
      edges = edges or self.valid_options(path)
      return sorted(edges, key=lambda edge: self.get_weight(edge[0], edge[1]))

  # more like slightly educated heuristic. like barely high school graduate who enlisted in the marines
  # and served 4 years, left with a honorable discharge, became a carpenter in a quiet suburban neighborhood
  # in the midwest, lived a simple, happy life.
  def smart_heuristic(self, path, edges=None):
      # left_endpoint, right_endpoint = path[0], path[-1]
      # weighter = lambda edge: self.get_weight(edge[0], edge[1])
      # left_weighter = lambda edge: self.f(edge, edge[0] if edge[1] == left_endpoint else edge[1])
      # right_weighter = lambda edge: self.f(edge, edge[0] if edge[1] == right_endpoint else edge[1])
      edges = edges or self.valid_options(path)
      # left_edges = [edge for edge in edges if left_endpoint in edge]
      # right_edges = [edge for edge in edges if right_endpoint in edge]
      # if left_edges and right_edges:
      #   return min([min(left_edges, key=left_weighter), min(right_edges, key=right_weighter)], key=weighter)
      # elif left_edges:
      #   return min(left_edges, key=left_weighter)
      # else:
      #   return min(right_edges, key=right_weighter)

      return sorted(edges, key=lambda edge: self.f_smart(edge, path))

  def binoculars_heuristic(self, path, edges=None):
      edges = edges or self.valid_options(path)
      paths = [self.append_edge(path, edge) for edge in edges]
      best_paths = sorted(paths, key=lambda path: self.path_cost(self.greedy(Graph.BASIC, path)))
      # return edges[paths.index(best_path)]
      return [edges[paths.index(best_path)] for best_path in best_paths]

  def smart_binoculars_heuristic(self, path, edges=None):
    edges = edges or self.valid_options(path)
    paths = [self.append_edge(path, edge) for edge in edges]
    best_paths = sorted(paths, key=lambda path: self.path_cost(self.greedy(Graph.SMART, path)))
    # return edges[paths.index(best_path)]
    return [edges[paths.index(best_path)] for best_path in best_paths]

  # the wisest heuristic of them all
  def guru_heuristic(self, path, edges=None, weights=None):
      heuristics = [Graph.BASIC, Graph.SMART, Graph.BINOCULARS]
      weights = weights or [0.5, 0.2, 2]
      edges = edges or self.valid_options(path)
      scores = dict((edge, 0) for edge in edges)
      prizes = list(map(lambda a: a**3, list(range(0, len(edges)))))[::-1]
      # unweighted
      for graph in [self, self.reweight()]:
          for h_index, heuristic in enumerate(heuristics):
              heuristic_func = graph.get_heuristic(heuristic)
              rankings = heuristic_func(path, edges)
              for index, edge in enumerate(rankings):
                  scores[edge] += prizes[index] * weights[h_index]
      best_score = max(scores.values())
      best_edges = [edge for edge in edges if scores[edge] == best_score]
      return best_edges

  # dont consult this one
  def stubborn_heuristic(self, path, edges=None):
      return "No"

  # TOOLS USED IN HEURISTICS

  # --- tools for smart greedy

  def family(self, node):
      return [edge for edge in self.all_edges if node in edge]

  def avg(self, node):
      edge_weight = lambda edge: self.get_weight(edge[0], edge[1])
      edges = self.family(node)
      return sum([edge_weight(edge) for edge in edges])/float(len(edges))

  def f(self, edge, node):
    a = self.avg(node)
    a = a if a > 0 else 1
    return self.get_weight(edge[0], edge[1])/a

  def true_weight(self, edge):
      return self.get_weight(edge[0], edge[1])*(self.f(edge, edge[0]) + self.f(edge, edge[1]))

  def f_smart(self, edge, path):
      return self.f(edge, edge[0]) if edge[0] not in path else self.f(edge, edge[1])

  # TRANSFORMATIONS

  def duplicate(self):
      return Graph(self.file)

  def reweight(self):
      graph2 = self.duplicate()
      for edge in graph2.all_edges:
          graph2.set_weight(self.true_weight(edge), edge[0], edge[1])
      return graph2

  # COMPARISONS BETWEEN GRAPHS

  def cost_comparison(self, other_graph=None):
      if other_graph is None:
          other_graph = self.reweight()
      return self.path_cost(self.greedy()) - self.path_cost(other_graph.greedy())

  def is_same(self, other_graph):
      for edge in self.all_edges:
          if self.get_weight(edge[0], edge[1]) != other_graph.get_weight(edge[0], edge[1]):
              return False
      return True

  # GENERAL TOOLS

  def weights_of_path(self, path):
      return [self.get_weight(edge[0], edge[1]) for edge in zip(path[:-1], path[1:])]

  def best_cost(self):
      return self.path_cost(self.tsp_naive())

  def tsp_naive(self):
      good_paths = list(filter(lambda lst: self.is_valid_hamiltonian(lst), permutations(list(range(0, self.num_nodes)))))
      return min(good_paths, key=lambda lst: self.path_cost(lst))

  def get_heuristic(self, heuristic):

    if heuristic is Graph.BASIC:
      heuristic_func = self.general_heuristic
    elif heuristic is Graph.SMART:
      heuristic_func = self.smart_heuristic
    elif heuristic is Graph.BINOCULARS:
      heuristic_func = self.binoculars_heuristic
    elif heuristic is Graph.GURU:
      heuristic_func = self.guru_heuristic
    elif heuristic is Graph.STUBBORN:
      heuristic_func = self.stubborn_heuristic
    elif heuristic is Graph.SMART_BINOCULARS:
      heuristic_func = self.smart_binoculars_heuristic

    return heuristic_func

  # DEPRECATED

  # returns a greedy solution
  def old_greedy(self):
      """ The implementation of the greedy solution without any special stuff """
      weighter = lambda edge: self.get_weight(edge[0], edge[1])
      path = list(min(self.all_edges, key=weighter))
      while not self.is_valid_hamiltonian(path):
          left_endpoint, right_endpoint = path[0], path[-1]
          new_edge = min(self.valid_options(path), key=weighter)
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

  def smart_greedy(self):
      weighter = lambda edge: self.get_weight(edge[0], edge[1])
      new_weighter = lambda edge, node: self.f(edge, edge[0] if edge[1] == node else edge[1])
      path = list(min(self.all_edges, key=weighter))
      while not self.is_valid_hamiltonian(path):
          left_endpoint, right_endpoint = path[0], path[-1]
          left_weighter = lambda edge: self.f(edge, edge[0] if edge[1] == left_endpoint else edge[1])
          right_weighter = lambda edge: self.f(edge, edge[0] if edge[1] == right_endpoint else edge[1])
          options = self.valid_options(path)
          left_edges = [edge for edge in options if left_endpoint in edge]
          right_edges = [edge for edge in options if right_endpoint in edge]
          new_edge = min([min(left_edges, key=left_weighter), min(right_edges, key=right_weighter)], key=weighter)
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

# other functions

def run_to_convergence(graph):
    graph2 = graph.reweight()
    i = 1
    while not graph2.is_same(graph2.reweight()):
        print i
        graph2 = graph2.reweight()
        i += 1
    return graph2

def permutations(lst):
    if len(lst) < 2:
        return [lst]
    perms_found = []
    for index, element in enumerate(lst):
        rest = lst[:index] + lst[index+1:]
        perms = permutations(rest)
        for perm in perms:
            perms_found.append([element] + perm)
    return perms_found
    #return [[element] + perm for perm in permutations(lst[:lst.index(element)] + lst[lst.index(element)+1:]) for element in lst]

