import graph
import break_triangle_ineq
import random

# TODO force greedy algorithm to pick shitty edge because of 3-node constraint

def break_greedy(n):
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
  # pick a random node to have slightly more attractive edges
  rand_node1 = 0
  while rand_node1==start_node or rand_node1==end_node:
    rand_node1 = random.choice(range(n))
  graph.set_weight(25, rand_node1, start_node)
  rand_node2 = 1
  while rand_node2==start_node or rand_node2==end_node:
    rand_node2 = random.choice(range(n))
  graph.set_weight(25, rand_node2, start_node)

  # make all other nodes going out of start look really bad
  for other_node in range(n):
    if start_node != other_node and other_node != rand_node1:
      graph.set_weight(50, other_node, start_node)
  # make all other nodes going out of end look really bad
  for other_node in range(n):
    if end_node != other_node and other_node != rand_node2:
      graph.set_weight(50, other_node, end_node)
  # make edges along the path bad
  for u, v in zip(rand_path[:-1], rand_path[1:]):
    graph.set_weight(0, u, v)
  graph.set_weight(100, rand_path[-1], rand_path[-2])
  return graph