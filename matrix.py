import random
import numpy as np

def gofuckyourself(n):
    """Go fucking fuck yourself

    @param n - the number of vertices
    >>> gofuckyourself()
    "fuck yourself"
    """



def generate_matrix(n):
    """Generate n * n matrix thing"""
    return [[random.randint(1,100) for _ in range(n)] for _ in range(n)]


def sanitize(n, matrix):
    # add zeros
    for i in range(n):
        matrix[i][i] = 0
    # transpose
    for i in range(n):
        for j in range(i,n):
            matrix[j][i] = matrix[i][j]
    return matrix

COLORS = ["R", "B"]

def generate_random_coloring(n):
    return [random.choice(COLORS) for _ in range(n)]

import numpy as np

N = 100
b = np.random.random_integers(-2000,2000,size=(N,N))
b_symm = (b + b.T)/2

def print_matrix(n, matrix, c):
  output = "\n".join([" ".join([str(i) for i in row]) for row in matrix])
  open("{0}.in".format(c),'w').write(str(n) + "\n" + output + "\n" + "".join(generate_random_coloring(n)))

for i in range(1,3):
  n = 50
  matrix = generate_matrix(n)
  matrix = sanitize(n, matrix)
  print_matrix(n, matrix, i)

