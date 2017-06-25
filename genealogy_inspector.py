# number of patents that have each trait
# take integral of ratios vs time up to a time t_f (in generations)
# this will be the "selection speed" of a genealogy

import genealogy
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from tqdm import tqdm
from scipy import optimize
import testresults
from testresults import TestResults


parents = 1
ratio = 1
tests = 4
power = 1
balanced = False
initial_counts = [1,19]
generations = 50
generations_sizes = 20
a = 1
p = 1
t = 1

testresultsfile = "outputs/testresults/"

def read_testresults(tag):
    if not os.path.isfile(testresultsfile + tag + '.trs'):
        write_testresult(TestResults(tag))

    with open(testresultsfile + tag + '.trs', 'rb+') as datafile:
        return pickle.load(datafile)

def write_testresult(results):
    with open(testresultsfile + results.tag + '.trs', 'wb+') as datafile:
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

def initfig():
    plt.figure(figsize=(11,8.5))

def show():
    plt.show()

def title(s):
    plt.title(s)

def legend():
    plt.legend()

def savefig(name,rangex=None,rangey=None):
    axes = plt.gca()
    if rangex:
        axes.set_xlim(rangex)
    if rangey:
        axes.set_ylim(rangey)

    plt.savefig(name)

def plot_percents(parents,ratio):

    results = read_testresults("percents").get_result("percents",parents,ratio)

    plt.title("Percentage of population that is dominant trait")#\n(parents=" + str(parents) + ",ratio=" + str(ratio) + ")")
    plt.xlabel('Generation')
    plt.ylabel('Percentage Red')

    xs = [x for x in range(len(results))]

    plt.plot(xs, results, '.', label='ratio=' + str(ratio))

def plot_percents_range(parents_range,ratio_range):
    for parents in parents_range:
        for ratio in ratio_range:
            plot_percents(parents,ratio)

def plot_exp_regressions(parents_range, ratio_range, x50=False):
    regressionsdata = read_testresults("exp_regressions")

    for parents in parents_range:
        counter = 0
        for ratio in ratio_range:
            equ = regressionsdata.get_result("equations",parents,ratio)

            def fit_fn(x):
                return equ.a * np.exp(equ.b*x) + equ.c

            x = [i for i in range(equ.maxx)]

            x = np.arange(min(x),max(x),0.1)
            y = [fit_fn(xi) for xi in x]

            plt.plot(x,y,'--C'+ str(counter))

            if x50:
                xv = equ.solve_x_at(0.5)
                if xv < max(x):
                    plt.plot([xv], [0.5], '--C'+ str(counter), marker='o', markersize=20)

            counter += 1

def plot_d50s(parents,ratio_range):
    regressionsdata = read_testresults("exp_regressions")

    xs = []
    ys = []

    counter = 0
    for ratio in ratio_range:
        xs.append(ratio)

        equ = regressionsdata.get_result("equations",parents,ratio)
        ys.append(equ.d50())

    plt.scatter(xs,ys)

    fit = optimize.curve_fit(lambda t,a,b: a*t + b,  xs,  ys,  p0=(0.3,0))
    fit = fit[0]
    def fit_fn(x):
        return fit[0]*x + fit[1]
    xs = np.arange(min(xs),max(xs),0.1)
    ys = [fit_fn(xi) for xi in xs]
    label = '(d50) ' + str(fit[0]) + 'x + (' + str(fit[1]) + ')'
    plt.plot(xs,ys,'--b',label=label)

    plt.xlabel('Ratio')
    plt.ylabel('Derivative')

def plot_d0s(parents_range,ratio_range):
    regressionsdata = read_testresults("exp_regressions")

    for parents in parents_range:
        xs = []
        ys = []

        for ratio in ratio_range:
            xs.append(ratio)

            equ = regressionsdata.get_result("equations",parents,ratio)
            ys.append(equ.d0())

        plt.scatter(xs,ys,c='r')

        fit = optimize.curve_fit(lambda t,a,b: a*t + b,  xs,  ys,  p0=(0.3,0))
        
        fit = fit[0]
        def fit_fn(x):
            return fit[0]*x + fit[1]
        xs = np.arange(min(xs),max(xs),0.1)
        ys = [fit_fn(xi) for xi in xs]
        label = '(d0) ' + str(fit[0]) + 'x + (' + str(fit[1]) + ')'
        plt.plot(xs,ys,'--r',label=label)

    plt.xlabel('Ratio')
    plt.ylabel('Derivative')

# parents vs d0, rather than the above ratio vs d0
def plot_d0s_parents(parents_range,ratio,regression_type="linear"):
    regressionsdata = read_testresults("exp_regressions")

    # plot raw data

    stds = []

    for parents in parents_range:

        # array of equations for this data point on parent number
        equations_raw = regressionsdata.get_result("equations_raw", parents, ratio)

        # array of data points for this parents number value
        ys = []

        for equ in equations_raw:
            ys.append(equ.d0())

        for y in ys:
            plt.scatter([parents],[y],c='b',s=10,zorder=2)

        stds.append(np.std(ys))

    # calculate smooth data and plot error bars

    xs = []
    ys = []
    i = 0

    for parents in parents_range:
        xs.append(parents)

        equ = regressionsdata.get_result("equations",parents,ratio)
        d0 = equ.d0()
        ys.append(d0)

        # plot error bars
        plt.errorbar([parents], d0, xerr=0, yerr=stds[i]/2,ecolor='r',elinewidth=10,zorder=1)
        i += 1

    # plot smoothed data

    plt.scatter(xs,ys,c='g',s=100,zorder=3)

    # regression

    fit = None
    fit_fn = None

    if regression_type == "linear":
        fit = optimize.curve_fit(lambda t,a,b: a*t + b,  xs,  ys,  p0=(0.3,0))
        fit = fit[0]
        fit_fn = lambda x: fit[0]*x + fit[1]
        print("y(x) = ax + b")
        print("a =",fit[0])
        print("b =",fit[1])

    elif regression_type == "quadratic":
        fit = optimize.curve_fit(lambda t,a,b,c: a*t**2 + b*t + c,  xs,  ys,  p0=(0.3,0,0.5))
        fit = fit[0]
        fit_fn = lambda x: fit[0]*x**2 + fit[1]*x + fit[2]
        print("y(x) = ax^2 + bx + c")
        print("a =",fit[0])
        print("b =",fit[1])
        print("c =",fit[2])

    xs = np.arange(min(xs),max(xs),0.1)
    ys = [fit_fn(xi) for xi in xs]
    label = '(d0) ' + str(fit[0]) + 'x + (' + str(fit[1]) + ')'
    plt.plot(xs,ys,'--g',label=label)

    plt.xlabel('Parents')
    plt.ylabel('Derivative')

def plot_first_slopes_parents(parents_range,ratio,regression_type="linear"):
    FS_data = read_testresults("first_slopes")

    # plot raw data

    stds = []

    for parents in parents_range:
        # array of FS for this data point on parent number
        FS_raw = FS_data.get_result("first_slopes_raw", parents, ratio)
        # scatter
        for fs in FS_raw:
            plt.scatter([parents],[fs],c='b',s=10,zorder=2)

        stds.append(np.std(FS_raw))

    # calculate smooth data and plot error bars

    xs = []
    ys = []
    i = 0

    for parents in parents_range:
        xs.append(parents)
        fs = FS_data.get_result("first_slopes",parents,ratio)
        ys.append(fs)

        # plot error bars
        plt.errorbar([parents], fs, xerr=0, yerr=stds[i]/2,ecolor='r',elinewidth=10,zorder=1)
        i += 1

    # plot smoothed data

    plt.scatter(xs,ys,c='g',s=100,zorder=3)

    # regression

    fit = None
    fit_fn = None

    if regression_type == "linear":
        fit = optimize.curve_fit(lambda t,a,b: a*t + b,  xs,  ys,  p0=(0.3,0))
        fit = fit[0]
        fit_fn = lambda x: fit[0]*x + fit[1]
        print("y(x) = ax + b")
        print("a =",fit[0])
        print("b =",fit[1])

    elif regression_type == "quadratic":
        fit = optimize.curve_fit(lambda t,a,b,c: a*t**2 + b*t + c,  xs,  ys,  p0=(0.3,0,0.5))
        fit = fit[0]
        fit_fn = lambda x: fit[0]*x**2 + fit[1]*x + fit[2]
        print("y(x) = ax^2 + bx + c")
        print("a =",fit[0])
        print("b =",fit[1])
        print("c =",fit[2])

    xs = np.arange(min(xs),max(xs),0.1)
    ys = [fit_fn(xi) for xi in xs]
    label = '(fs) ' + str(fit[0]) + 'x + (' + str(fit[1]) + ')'
    plt.plot(xs,ys,'--g',label=label)

    plt.xlabel('Parents')
    plt.ylabel('First Slope')

class Exp_Equation:
    def __init__(self,a,b,c,maxx):
        self.a = a
        self.b = b
        self.c = c
        self.maxx = maxx

    def solve_x_at(self,y):
        return (1/self.b)*np.log((y-self.c)/self.a)

    def derivative(self,x):
        return self.a * self.b * np.exp(self.b * x)

    def d50(self):
        return self.derivative(self.solve_x_at(0.5))

    def d0(self):
        return self.derivative(self.solve_x_at(0))

def calc_exp_regressions(parents_range, ratio_range):
    results = read_testresults("exp_regressions")
    results.add_category("equations")

    # calculate regressions for smoothed data
    for parents in parents_range:
        for ratio in ratio_range:
            # data is list of percents
            data = read_testresults("percents").get_result("percents",parents,ratio)

            xs = [x for x in range(0,len(data))]
            ys = [x - 1 for x in data] # want the max of the exp function to be 0

            fit = optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+c,  xs,  ys,  p0=(-0.5,-0.1,0))
            fit = fit[0]
            fit[2] += 1 # add the 1 back in

            results.add_result("equations",parents,ratio,Exp_Equation(fit[0],fit[1],fit[2],len(data)))

    # calculate regressions for raw data
    for parents in parents_range:
        for ratio in ratio_range:
            # data is list of percents
            data_raw = read_testresults("percents").get_result("percents_raw",parents,ratio)

            equations_raw = []

            for data in data_raw:

                try:

                    xs = [x for x in range(0,len(data))]
                    ys = [x - 1 for x in data] # want the max of the exp function to be 0

                    fit = optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+c,  xs,  ys,  p0=(-0.5,-0.1,0))
                    fit = fit[0]
                    fit[2] += 1 # add the 1 back in

                    equ = Exp_Equation(fit[0],fit[1],fit[2],len(data))
                    equations_raw.append(equ)

                except:
                    pass

            results.add_result("equations_raw",parents,ratio,equations_raw)

    write_testresult(results)

def calc_first_slopes(parents_range,ratio_range):
    results = read_testresults("first_slopes")
    results.add_category("first_slopes")

    for parents in parents_range:
        for ratio in ratio_range:
            ### SMOOTHED ###
            # calculate first slopes for smoothed data
            data = read_testresults("percents").get_result("percents",parents,ratio)
            # difference between first and second %s (1 generation along x axis, so divide by 1 :P )
            FS = data[1] - data[0]
            # add result at p,r coordinate
            results.add_result("first_slopes",parents,ratio,FS)

            ### RAW ###
            # calculate first slopes for smoothed data (array of raw data)
            data = read_testresults("percents").get_result("percents_raw",parents,ratio)
            # difference between first and second %s (1 generation along x axis, so divide by 1 :P )
            FS_raw = []
            for d in data:
                FS_raw.append(d[1] - d[0])
            # add result at p,r coordinate
            results.add_result("first_slopes_raw",parents,ratio,FS_raw)

    write_testresult(results)
            

def calc_smoothed_percents(parents,ratio,tests):
    testresults = read_testresults("percents")

    # graph percents vs generation num
    set_parameters({'parents': parents, 'ratio': ratio})

    # store all the calculated percents for each test
    # in form : percents[generation]
    percents = []

    for i in tqdm(range(tests)):
        make_inspector_genealogy()

        percents.append(get_percents())

    results = [[] for x in range(len(percents[0]))]
    results_raw = [[] for x in range(len(percents))]

    # i is the index of the list
    for i in range(len(percents)):
        # j is the index of the generation
        for j in range(len(percents[i])):
            results[j].append(percents[i][j])

    # i is the index of the list
    for i in range(len(percents)):
        # j is the index of the generation
        for j in range(len(percents[i])):
            results_raw[i].append(percents[i][j])

    for i in range(len(results)):
        results[i] = np.mean(results[i])

    # save results to appropriate file:
    testresults.add_result("percents", parents, ratio, results)
    testresults.add_result("percents_raw", parents, ratio, results_raw)
    write_testresult(testresults)

    return results

def calc_smoothed_percents_range(parents_range,ratio_range,tests):
    for parents in parents_range:
        for ratio in ratio_range:
            calc_smoothed_percents(parents,ratio,tests)