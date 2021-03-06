import graph as gr
import random
import numpy as np 


def kruskalsSolver(graph):

    best_path = None
    best_cost = float("inf")

    for i in range(gr.COLOR_LIMIT):
        subtr = i
        path, cost = kruskalsSolverHelper(graph, subtr)

        if graph.is_valid_hamiltonian(path):
            if cost < best_cost:
                best_path = path
                best_cost = cost

    return best_path, best_cost
    # return None

def kruskalsSolverHelper(graph, subtr):
    n = graph.num_nodes
    sorted_edges = graph.get_sorted_edges()
    path_graph = graph.copy_empty()

    # create the disjoint sets Data Structure
    union_find = CDisjointSets()
    for node in range(n):
        union_find.MakeSet(node)

    count = 0
    for edge in sorted_edges:
        
        u, v = edge

        # add in the edge
        weight = graph.get_weight(u, v)
        path_graph.add_edge(weight, u, v)

        # if we're about to create a cycle, we don't add the edge
        if union_find.FindLabel(u) == union_find.FindLabel(v):
            path_graph.remove_edge(u, v)
            continue

        # if the edge is going to create a fork, we don't add the edge
        if not no_forks_found(path_graph, edge):
            path_graph.remove_edge(u, v)
            continue

        # Note: at this point we are guaranteed to have an acyclic path.
        # now, we check to see if that there are no RRRR and BBBB instances
        if not new_coloring_is_valid(path_graph, edge):
            path_graph.remove_edge(u, v)
            continue

        if not check_remaining_color_ratio(path_graph, subtr):
            path_graph.remove_edge(u, v)
            continue

        count += 1
        # No cycles. Guaranteed a path. And colors work. Now we add the edge.
        union_find.Join(u, v)

    # recovering a path
    endpoint = None
    for node in range(n):
        if path_graph.get_degree(node) == 1:
            endpoint = node
            break

    path = [endpoint]

    new_path_graph = graph.copy_empty()
    for edge in path_graph.all_edges:
        u, v = edge
        weight = graph.get_weight(u, v)
        new_path_graph.add_edge(weight, u, v)

    # go back from u
    visited = set()
    curr = endpoint
    prev = None
    while curr not in visited:
        next_u_lst = new_path_graph.get_neighbors(curr)
        if prev != None:
            next_u_lst.remove(prev)

        if len(next_u_lst) > 0:
            next_u = next_u_lst[0]

        path.append(next_u)
        prev = curr
        curr = next_u
        visited = visited.union({prev})


    # if graph.is_valid_hamiltonian()
    return path[:-1], new_path_graph.path_cost(path[:-1])

def new_coloring_is_valid(graph, edge_added):
    
    u, v = edge_added
    # # if the edge you added has nodes of differing colors, you're good.
    if graph.get_color(u) != graph.get_color(v):
        return True
    
    # color = graph.get_color(u)
    path = [u, v]

    # go back from u
    count = 0
    curr = u
    prev = v
    while count < gr.COLOR_LIMIT + 1:
        next_u_lst = graph.get_neighbors(curr)
        next_u_lst.remove(prev)
        if len(next_u_lst) != 0:
            next_u = next_u_lst[0]
        else:
            break
        path.insert(0, next_u)
        prev = curr
        curr = next_u
        count += 1

    count = 0
    curr = v
    prev = u
    while count < gr.COLOR_LIMIT + 1:
        next_v_lst = graph.get_neighbors(curr)
        next_v_lst.remove(prev)
        if len(next_v_lst) != 0:
            next_v = next_v_lst[0]
        else:
            break
        prev = curr
        path.append(next_v)
        curr = next_v
        count += 1

    return graph.is_valid_coloring(path)


def no_forks_found(graph, edge_added):
    return graph.get_degree(edge_added[0]) <= 2 and graph.get_degree(edge_added[1]) <= 2 

def same_color_neighbors_path_from_end_node(graph, end_node):

    color = graph.get_color(end_node)

    count = 0
    prev = None
    curr = end_node
    while True:
        next_neighbors = graph.get_neighbors(curr)
        if prev != None:
            next_neighbors.remove(prev)
        if len(next_neighbors) != 0:
            next_neigh = next_neighbors[0]
        else:
            break

        if graph.get_color(next_neigh) == color:
            count += 1
        else:
            return count

        prev = curr
        curr = next_neigh


def check_remaining_color_ratio(graph, subtr):
    reds, blues, total = 0, 0, 0
    for node in range(graph.num_nodes):
        degree = graph.get_degree(node)
        if degree == 0 or (degree == 1 and same_color_neighbors_path_from_end_node(graph, node) == gr.COLOR_LIMIT):
            total += 1
            if graph.is_red(node):
                reds += 1
            else:
                blues += 1

    if subtr == gr.COLOR_LIMIT - 1:
        return total <= gr.COLOR_LIMIT or abs(reds - blues) <= 1
    else:
        return total <= gr.COLOR_LIMIT or (reds * (gr.COLOR_LIMIT - subtr) >= blues and blues * (gr.COLOR_LIMIT - subtr) >= reds)


""" Disjoint Sets
    -------------
    Pablo Francisco Perez Hidalgo
    December,2012. 
""" 
class CDisjointSets:
 
    #Class to represent each set
    class DSet:
        def __init__(self, label_value):
            self.__label = label_value
            self.rank = 1
            self.parent = self
        def getLabel(self):
            return self.__label
 
    #CDisjointSets Private attributes
    __sets = None
 
    #CDisjointSets Constructors and public methods.
    def __init__(self):
        self.__sets = {}
 
    def MakeSet(self, label):
        # if label in self.__sets: #This check slows the operation a lot,
        #     return False         #it should be removed if it is sure that
        #                          #two sets with the same label are not goind
        #                          #to be created.
        self.__sets[label] = self.DSet(label)
 
    #Pre: 'labelA' and 'labelB' are labels or existing disjoint sets.
    def Join(self, labelA, labelB):
        a = self.__sets[labelA]
        b = self.__sets[labelB]
        pa = self.Find(a)
        pb = self.Find(b)
        if pa == pb: 
            return #They are already joined
        parent = pa
        child = pb
        if pa.rank < pb.rank:
            parent = pb
            child = pa
        child.parent = parent
        parent.rank = max(parent.rank, child.rank+1)
 
    def Find(self,x):
        if x == x.parent:
            return x
        x.parent = self.Find(x.parent)
        return x.parent
 
    def FindLabel(self, label):
        return self.Find(self.__sets[label])
 
    def __str__(self):
        ret = ""
        for e in self.__sets:
            ret = ret + "parent("+self.__sets[e].getLabel().__str__()+") = "+self.FindLabel(e).parent.getLabel().__str__() + "\n"
        return ret