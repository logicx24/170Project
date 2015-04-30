import graph
import break_triangle_ineq
import random

def break_greedy(n):
  # FIXME this doesn't actually break anything, because it only produces one really heavy edge.
  # It'll only force a shitty move if the algorithm just happens to go with the random path.
  colors = (["R", "B"] * (n/2))[:]
  graph = break_triangle_ineq.CoordGraph(n) # all weightsare currently -1
  graph.colors = colors
  for node1 in range(n):
    for node2 in range(node1+1, n):
      graph.set_weight(1, node1, node2)

  red_nodes = range(n)[::2]
  blue_nodes = range(n)[1::2]
  random.shuffle(red_nodes)
  random.shuffle(blue_nodes)
  rand_path = [val for pair in zip(red_nodes, blue_nodes) for val in pair]
  start_node = rand_path[0]
  end_node = rand_path[-1]
  for u, v in zip(rand_path[:-1], rand_path[1:]):
    graph.set_weight(0, u, v)
  for other_node in range(n):
    if end_node != other_node:
      graph.set_weight(50, other_node, end_node)
  for other_node in range(n):
    if start_node != other_node:
      graph.set_weight(50, other_node, start_node)
  graph.set_weight(100, rand_path[-1], rand_path[-2])
  return graph