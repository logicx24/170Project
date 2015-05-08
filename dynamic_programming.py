import numpy
import itertools
from graph import Graph, COLOR_LIMIT
import math

def cluster(graph, limit):
    k = graph.num_nodes//limit
    d = {}
    for node in range(graph.num_nodes):
        d[node] = graph.bellman_ford(node)
    ks = []
    for _ in range(k):
        farthestFrom = {}
        remaining = list(range(graph.num_nodes))
        for kd in ks:
            if kd in remaining:
                remaining.remove(kd)
        for remain in remaining:
            for key in d[remain]:
                if key in ks:
                    farthestFrom[key] = 0
                elif key in farthestFrom:
                    farthestFrom[key] += d[remain][key]
                else:
                    farthestFrom[key] = d[remain][key]
        ks.append(max(farthestFrom, key=farthestFrom.get))

    clusters = {k:[] for k in ks}

    for node in range(graph.num_nodes):
        minCluster = ks[0]
        for k in ks:
            if len(clusters[k]) >= limit:
                continue
            num_reds = sum([1 for node in clusters[k] if graph.is_red(node)])
            num_blues = sum([1 for node in clusters[k] if graph.is_blue(node)])
            if graph.is_red(node) and num_reds > 3 and num_reds > 8:
                continue
            if graph.is_blue(node) and num_blues > 3 and num_blues  > 8:
                continue
            minCluster = min([minCluster, k], key=d[node].get)
            if len(clusters[minCluster]) > limit:
                minCluster = k
        clusters[minCluster].append(node)

    return clusters

def cluster_and_solve(graph, cluster_size):
    
    clusters = cluster(graph, cluster_size)
    
    graphs = []
    node_maps = {}
    for key in clusters:
        nodes = clusters[key]
        num_nodes = len(nodes)
        colors_list = [graph.get_color(node) for node in nodes]
        new_graph = Graph(colors_list=colors_list)
        old_to_new = {}
        new_to_old = {}
        count = 0
        for node in nodes:
            old_to_new[node] = count
            new_to_old[count] = node
            count+=1
        for node1 in nodes:
            for node2 in nodes:
                new_graph.add_edge(graph.get_weight(node1, node2), old_to_new[node1], old_to_new[node2])
        graphs.append(new_graph)
        node_maps[new_graph] = old_to_new, new_to_old
    
    paths = {}
    for temp_graph in graphs:
        paths[temp_graph] = dynamicSolver(temp_graph)[0]

    pathing = {}
    for other_graph in paths:
        pathing[other_graph] = [node_maps[other_graph][1][node] for node in paths[other_graph]]            

    flatten = lambda listsOfLists : [item for sublist in listsOfLists for item in sublist]
    return min([flatten(list(tup)) for tup in list(itertools.permutations(pathing.values()))], key=graph.path_cost)


def sort_to_tuple(my_set):
    return tuple(sorted(list(my_set)))

def dynamicSolver(graph):

    n = graph.num_nodes
    best_val = float("inf")
    best_path = None
    for start in range(n):
        path, val = dynamicSolverFromStart(graph, start)
        if val < best_val:
            best_val = val
            best_path = path
    return best_path, best_val

def dynamicSolverParallel(graph):
    import multiprocessing

    q = multiprocessing.Queue()
    def worker(q, starts):
        best_val = float("inf")
        best_path = None
        print(q)
        for start in starts:
            path, val = dynamicSolverFromStart(graph, start)
            if val < best_val:
                best_val = val
                best_path = path
        q.put((best_path, best_val))

    nprocs = multiprocessing.cpu_count()
    procs = []
    starts = list(range(graph.num_nodes))
    chunks = int(math.ceil(len(starts)/float(nprocs)))
    for i in range(nprocs):
        p = multiprocessing.Process(target=worker, args=(q, starts[(chunks*i):(chunks*(i+1))]))
        procs.append(p)
        p.start()

    lst = []
    for i in range(nprocs):
        res = q.get()
        lst.append(res)

    print(lst)

    for p in procs:
        p.join()

    return min(lst, key=lambda x: x[1])

def quickDynamicSolver(graph):
    n = graph.num_nodes
    best_val = float("inf")
    best_path = None

    start_lst = []
    for i in range(n):
        sorted_edges = graph.sorted_edges_through_node(i)
        # print sorted_edges
        diff = sorted_edges[2] - sorted_edges[1]
        tup = (i, diff)
        if len(start_lst) == 5:
            if diff > start_lst[0][1]:
                start_lst[0] = tup
        else:
            start_lst.append(tup)
        start_lst = sorted(start_lst, key=lambda tup:tup[1])

    # print start_lst
    start_lst = [node for node, diff in start_lst]
    print "Running on end nodes: ", ', '.join([str(x) for x in start_lst])
    # return list(range(n)), 10

    for start in start_lst:
        # print "running on start as {0}".format(start)
        path, val = dynamicSolverFromStart(graph, start)
        if val < best_val:
            best_val = val
            best_path = path
    return best_path, best_val

def dynamicSolverFromStart(graph, start):
    n = graph.num_nodes
    all_nodes = set(range(n))

    collection = {}
    if graph.is_red(start):
        collection[((start,), start)] = DynamicNode({start}, red_count=1)
    else:
        collection[((start,), start)] = DynamicNode({start}, blue_count=1)

    for s in range(2, n+1):
        all_nodes_but_one = all_nodes - {start}
        for subset in itertools.combinations(all_nodes_but_one, s-1):
            subset = set(subset).union({start})            # add in the first node to the subset
            collection[(sort_to_tuple(subset), start)] = DynamicNode(subset, value=float("inf"))
            for j in sort_to_tuple(subset):
                if j == start:
                    continue
                else:
                    min_val = float("inf")
                    min_node = None
                    
                    for i in sort_to_tuple(subset):
                        if i != j:
                            val = collection[(sort_to_tuple(subset - {j}), i)].value + graph.get_weight(i, j)
                            node = collection[(sort_to_tuple(subset - {j}), i)]
                            if val < min_val and cond(j, node, graph):
                                min_val = val
                                min_node = node

                    if min_node == None:
                        new_red = 0
                        new_blue = 0
                    else:
                        new_red = min_node.red_count + 1
                        new_blue = min_node.blue_count + 1

                    if graph.is_red(j):
                        collection[(sort_to_tuple(subset), j)] = DynamicNode(subset, value=min_val, prev=min_node, blue_count=0, red_count=new_red)
                        # if collection[(sort_to_tuple(subset), j)].red_count > COLOR_LIMIT: print "VIOLATION RED"
                    else:
                        collection[(sort_to_tuple(subset), j)] = DynamicNode(subset, value=min_val, prev=min_node, blue_count=new_blue, red_count=0)
                        # if collection[(sort_to_tuple(subset), j)].blue_count > COLOR_LIMIT: print "VIOLATION BLUE"


                    new_node = collection[(sort_to_tuple(subset), j)]

                    #### FOR TESTING ONLY ####
                    if new_node.prev != None:
                        vertex_added = list(new_node.node_set - new_node.prev.node_set)[0]

                        # if new_node.prev.red_count == COLOR_LIMIT and graph.get_color(vertex_added) != 'B':
                        #     print "VIOLATION: Added 4th RED"
                        # elif new_node.prev.blue_count == COLOR_LIMIT and graph.get_color(vertex_added) != 'R':
                        #     print "VIOLATION: Added 4th BLUE"

                        # print "ADDED ", graph.get_color(vertex_added), "VERT: ", vertex_added
                        # print "NEW RED: ", new_node.red_count
                        # print "OLD RED: ", new_node.prev.red_count
                        # print "NEW BLUE: ", new_node.blue_count
                        # print "OLD BLUE: ", new_node.prev.blue_count, "\n"

                    ###########################


                    # min_node, min_val = smallest_valued_node([(collection[(sort_to_tuple(subset - {j}), i)], collection[(sort_to_tuple(subset - {j}), i)].value + graph.get_weight(i, j)) for i in sort_to_tuple(subset) if i != j])
                    # collection[(sort_to_tuple(subset), j)] = DynamicNode(subset, value=min_val, prev=min_node)

    min_node, val = smallest_valued_node([(collection[(sort_to_tuple(all_nodes), j)], collection[(sort_to_tuple(all_nodes), j)].value) for j in (all_nodes - {start})])
    return retrace_steps(min_node), val 


def smallest_valued_node(node_lst):
    argmin = node_lst[0][0]
    min_val = node_lst[0][1]

    for node in node_lst[1:]:
        if node[1] < min_val:
            min_val = node[1]
            argmin = node[0]

    return argmin, min_val


def retrace_steps(node):
    ptr = node
    lst = []
    while ptr.prev != None:
        difference = ptr.node_set - ptr.prev.node_set
        lst += list(difference)
        ptr = ptr.prev

    lst += list(ptr.node_set)
    return lst


def cond(vert_number, prev, graph):
    if graph.is_red(vert_number) and prev.nptsp_valid_red():
        return True
    elif graph.is_blue(vert_number) and prev.nptsp_valid_blue():
        return True
    else:
        return False


class DynamicNode():

    def __init__(self, node_set, value=0.0, blue_count=0, red_count=0, prev=None):
        self.value = value
        self.prev = prev
        self.blue_count = blue_count
        self.red_count = red_count
        self.node_set = node_set

    def nptsp_valid_red(self):
        return self.red_count != COLOR_LIMIT

    def nptsp_valid_blue(self):
        return self.blue_count != COLOR_LIMIT

# g = Graph(open('1.in').read())
# print dynamicSolver(g)
