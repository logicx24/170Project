import graph
import random
import numpy as np 


def kruskals_path(graph):
	n = graph.num_nodes
	sorted_edges = graph.get_sorted_edges()
	path_graph = graph.copy_empty()

    # create the disjoint sets Data Structure
    union_find = CDisjointSets()
    for node in range(n):
        union_find.MakeSet(node)

	for edge in sorted_edges:
        
        u, v = edge

        # if we're about to create a cycle, we don't add the edge
        if union_find.FindLabel(u) == union_find.FindLabel(v):
            continue

        # if the edge is going to create a fork, we don't add the edge
        if not no_forks_found(graph, edge):
            continue

        # Note: at this point we are guaranteed to have an acyclic path.
        # now, we check to see if that there are no RRRR and BBBB instances
        if not new_coloring_is_valid(graph, edge_added):
            continue

        # No cycles. Guaranteed a path. And colors work. Now we add the edge.
        path_graph.add_edge(u, v)
        union_find.Join(u, v)

    # recovering a path
    endpoint = None
    for node in range(n):
        if path_graph.get_degree(node) == 1:
            endpoint = node
            break

    # # if the edge you added has nodes of differing colors, you're good.
    # if graph.get_color(u) != graph.get_color(v):
    #     return True
    
    # color = graph.get_color(u)
    path = [endpoint]

    # go back from u
    curr = endpoint
    prev = None
    while curr:
        next_u_lst = None
        if prev:
            next_u_lst = graph.get_neighbors(curr).remove(prev)
        else:
            next_u_lst = graph.get_neighbors(curr)
        if next_u_lst:
            next_u = next_u_lst[0]
        else:
            break
        path.append(next_u)
        prev = curr
        curr = next_u

    return path

    # for edge in path_graph.get_sorted_edges():


def new_coloring_is_valid(graph, edge_added):
    
    u, v = edge_added
    # # if the edge you added has nodes of differing colors, you're good.
    # if graph.get_color(u) != graph.get_color(v):
    #     return True
    
    # color = graph.get_color(u)
    path = [u, v]

    # go back from u
    count = 0
    curr = u
    prev = v
    while count < COLOR_LIMIT + 1:
        next_u_lst = graph.get_neighbors(curr).remove(prev)
        if next_u_lst:
            next_u = next_u_lst[0]
        else:
            break
        path.insert(next_u, 0)
        prev = curr
        curr = next_u
        count += 1

    # go forward from v 
    count = 0
    curr = v
    prev = u
    while count < COLOR_LIMIT + 1:
        next_v_lst = graph.get_neighbors(curr).remove(prev)
        if next_v_lst:
            next_v = next_v_lst[0]
        else:
            break
        prev = curr
        path.append(next_v)
        curr = next_v
        count += 1

    return graph.is_valid_coloring(path)

    # first explore on the other side of u


def no_forks_found(graph, edge_added):
    return graph.get_degree(edge_added[0]) <= 2 and graph.get_degree(edge_added[1]) <= 2 




""" Disjoint Sets
    -------------
    Pablo Francisco Pérez Hidalgo
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