# 170Project - NPTSP

Project for 170

Our approximate solution to the Non Partisan Traveling Salesman Problem, described at follows:

In the Traveling Salesman Problem we are given a graph with edge weights, and are asked to find the best TSP path, that is, overall cheapest route that visits all cities exactly once. (Unlike a tour, a TSP path doesn’t have to return to its start city). In the non-partisan travelling senator problem (NPTSP), each city also has a color, either RED or BLUE, and the path cannot visit more than three cities of the same color consecutively. You still want the cheapest such path that visits every city exactly once. More specifically, you are given a complete, undirected, weighted graph on N cities. The cities are labeled
from 1 to N. The graph is given to you in adjacency matrix format, that is you will recieve an N ×N matrix, where the entry in the ith row and jth column represents the edge weight between city i and city j. You are also given a string of length N representing the colors of the cities. The ith character of the string is R if the city is red, and B otherwise. You may also assume that the number of red and blue cities are exactly the same.
