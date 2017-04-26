# number of patents that have each trait
# take integral of ratios vs time up to a time t_f (in generations)
# this will be the "selection speed" of a genealogy

import genealogy
import matplotlib.pyplot as plt
import numpy as np
import pickle
from tqdm import tqdm
from scipy import optimize


parents = 1
ratio = 1
tests = 4
power = 1
balanced = True
initial_counts = None
generations = 50
generations_sizes = 16
a = 1
p = 1
t = 1

percentsdatafile = "outputs/ratios/percentsdata/"
testresultsfile = "outputs/testresults/"

def read_percentsdata(parents,ratio):
    with open(percentsdatafile + 'percents(parents=' + str(parents) + ',ratio=' + str(ratio) + ').list', 'rb+') as datafile:
            return pickle.load(datafile)

def write_percentsdata(parents,ratio,results):
    with open(percentsdatafile + 'percents(parents=' + str(parents) + ',ratio=' + str(ratio) + ').list', 'wb+') as datafile:
        pickle.dump(results, datafile, pickle.HIGHEST_PROTOCOL)

def read_testresult(name):
    with open(testresultsfile + name + '.trs', 'rb+') as datafile:
        return pickle.load(datafile)

def write_testresult(name,results):
    with open(testresultsfile + name + '.trs', 'wb+') as datafile:
        pickle.dump(results, datafile, pickle.HIGHEST_PROTOCOL)  

def set_parameters(params):
    global tests, ratio, parents, power, generations, generations_sizes, a, p, t, initial_counts, balanced
    if 'tests' in params:
        tests = params['tests']
    if 'ratio' in params:
        ratio = params['ratio']
    if 'parents' in params:
        parents = params['parents']
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
    if 'initial_counts' in params:
        initial_counts = params['initial_counts']
    if 'balanced' in params:
        balanced = params['balanced']

def reset_parameters():
    global tests, power, generations, generations_sizes, a, p, t
    tests = 4
    power = 1
    generations = 50
    generations_sizes = 16
    a = 1
    p = 1
    t = 1

def generation_sizes_function(gen_ind):
    return generations_sizes

def make_inspector_genealogy():

    genealogy.init_genealogy()

    genealogy.make_genealogy(
            generations=generations,
            parents=parents,
            generation_sizes_function=generation_sizes_function,
            balanced=balanced,
            initial_counts=initial_counts,
            age_factor=a,
            popular_factor=p,
            trait_factor=t,
            trait_weights=[ratio,1]
        )


def get_percents():
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

def plot_percents(parents,ratio,tests):

    results = calc_smoothed_percents(parents,ratio,tests)

    plt.title("Percentage of population that is dominant trait")#\n(parents=" + str(parents) + ",ratio=" + str(ratio) + ")")
    plt.xlabel('Generation')
    plt.ylabel('Percentage Red')

    xs = [x for x in range(len(results))]

    plt.plot(xs, results, 'o', label='ratio=' + str(ratio))

def legend():
    plt.legend()

def savefig(name):
    plt.savefig(name)

def plot_log_regressions(parents, ratio_range):
    for ratio in ratio_range:
        # data is list of percents
        data = read_percentsdata(parents,ratio)

        x = [x for x in range(1,len(data))]
        y = data[1:]

        fit = np.polyfit(np.log(x), y, 1)
        def fit_fn(x):
            return fit[0]*np.log(x)+fit[1]

        x = np.arange(min(x),max(x),0.1)
        y = [fit_fn(xi) for xi in x]

        plt.plot(x,y,'k')

def calc_log_regressions(parents, ratio_range):
    results = []
    for ratio in ratio_range:
        # data is list of percents
        data = read_percentsdata(parents,ratio)

        x = [x for x in range(1,len(data))]
        y = data[1:]

        fit = np.polyfit(np.log(x), y, 1)
        def fit_fn(x):
            return fit[0]*np.log(x)+fit[1]

        results.append(fit_fn)

    return results

def plot_exp_regressions(parents, ratio_range):
    for ratio in ratio_range:
        # data is list of percents
        data = read_percentsdata(parents,ratio)

        x = [x for x in range(0,len(data))]
        y = [x - 1 for x in data] # want the max of the exp function to be 0

        # fit = np.polyfit(x, np.log(y), 1, w=np.sqrt(y))

        fit = optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+c,  x,  y,  p0=(-1,-0.1,0))
        fit = fit[0]
        print(fit)

        def fit_fn(x):
            return fit[0] * np.exp(fit[1]*x) + fit[2]

        x = np.arange(min(x),max(x),0.1)
        y = [fit_fn(xi)+1 for xi in x] # add the one back in

        plt.plot(x,y,'k')

def calc_exp_regressions(parents, ratio_range):
    for ratio in ratio_range:
        # data is list of percents
        data = read_percentsdata(parents,ratio)

        x = [x for x in range(0,len(data))]
        y = [x - 1 for x in data] # want the max of the exp function to be 0

        # fit = np.polyfit(x, np.log(y), 1, w=np.sqrt(y))

        fit = optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+c,  x,  y,  p0=(-1,-0.1,0))
        fit = fit[0]
        print(fit)

        def fit_fn(x):
            return fit[0] * np.exp(fit[1]*x) + fit[2]

        x = np.arange(min(x),max(x),0.1)
        y = [fit_fn(xi)+1 for xi in x] # add the one back in

        plt.plot(x,y,'k')

def calc_smoothed_percents(parents,ratio,tests):
    # graph percents vs generation num

    set_parameters({'parents': parents, 'ratio': ratio})

    # store all the calculated percents for each test
    percents = []

    for i in tqdm(range(tests)):
        make_inspector_genealogy()

        percents.append(get_percents())

    results = [[] for x in range(len(percents[0]))]

    # i is the index of the list
    for i in range(len(percents)):
        # j is the index of the generation
        for j in range(len(percents[i])):
            results[j].append(percents[i][j])

    for i in range(len(results)):
        results[i] = np.mean(results[i])

    # save results to appropriate file:
    write_percentsdata(parents,ratio,results)

    return results

def S_value(parents,ratio):
    set_parameters({'parents': parents, 'ratio': ratio})

    results = []

    for i in range(tests):

        make_inspector_genealogy()

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


def deriv50_value(parents,ratio):

    set_parameters({'parents': parents,'ratio': ratio})

    results = []

    for i in range(tests):

        make_inspector_genealogy()

        results.append(inspect_deriv50())

    return (np.mean(results))**power

def deriv50_value():

    percents = get_percents()

    # deriv50 = ()