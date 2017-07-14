import random
import numpy as np
import math
import copy
random.seed()

class GenealogyData:

	def __init__(name):
		self.name = name
		self.history = None


"""

Parameters:

	name

	generation_sizes_function
	fitness_function (age, children, traits[])

	generations
	parents

	age_factor
	popular_factor
	trait_factor

	traits_function
	traits

"""

"""

Member:

	[0]: children count
	[1]: trait values
	[2]: fitness (not including age)

"""

def run(name,
        generations,
        parents,
        generation_sizes_function,
        age_factor,
        popular_factor,
        trait_factor,
        traits,
        traits_function):

	blank_member = [0, [ 0 for i in traits ], 0]
	def blank():
		return copy.deepcopy(blank_member)

	# create blank genealogy
	history = [[blank() for i in generation_sizes_function(g)] for g in range(generations)]

	# fill first generation
	

	# fill subsequent generations