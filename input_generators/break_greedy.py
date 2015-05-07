import graph
import break_triangle_ineq
import random

# TODO force greedy algorithm to pick shitty edge because of 3-node constraint
# TODO hand-tune the example to force path into shitty edge why not -_-

def break_greedy(n, random_path=True, shuffle_colors=False):
  colors = (["R", "B"] * (n/2))[:]
  graph = break_triangle_ineq.CoordGraph(n) # all weights are currently -1
  graph.colors = colors
  for node1 in range(n):
    for node2 in range(node1+1, n):
      graph.set_weight(1, node1, node2)

  rand_path = []

  if random_path:
    red_nodes = range(n)[::2]
    blue_nodes = range(n)[1::2]
    random.shuffle(red_nodes)
    random.shuffle(blue_nodes)
    rand_path = [val for pair in zip(red_nodes, blue_nodes) for val in pair]
  else:
    rand_path = range(n)

  start_node = rand_path[0]
  end_node = rand_path[-1]

  # pick a random node to have slightly more attractive edges
  # TODO not sure what's so great about this
  rand_node1 = 0
  while rand_node1==start_node or rand_node1==end_node:
    rand_node1 = random.choice(range(n))
  graph.set_weight(25, rand_node1, start_node)
  rand_node2 = 1
  while rand_node2==start_node or rand_node2==end_node:
    rand_node2 = random.choice(range(n))
  graph.set_weight(25, rand_node2, end_node)

  # set edge weights to 0 along this nice path
  for u, v in zip(rand_path[:-1], rand_path[1:]):
    graph.set_weight(0, u, v)
  # make all other nodes going out of start look really bad
  for other_node in range(n):
    if start_node != other_node and other_node != rand_node1:
      graph.set_weight(50, other_node, start_node)
  # make all other nodes going out of end look really bad
  for other_node in range(n):
    if end_node != other_node and other_node != rand_node2:
      graph.set_weight(50, other_node, end_node)
  # make last edge along the path really bad
  graph.set_weight(100, rand_path[-1], rand_path[-2])

  if shuffle_colors:
    random.shuffle(graph.colors)

  return graph

def break_kruskal(n=50):
  colors = (["B", "B", "B", "R", "R", "R"] * int(n/3))[:48] + ["R", "B"]
  graph = break_triangle_ineq.CoordGraph(n) # all weights are currently -1
  graph.colors = colors

  intended_path = range(n)

  # red_nodes = []
  # blue_nodes = []
  # for i in range(n)[::6]:
  #   red_nodes += [i, i+1, i+2]
  #   blue_nodes += [i+3, i+4, i+5]
  # red_nodes = [i for i in red_nodes if i <= 49]
  # blue_nodes = [i for i in blue_nodes if i <= 49]
  # blue_nodes += [49]

  red_nodes = [r for r in intended_path if colors[r]=="R"]
  blue_nodes = [b for b in intended_path if colors[b]=="B"]

  # for tier in range(n/6)[::3]:
  #   for r in red_nodes:
  #     if r+1 <= 49: graph.set_weight(tier, r, r+1)
  # for tier in range(n/6)[::3]:
  #   for b in blue_nodes:
  #     if b+1 <= 49: graph.set_weight(tier+1, b, b+1)

  # weight_counter = 0
  # for node1 in range(len(red_nodes)):
  #   for node2 in range(node1+1, len(red_nodes)):
  #     graph.set_weight(weight_counter, red_nodes[node1], red_nodes[node2])
  #     weight_counter += 1

  # weight_counter = 0
  # for node1 in range(len(blue_nodes)):
  #   for node2 in range(node1+1, len(blue_nodes)):
  #     graph.set_weight(weight_counter, blue_nodes[node1], blue_nodes[node2])
  #     weight_counter += 1

  for node1 in range(n):
    for node2 in range(node1+1, n):
      graph.set_weight(random.randint(5, 20), node1, node2)

  graph.set_weight(0, 0, 1)
  graph.set_weight(2, 1, 2)
  graph.set_weight(3, 2, 3)
  graph.set_weight(1, 1, 49)
  for blue_node in blue_nodes:
    if blue_node != 49 and blue_node != 1:
      graph.set_weight(100, 49, blue_node)


  # fucked_nodes = [n-1 for n in intended_path[::3]]
  # for node in fucked_nodes:
  #   this_color = graph.colors[node]
  #   opp_color = [x for x in intended_path if x > node and graph.colors[x] != this_color]
  #   for opp in opp_color:
  #     graph.set_weight(100, node, opp)
  #   graph.set_weight(99, node, node+1)

  # for node1 in range(n):
  #   for node2 in range(node1+1, n):
  #     if graph.get_weight(node1, node2) == -1:
  #       graph.set_weight(4, node1, node2)

  return graph












