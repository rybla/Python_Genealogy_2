import genealogy_multitraits as genealogy
# import dot_creator
import genealogy_multitraits_inspector as gi
import numpy as np
import sys
import time
import file_manager
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# tests, parents, generations, generations_sizes, a, p, t, traits

parents_range = range(1,10)

gi.set_parameters({
	'tests': 100,
	'generatiaons': 2,
	'generations_sizes': 100,
	'a': 0,
	'p': 0,
	't': 1,
	'traits': [2,8,32,128,512],
	'target': [1,1,1,1,1],
	'traits_function': 'sum' # prod or sum
})

gi.calc_smoothed_percents_range(parents_range)
gi.calc_first_slopes(parents_range)

gi.initfig()

gi.plot_first_slopes_parents(parents_range,"quadratic")

gi.savefig("outputs/parents/evolutionrate/evolutionrate_parents_sum_traits5_size+.png")