import genealogy
import dot_creator
import genealogy_inspector
import numpy as np
import sys
import time
import file_manager
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from tqdm import tqdm

def generation_sizes_function(gen_ind):
    return 16

def fast_print(text):
    sys.stdout.write(str(text) + "\n")
    sys.stdout.flush()

"""
Goal:
- create 5x5 matrix with axes being:
    color weight ratio (1, 1.75, 1.5, 2, 4)
    number of parents (1, 2, 4, 8, 16)
"""

# vector in form (parents,color_weight,S)
# output = file_manager.FileManager("outputs","result_surface.txt")
# output_string = "{"

a = 0
p = 0
t = 1

power = 2

def get_S(parents,ratio):

    results = []

    # gets average of 4 tests
    for i in range(12):

        genealogy.init_genealogy()

        genealogy.make_genealogy(
                generations=40,
                parents=parents,
                generation_sizes_function=generation_sizes_function,
                balanced=True,
                age_factor=a,
                popular_factor=p,
                trait_factor=t,
                trait_weights=[ratio,1]
            )

        results.append(genealogy_inspector.inspect_S())

    return (np.mean(results))**power

xs = [x for x in range(1,17)]

ys = np.arange(1,5,0.5)
# ys = [1,1.5,2,2,5,3,3.5,4,4.5]

# for 2d graph with multiple lines
for y in tqdm(ys):
    zs = [get_S(x,y) for x in xs]
    plt.plot(xs,zs)

plt.legend(["r=" + str(y) for y in ys], 'lower right')

plt.show()

# for 3d surface:

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# X, Y = np.meshgrid(xs, ys)

# zs = []
# total = 0
# for x,y in zip(np.ravel(X), np.ravel(Y)):
#     total += 1
# fast_print("total:" + str(total))
# count = 1
# start_time = 0
# for x,y in zip(np.ravel(X), np.ravel(Y)):
#     if count == 1:
#         start_time = time.time()
#     elif count == len(xs):
#         dt = time.time() - start_time
#         print("estimated time: " + str((dt * len(ys))//60) + " minutes")
#     zs.append(get_S(x,y))
#     fast_print(count)
#     count += 1

# zs = np.array(zs)

# Z = zs.reshape(X.shape)

# ax.plot_surface(X, Y, Z)
# # ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

# ax.set_xlabel('parents per member')
# ax.set_ylabel('trait ratio to the' + str(power) + ' power')
# ax.set_zlabel('S')

# plt.show()
# plt.savefig("outputs/S_surface.png")



## Create DOT

# genealogy.init_genealogy()

# G = genealogy.make_genealogy(
#                 generations=100,
#                 parents=1,
#                 generation_sizes_function=generation_sizes_function,
#                 balanced=True,
#                 age_factor=0,
#                 popular_factor=0,
#                 trait_factor=1
#             )

# dot_creator.create_dot(G)