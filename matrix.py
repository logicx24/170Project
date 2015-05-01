import random
import numpy as np


def generate_matrix(n):
    """Generate n * n matrix thing"""
    return [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]


def sanitize(n, matrix):
    # add zeros
    for i in range(n):
        matrix[i][i] = 0
    # transpose
    for i in range(n):
        for j in range(i, n):
            matrix[j][i] = matrix[i][j]
    return matrix

COLORS = ["R", "B"]

def generate_random_coloring(n):
    red = np.array(["R"] * (n / 2))
    blue = np.array(["B"] * (n / 2))
    lst = np.append(red, blue)
    np.random.shuffle(lst)
    return lst

def print_matrix(n, matrix, c):
    output = "\n".join([" ".join([str(i) for i in row]) for row in matrix])
    open("{0}.in".format(c), 'w').write(
        str(n) + "\n" + output + "\n" + "".join(generate_random_coloring(n)))

for i in range(1, 4):
    n = 6
    matrix = generate_matrix(n)
    matrix = sanitize(n, matrix)
    print_matrix(n, matrix, i)
