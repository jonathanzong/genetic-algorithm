# explanation found at http://jonathanzong.com/blog/2013/07/08/optimizing-top-choices-with-genetic-algorithm

import random, math
from copy import deepcopy
from sys import maxint

class Student:
	def __init__(self, name, choices):
		self.name = name
		self.choices = choices

	def get_rank(self, choice):
		return self.choices.index(choice)

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		return self.name == other.name

	def __repr__(self):
		return self.name

# configure
n = 13
k = 12

choice_set = []
student_set = []

# populate choice_set with choice names
for x in range(n):
	choice_set.append('Choice '+str(x+1))

# populate student_set with student names and a randomly permuted list of choices
for x in range(k):
	student_set.append(Student(chr(x+65), random.sample(choice_set,n)))

# sum the indices of the choices assigned to a student
# penalize additionally by highest index, for fairness
def cost_function(assignments):
	#cost = sum_indices(assignments)
	cost = 0
	max_index = 0
	for student in student_set:
		choice = assignments[student]
		index = student.get_rank(choice)
		cost += index
		if index > max_index:
			max_index = index
	return cost + index

def seed_ga(g_size):
	# randomly generate seed generation by shuffling
	# choices and assigning them to students in order
	generation = []
	for x in range(g_size):
		random.shuffle(choice_set)
		assignment = {}
		for i in range(k):
			assignment[student_set[i]] = choice_set[i]
		generation.append(assignment)
	return generation

def genetic_algo(generation, n_iter):
	g_size = len(generation)
	# iterate the GA n_iter number of times and return best solution
	for x in range(n_iter):
		# sort generation by ascending cost
		generation.sort(key=lambda x: cost_function(x))
		# keep the top half (best solutions move onto the next generation)
		# mutate the best solutions by introducing random swaps in assignment
		generation[g_size/2:] = deepcopy(generation[:g_size/2])
		for candidate in generation[g_size/2 : g_size]:
			swaps = random.sample(student_set,2)
			temp = candidate[swaps[0]]
			candidate[swaps[0]] = candidate[swaps[1]]
			candidate[swaps[1]] = temp
	return generation[0]

# run GA multiple times to combat convergence to local optima
best_score = maxint
best_assignment = None
for x in range(10):
	generation = seed_ga(10)
	res = genetic_algo(generation,100)
	cost = cost_function(res)
	print 'Cost: ', cost
	if cost < best_score:
		best_score = cost
		best_assignment = res

print 'Best solution: ', best_assignment
print 'Minimized Cost: ', best_score
for key in best_assignment:
	print key, ' got index ', key.get_rank(best_assignment[key])
