import genealogy_multitraits as genealogy
import dot_creator
import genealogy_multitraits_inspector as gi
import numpy as np
import sys
import time
import file_manager
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# tests, parents, generations, generations_sizes, a, p, t, traits

parents_range = [1,2,3]

gi.set_parameters({
	'tests': 100,
	'generations': 10,
	'generations_sizes': 100,
	'a': 1,
	'p': 1,
	't': 1,
	'traits': [2,3,3],
	'target': [1,1,1],
	'traits_function': 'prod'
})

gi.calc_smoothed_percents_range(parents_range)
gi.plot_percents_range(parents_range)
gi.savefig("outputs/parents/multitrait/MultitraitPercents_magnified+_prod.png")

# gi.set_parameters({
# 	'traits_function': 'prod'
# })

# gi.calc_smoothed_percents_range(parents_range)
# gi.plot_percents_range(parents_range)
# gi.savefig("outputs/parents/multitrait/MultitraitPercents_Prod.png")
