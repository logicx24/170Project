import unittest
import numpy as np
from graph import Graph
from dynamic_programming import dynamicSolver
import os

TEST_PATH = os.path.dirname(os.path.abspath(__file__)) + '/test_inputs/'

class TestDotFinder(unittest.TestCase):

    def _check(self, actual, expected):
        np.testing.assert_allclose(actual, expected)

    def test_simple(self):

        graph = Graph(open(TEST_PATH + 'simple.in').read())
        actual_path, actual_dist = dynamicSolver(graph)

        expected_path = [2, 0, 1]
        expected_dist = 128.0

        self._check(actual_path, expected_path)
        self._check(actual_dist, expected_dist)

    def test_four_nodes(self):

		graph = Graph(open(TEST_PATH + 'four_nodes.in').read())
		actual_path, actual_dist = dynamicSolver(graph)

		expected_path = [2, 3, 1, 0]
		expected_dist = 102.0
		
		self._check(actual_path, expected_path)
		self._check(actual_dist, expected_dist)    	
