import unittest
import numpy as np
from graph import Graph
import os

TEST_PATH = os.path.dirname(os.path.abspath(__file__)) + '/test_inputs/'

class TestGraph(unittest.TestCase):

    def _check(self, actual, expected):
        np.testing.assert_allclose(actual, expected)

    def test_red_and_blue(self):
        graph = Graph(open(TEST_PATH + 'four_nodes.in').read())
        
        self._check(graph.is_blue(0), True)
        self._check(graph.is_red(0), False)

        self._check(graph.is_blue(1), True)
        self._check(graph.is_red(1), False)

        self._check(graph.is_blue(2), False)
        self._check(graph.is_red(2), True)

        self._check(graph.is_blue(3), False)
        self._check(graph.is_red(3), True)