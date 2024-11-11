#!/usr/bin/env python3

import numpy as np
from quadproj.quadrics import Quadric
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from quadproj.fun import Fun
from quadproj.project import double_newton

import time

eps_test = pow(10, -6)

np.random.seed(1)


def _test_convergence_newton(dim=500):
    Q = None
    while Q is None or Q.is_empty:
        _A = np.random.rand(dim, dim)
        A = (_A + _A.T) / 2

        param = {'A': A, 'b': np.random.rand(dim), 'c': np.random.randn() * dim / 5}
        E, _ = np.linalg.eig(A)
        tic = time.time()
        Q = Quadric(**param)
        toc_quadric = time.time() - tic  # most of the execution time needed to build the quadric is taken by the eigendecomposition
    x0_not_std = np.random.rand(dim)

    x0 = Q.to_normalized(x0_not_std)
    F = Fun(Q, x0)
    hist = {'f': [], 'x': [], 'df': []}
    tic = time.time()
    output_newton = double_newton(F, **hist)
    toc_newton = time.time() - tic
    dist = [abs(el - hist['x'][-1]) for el in hist['x']]
    flag_s = output_newton.message.split(' ')[-1] == '0'
    return dist, hist['f'], flag_s, hist, toc_newton, toc_quadric


''' Plotting the result
    The color difference (blue or red) indicates whether we started the newton method
    from mu=0 or mu=mu_s (the latter being obtained via substitution).
'''

fig, ax = plt.subplots()
dist_r = []
f_r = []
iterations_r = []
dist_b = []
f_b = []
iterations_b = []
alpha = 0.25
full_toc_newton = []
full_toc_quadric = []
m = 50
for i in range(m):
    _dist, _f, flag_s, hist, toc_newton, toc_quadric = _test_convergence_newton()
    full_toc_newton.append(toc_newton)
    full_toc_quadric.append(toc_quadric)
    if flag_s:
        color = 'blue'
        dist_b.append(_dist)
        f_b.append(_f)
        iterations_b.append(len(_dist))
    else:
        color = 'red'
        dist_r.append(_dist)
        f_r.append(_f)
        iterations_r.append(len(_dist))
    _dist = np.delete(_dist, np.where(np.abs(_dist) < pow(10, -16)))
    ax.semilogy(np.arange(len(_dist)), _dist, color=color, alpha=alpha, linewidth=1.5)
    ax.set_xlabel(r'Iterations')
    ax.set_ylabel(r'$\|\| \mu^k - \mu^* \| \|_2$')
ax.plot([0], [0], color='blue', alpha=alpha, linewidth=2, label='Starting from $0$')
ax.plot([0], [0], color='red', alpha=alpha, linewidth=2, label='Starting from $ \\mu_s $')
ax.legend()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

print(f"Mean execution time of newton is {np.mean(full_toc_newton)} \n \
      Mean execution time of the eigendecomposition is {np.mean(full_toc_quadric)}")

# fig.savefig('../output/newton.pdf', bbox_to_inches='tight')  # TODO: use relative path of file


fig, ax = plt.subplots()
plt.boxplot([full_toc_newton, full_toc_quadric])
plt.xticks([1, 2], ['newton', 'eigendecomposition'])
plt.ylabel('execution time (s)')
# fig.savefig('../output/newton_boxplot.pdf', bbox_to_inches='tight')
plt.show()
