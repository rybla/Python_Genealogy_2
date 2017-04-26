import numpy as np
import matplotlib.pyplot as plt
import random
random.seed()

n = 50
def f(x):
    return np.log(x) + random.randint(0,2)

xs = [x for x in range(50)]
ys = [f(x) for x in xs]

plt.scatter(xs, ys)

for i in range(len(xs)-1):
    print(i)
    if xs[i] <= 0:
        xs.remove(xs[i])
        ys.remove(ys[i])

fit = np.polyfit(np.log(xs), ys, deg=1)
fit_fn = np.poly1d(fit)

xs = np.arange(min(xs),max(xs),0.1)
ys = fit_fn(xs)

plt.plot(xs, ys)

plt.show()