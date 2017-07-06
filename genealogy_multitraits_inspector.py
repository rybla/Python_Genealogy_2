import matplotlib.pyplot as plt
import genealogy_multitraits as genealogy
import numpy as np
import pickle
import os
from tqdm import tqdm
from scipy import optimize
import testresults
from testresults import TestResults


parents = 1
tests = 4
generations = 50
generations_sizes = 20
a = 1
p = 1
t = 1
traits = [2,3,4]
target = [1,1,1]
traits_function = 'prod'

ratio = 0 # doesnt matter for multitrait genealogies

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
    global tests, parents, generations, generations_sizes, a, p, t, traits, target, traits_function
    if 'tests' in params:
        tests = params['tests']
    if 'parents' in params:
        parents = params['parents']
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
    if 'traits' in params:
        traits = params['traits']
    if 'target' in params:
        target = params['target']
    if 'traits_function' in params:
        traits_function = params['traits_function']

def generation_sizes_function(gen_ind):
    return generations_sizes

def make_inspector_genealogy():

    genealogy.init_genealogy()

    genealogy.make_genealogy(
            generations=generations,
            parents=parents,
            generation_sizes_function=generation_sizes_function,
            age_factor=a,
            popular_factor=p,
            trait_factor=t,
            traits=traits,
            traits_function=traits_function
        )

def get_percents():
    # percents (for each generation)
    percents = []

    # calculate percents
    i = 0
    for j in genealogy.GENERATION_COUNTS:
        
        # see how many members have the target trait
        count = 0
        for k in range(j):
            count += int(genealogy.get_member_raw_traits(i) == target)
            i += 1

        percents.append( count / j )

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

def plot_percents(parents):
    results = read_testresults("percents").get_result("percents",parents,ratio)

    plt.title("Percentage of population that is dominant trait")#\n(parents=" + str(parents) + ",ratio=" + str(ratio) + ")")
    plt.xlabel('Generation')
    plt.ylabel('Percentage Gray')

    xs = [x for x in range(len(results))]

    plt.plot(xs, results, '.', label='parents=' + str(parents))

def plot_percents_range(parents_range):
    for parents in parents_range:
        plot_percents(parents)

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


def plot_first_slopes_parents(parents_range,regression_type="linear"):
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
        plt.errorbar([parents], fs, xerr=0, yerr=stds[i],ecolor='r',elinewidth=10,zorder=1)
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

def calc_first_slopes(parents_range):
    results = read_testresults("first_slopes")
    results.add_category("first_slopes")

    for parents in parents_range:
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
            

def calc_smoothed_percents(parents):
    testresults = read_testresults("percents")

    # graph percents vs generation num
    set_parameters({'parents': parents})

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

def calc_smoothed_percents_range(parents_range):
    for parents in parents_range:
        calc_smoothed_percents(parents)