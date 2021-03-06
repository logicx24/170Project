import graph
import random
import itertools


def starter_population(graph, num, starter):
	res = []
	for path in itertools.permutations(starter):
		path = list(path)
		if graph.is_valid_hamiltonian_and_seq(path):
			res.append(path)
		if len(res) >= num:
			return res

def crossover1(parent1, parent2):
	first_index = random.randint(0, len(parent1)-1)
	second_index = random.randint(0, len(parent1)-1)

	mindex = min(first_index, second_index)
	maxdex = max(first_index, second_index)

	subsetp1 = parent1[mindex:maxdex+1]
	subsetp2 = parent2[mindex:maxdex+1]

	offspring1 = [0]*len(parent1)
	offspring2 = [0]*len(parent2)

	for i in range(mindex, maxdex+1):
		offspring1[i] = parent2[i]
		offspring2[i] = parent1[i]

	parent1set = parent1[:]
	parent2set = parent2[:]
	for i in range(len(subsetp1)):
		parent1set.remove(subsetp2[i])
		parent2set.remove(subsetp1[i])

	ind = 0
	for i in range(len(parent1set)):
		if ind == mindex:
			ind = maxdex + 1
		if ind < mindex or ind > maxdex:
			offspring1[ind] = parent1set[i]
			offspring2[ind] = parent2set[i]
			ind += 1

	return offspring1, offspring2

def mutation(parent1, mutation_rate):
	for first_index in range(len(parent1)):
		second_index = random.randint(0, len(parent1)-1)
		if random.random() < mutation_rate:
			parent1[first_index], parent1[second_index] = parent1[second_index], parent1[first_index]
	return parent1

def one_away(path):
	splits = [(path[:i], path[i:]) for i in range(len(path) + 1)]
	transposes = [a + [b[1]] + [b[0]] + b[2:] for a, b in splits if len(b)>1]
	#print(transposes)
	return [trans for trans in transposes if graph.is_valid_hamiltonian_and_seq(trans)]

def best_path(path, graph):
	tmp = one_away(path)
	
	two = []
	for e1 in tmp:
		two.extend(one_away(e1))

	three = []
	for e2 in two:
		three.extend(one_away(e2))

	return min(list(tmp + two + three), key=graph.path_cost)





