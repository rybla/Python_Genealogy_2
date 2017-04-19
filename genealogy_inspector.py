# number of patents that have each trait
# take integral of ratios vs time up to a time t_f (in generations)
# this will be the "selection speed" of a genealogy

import genealogy
import matplotlib.pyplot as plt
import numpy as np


parents = 1
ratio = 1
tests = 4
power = 1
generations = 50
generations_sizes = 16
a = 1
p = 1
t = 1

def set_parameters(params):
    global tests, power, generations, generations_sizes, a, p, t
    if 'tests' in params:
        tests = params['tests']
    if 'power' in params:
        power = params['power']
    if 'generations' in params:
        generations = params['generations']
    if 'generations_sizes' in params:
        generations_sizes = params['generations_sizes']
    if 'a' in params:
        a = params['a']
    if 'p' in params:
        p = params['p']
    if 't' in params:
        t = params['t']

def reset_parameters():
    global tests, power, generations, generations_sizes, a, p, t
    tests = 4
    power = 1
    generations = 50
    generations_sizes = 16
    a = 1
    p = 1
    t = 1

def make_inspector_geneology():

    def generation_sizes_function(gen_ind):
        return generations_sizes

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


def get_percents():
    # G in form [NAME,GENERATION_COUNTS,MEMBERS]

    # counts (for each trait)
    counts = [0 for t in genealogy.TRAITS]

    # percents (for each generation)
    percents = []

    # calculate percents

    i = 0

    for j in genealogy.GENERATION_COUNTS:

        counts = [0 for count in counts]

        for k in range(j):

            counts[genealogy.get_member_raw_trait(i)] += 1

            i += 1

        # calculate the percentage of generation that is 0
        percents.append( counts[0] / sum(counts) )

    return percents


def S_value(parents,ratio):
    set_parameters({'parents': parents, 'ratio': ratio})

    results = []

    for i in range(tests):

        make_inspector_geneology()

        results.append(inspect_S())

    return (np.mean(results))**power

def inspect_S(graph=False):

    percents = get_percents()

    # integral under percents vs generation
    S = np.trapz(percents) - (0.5 * len(percents)) # minus the expected S's if there was no selection

    if graph:

        plt.title('Percentage Red per Generation (S=' + str(S) + ")")
        plt.xlabel('Generation')
        plt.ylabel('Percentage Red')

        plt.plot([x for x in range(len(percents))], percents)

        plt.savefig("outputs/" + genealogy.NAME + '.png')

    return S

# most useful for 
def D_value(parents,ratio):

    set_parameters({'parents': parents, 'ratio': ratio})

    results = []

    for i in range(tests):

        make_inspector_geneology()

        results.append(inspect_D())

    return (np.mean(results))**power

def inspect_D():

    # slope from first to last generation percentage
    percents = get_percents()

    D = (percents[-1] - percents[0]) / len(percents)

    return D