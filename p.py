# coding: utf-8

import compy as cp
import numpy as np
import matplotlib.pyplot as plt

D = cp.Domain(-4, 4, 1000)
#V = np.zeros(len(D))
#V[0] = 1e15
#V[-1] = 1e15
V = 0.5*D.as_array()**2

ev, ef = cp.schrodinger.solve_numerov(D, V, 1, 1, eigen_num=2)

for v, f in zip(ev, ef):
    plt.plot(D.as_array(), cp.schrodinger.square_modulus(f), label="{:.4}".format(v))

plt.grid(True)
plt.legend()
plt.show()
