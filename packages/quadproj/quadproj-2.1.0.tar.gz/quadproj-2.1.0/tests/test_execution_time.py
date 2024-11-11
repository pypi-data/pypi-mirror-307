import quadproj
from quadproj import quadrics
from quadproj.project import project

import matplotlib
import matplotlib.pyplot as plt

from scipy.optimize import fsolve

import numpy as np
import time


matplotlib.rc('text', usetex=True)
rc_fonts = {
    "text.usetex": True,
    'text.latex.preview': True,  # Gives correct legend alignment.
    'mathtext.default': 'regular',
    'text.latex.preamble': [r"""\usepackage{bm}"""],
}
matplotlib.rcParams.update({'font.size': 16})

dims = np.arange(2, 1000, 100)

time_array_eigen = np.zeros(len(dims))
time_array_newton = np.zeros(len(dims))
time_array_fsolve = np.zeros(len(dims))
time_total_quadproj = np.zeros(len(dims))

n_instances = 5

for i, dim in enumerate(dims):
    print(f'Running dimension {dim}')
    for m in range(n_instances):
        print(f'Running instance {m} of dimension {dim}')

        _A = np.random.rand(dim, dim)
        A = _A + _A.T  # make sure that A is positive definite
        b = np.random.rand(dim)
        c = -1.42

        param = {'A': A, 'b': b, 'c': c}
        tic = time.time()
        tic_total = time.time()
        Q = quadrics.Quadric(**param)
        time_array_eigen[i] += (time.time() - tic) / n_instances
        x0 = np.random.rand(dim)

        tic = time.time()
        x_project = project(Q, x0)
        time_array_newton[i] += (time.time() - tic) / n_instances
        time_total_quadproj[i] += (time.time() - tic_total) / n_instances

        def F(y):
            x = y[:-1]
            mu = y[-1]
            out_1 = 2 * (x - x0) + 2 * mu * A @ x + mu * b
            out_2 = np.dot(x, np.dot(A, x)) + np.dot(b, x) + c
            return np.hstack((out_1, out_2))
        mu0 = 0
        y0 = np.hstack((x0, np.ones(1) * mu0))
        tic = time.time()
        out_fsolve = fsolve(F, y0)
        x_project_fsolve = out_fsolve[:-1]
        test_fsolve = np.linalg.norm(x_project_fsolve - x_project) < pow(10, -6)
        if not test_fsolve:
            print(f'Distance from x_project is {np.linalg.norm(x_project -x0)} \n Distance from x_project_fsolve is {np.linalg.norm(x_project_fsolve-x0)}')
            fig, ax = Q.plot(show=False, show_principal_axes=True)
            quadproj.project.plot_x0_x_project(ax, Q, x0, x_project)
            ax.scatter(x_project_fsolve[0], x_project_fsolve[1], color='green')
            print(f'Q.eig {Q.eig} \n Q.eig_bar{Q.eig_bar}\n x0_std {Q.to_standardized(x0)}')
            print(Q.is_feasible(x_project), Q.is_feasible(x_project_fsolve))
            plt.show()
        assert np.linalg.norm(x_project_fsolve - x_project) < pow(10, -6), 'Solution obtained by fsolve is incorrect'
        toc_fsolve = time.time() - tic
        time_array_fsolve[i] += toc_fsolve / n_instances


plt.semilogy(dims, time_array_eigen, 'b', marker='v', label='quadproj time to build the quadric')
plt.semilogy(dims, time_array_newton, 'r', marker='^', label='quadproj time to project')
plt.semilogy(dims, time_total_quadproj, '--', marker='o', label='quadproj total time')
plt.semilogy(dims, time_array_fsolve, '--', marker='*', label='fsolve total time')
plt.legend()

plt.xlabel('Quadric size $n$')
plt.ylabel('Execution time [s]')

# plt.savefig('out_test_execution_time.pdf')
# plt.savefig('out_test_execution_time.png')

plt.show()
