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
from tqdm import tqdm

def fast_print(text):
    sys.stdout.write(str(text) + "\n")
    sys.stdout.flush()

xs = [x for x in np.arange(1,10,2)]

ys = np.arange(1,5,1)

gi.set_parameters({
                                        'a': 0,
                                        'p': 0,
                                        't': 1,
                                        'generations': 3,
                                        'tests': 100
                                    })

patches = []
colors = ['b','g','r','c','m','y','k','w']

# for 2d graph with multiple lines
counter = 0
for y in tqdm(ys):
    zs = [gi.D_value(x,y) for x in xs]
    plt.plot(xs,zs,color=colors[counter])
    patches.append(mpatches.Patch(color=colors[counter],label=str(y)))
    counter += 1

plt.legend(title='trait ratio', handles=patches, loc='lower right')

plt.show()

sys.exit()