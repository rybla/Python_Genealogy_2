import numpy as np
import matplotlib.pyplot as plt
import pickle

for i in np.arange(1,2.0,0.2):
    with open('percents(parents=1,ratio=' + str(i) + ').list', 'rb') as percents:
        percents = pickle.load(percents)
        x = [x for x in range(len(percents))]
        fit = np.polyfit(x,percents,3)
        fit_fn = np.poly1d(fit)
        plt.plot(x, percents, 'ro', x, fit_fn(x), '--k')

plt.show()

quit()