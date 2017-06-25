import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(11,8.5))

x = np.arange(1,10)
y = x/2

plt.scatter(x,y,c="b",s=1000)

for i in range(len(x)):
	plt.errorbar(x[i],y[i],xerr=0,yerr=y[i]**2,c="r",capthick=2,capsize=5)

plt.show()