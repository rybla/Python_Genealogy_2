import genealogy
import dot_creator
import genealogy_inspector as gi
import numpy as np
import sys
import time
import file_manager
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

tests = 500
generations = 2
generations_sizes = 100
a = 0
p = 0
t = 1

parents_range = [1,25,50,90]
ratio = 2

ratio_range = range(ratio,ratio+1)

gi.set_parameters({
                    'a': a,
                    'p': p,
                    't': t,
                    'generations': generations,
                    'generations_sizes': generations_sizes,
                    'balanced': True
                })

gi.calc_smoothed_percents_range(parents_range,ratio_range,tests)
# # gi.calc_exp_regressions(parents_range,ratio_range)
gi.calc_first_slopes(parents_range,ratio_range)

gi.initfig()

# gi.plot_d0s_parents(parents_range,ratio,"linear")
gi.plot_first_slopes_parents(parents_range,ratio,"quadratic")

gi.savefig("outputs/parents/parents_test_FS_r2_parents1-90_gensize100_quadratic.png")