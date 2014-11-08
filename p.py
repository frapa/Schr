# coding: utf-8

import numinger as nu
import numpy as np

D = nu.Domain(-1, 1, 1000)
V = np.zeros(len(D))
V[0] = 1e15
V[-1] = 1e15

nu.schrod(D, V, 0, 0)
