import unittest
import numpy as np
from graph import Graph
from kruskal_path import kruskalsSolver
import os

TEST_PATH = os.path.dirname(os.path.abspath(__file__)) + '/test_inputs/'


class TestKruskals(unittest.TestCase):

    def _check(self, actual, expected):
        np.testing.assert_allclose(actual, expected)

    def test_four_nodes(self):
        graph = Graph(open(TEST_PATH + 'four_nodes.in').read())
        actual_path, actual_dist = kruskalsSolver(graph)

        expected_path = [0, 1, 3, 2]
        expected_dist = 102.0

        self._check(actual_path, expected_path)
        self._check(actual_dist, expected_dist)

    def test_ten_nodes1_valid_hamiltonian(self):

        graph = Graph(open(TEST_PATH + 'ten_nodes1.in').read())
        actual_path, actual_dist = kruskalsSolver(graph)

        self._check(graph.is_valid_hamiltonian(actual_path), True)

    def test_ten_nodes2_valid_hamiltonian(self):

        graph = Graph(open(TEST_PATH + 'ten_nodes2.in').read())
        actual_path, actual_dist = kruskalsSolver(graph)

        self._check(graph.is_valid_hamiltonian(actual_path), True)

    def test_twelve_nodes1_valid_hamiltonian(self):

        graph = Graph(open(TEST_PATH + 'twelve_nodes1.in').read())
        actual_path, actual_dist = kruskalsSolver(graph)

        self._check(graph.is_valid_coloring(actual_path), True)
