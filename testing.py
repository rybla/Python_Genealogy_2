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

generations = 80
generations_sizes = 20

def test_ratio(parents,ratio,tests):
    gi.set_parameters({
                        'a': 0,
                        'p': 0,
                        't': 1,
                        'generations': generations,
                        'generations_sizes': generations_sizes
                    })

    gi.plot_percents(parents,ratio,tests)

def test_ratios(parents_range,ratio_range,tests):
    gi.set_parameters({
                        'a': 0,
                        'p': 0,
                        't': 1,
                        'generations': generations,
                        'generations_sizes': generations_sizes
                    })

    for p in parents_range:
        for r in ratio_range:
            test_ratio(p,r,tests)

    gi.savefig("outputs/ratios/traittakeover.png")

def test_ratios_rising(parents, ratio_range, tests):
    gi.set_parameters({
                        'a': 0,
                        'p': 0,
                        't': 1,
                        'balanced': False,
                        'initial_counts': [1,19],
                        'generations': generations,
                        'generations_sizes': generations_sizes
                    })

    for r in ratio_range:
        test_ratio(parents,r,tests)

    # gi.plot_log_regressions(parents,ratio_range)
    gi.plot_exp_regressions(parents,ratio_range)

    gi.legend()

    gi.savefig('outputs/ratios/trait_takeover_rising(parents=' + str(parents) + ').png')


def test_parents_and_ratios():
    xs = [x for x in np.arange(1,10,2)]

    ys = np.arange(1,5,1)

    gi.set_parameters({
                        'a': 0,
                        'p': 0,
                        't': 1,
                        'generations': generations,
                        'tests': 200
                    })

    patches = []
    colors = ['b','g','r','c','m','y','k','w']

    # for 2d graph with multiple lines
    counter = 0
    for y in ys:
        zs = [gi.S_value(x,y) for x in xs]
        plt.plot(xs,zs,color=colors[counter])
        patches.append(mpatches.Patch(color=colors[counter],label=str(y)))
        counter += 1

    plt.legend(title='trait ratio', handles=patches, loc='lower right')

    plt.savefig("S_values(tests=200)")

    sys.exit()