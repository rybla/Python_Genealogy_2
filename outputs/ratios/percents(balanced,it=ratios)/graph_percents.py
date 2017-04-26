import numpy as np
import pickle
import matplotlib.pyplot as plt

for i in np.arange(1,4.6,0.2):
    with open('percents(parents=1,ratio=' + str(i) + ').list', 'rb') as percents:
        percents = pickle.load(percents)
        plt.plot(percents)

plt.show()