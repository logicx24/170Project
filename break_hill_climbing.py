import graph
import break_triangle_ineq
import random

def break_greedy(n):
  # FIXME this doesn't actually break anything.
  graph = break_triangle_ineq.CoordGraph(n)
  for node1 in range(n):
    for node2 in range(node1+1, n):
      graph.set_weight(random.randint(1, 2), node1, node2)

  rand_path = range(n)
  random.shuffle(rand_path)
  for u, v in zip(rand_path[:-1], rand_path[1:]):
    graph.set_weight(0, u, v)
  graph.set_weight(100, rand_path[-1], rand_path[-2])
  return graph