import genealogy
import dot_creator
import numpy as np

def generation_sizes_function(gen_ind):
    return 16


for a in np.arange(2,5,1):
    for p in np.arange(2,4.5,.5):

        genealogy.init_genealogy()

        G = genealogy.make_genealogy(
                generations=15,
                parents=2,
                generation_sizes_function=generation_sizes_function,
                balanced=True,
                age_factor=a,
                popular_factor=p,
                trait_factor=1
            )

        dot_creator.create_dot(G)

# genealogy.init_genealogy()

# G = genealogy.make_genealogy(
#                 generations=15,
#                 parents=2,
#                 generation_sizes_function=generation_sizes_function,
#                 balanced=True,
#                 age_factor=1,
#                 popular_factor=1,
#                 trait_factor=1
#             )

# dot_creator.create_dot(G)