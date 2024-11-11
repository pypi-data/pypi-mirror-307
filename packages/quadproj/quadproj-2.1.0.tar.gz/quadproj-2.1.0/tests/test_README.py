from quadproj.quadrics import Quadric
from quadproj.project import project


import numpy as np


# creating random data
dim = 42
_A = np.random.rand(dim, dim)
A = _A + _A.T  # make sure that A is positive definite
b = np.random.rand(dim)
c = -1.42


param = {'A': A, 'b': b, 'c': c}
Q = Quadric(**param)

x0 = np.random.rand(dim)
x_project = project(Q, x0)
assert Q.is_feasible(x_project), 'The projection is incorrect!'
from quadproj.project import plot_x0_x_project

from os.path import join
import pathlib


root_folder = pathlib.Path(__file__).resolve().parent.parent
output_folder = join(root_folder, 'output')

import matplotlib.pyplot as plt

show = False

A = np.array([[1, 0.1], [0.1, 2]])
b = np.zeros(2)
c = -1
Q = Quadric(**{'A': A, 'b': b, 'c': c})

x0 = np.array([2, 1])
x_project = project(Q, x0)

fig, ax = Q.plot(show=show)
plot_x0_x_project(ax, Q, x0, x_project)
plt.savefig(join(output_folder, 'ellipse_no_circle.png'))
fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
fig.savefig(join(output_folder, 'ellipse_circle.png'))
if show:
    plt.show()
x0 = Q.to_non_normalized(np.array([0, 0.1]))
x_project = project(Q, x0)
fig, ax = Q.plot(show_principal_axes=True)
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
fig.savefig(join(output_folder, 'ellipse_degenerated.png'))
if show:
    plt.show()
A[0, 0] = -2
Q = Quadric(**{'A': A, 'b': b, 'c': c})
x0 = Q.to_non_normalized(np.array([0, 0.1]))
x_project = project(Q, x0)
fig, ax = Q.plot(show_principal_axes=True)
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
fig.savefig(join(output_folder, 'hyperbola_degenerated.png'))
if show:
    plt.show()
dim = 3
A = np.eye(dim)
A[0, 0] = 2
A[1, 1] = 0.5

b = np.zeros(dim)
c = -1
param = {'A': A, 'b': b, 'c': c}
Q = Quadric(**param)


fig, ax = Q.plot()

fig.savefig(join(output_folder, 'ellipsoid.png'))

Q.get_turning_gif(step=4, gif_path=join(output_folder, Q.type + '.gif'))
from quadproj.quadrics import get_gif

A[0, 0] = -4

param = {'A': A, 'b': b, 'c': c}
Q = Quadric(**param)

x0 = np.array([0.1, 0.42, -1.5])

x_project = project(Q, x0)

fig, ax = Q.plot()
ax.grid(False)
ax.axis('off')
plot_x0_x_project(ax, Q, x0, x_project)
ax.get_legend().remove()

save_gif = True
if save_gif:
    get_gif(fig, ax, elev=15, gif_path=join(output_folder, 'one_sheet_hyperboloid.gif'))
if show:
    plt.show()
fig, ax = Q.plot()
ax.grid(False)
ax.axis('off')
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
ax.get_legend().remove()

if save_gif: 
    get_gif(fig, ax, elev=15, gif_path=join(output_folder, 'one_sheet_hyperboloid_ball.gif'))
A[0, 0] = 4
A[1, 1] = -2
A[2, 2] = -1

b = np.array([0.5, 1, -0.25])

c = -1

param = {'A': A, 'b': b, 'c': c}
Q = Quadric(**param)

x0 = np.array([0.1, 0.42, -0.45])

x_project = project(Q, x0)

fig, ax = Q.plot()
ax.grid(False)
ax.axis('off')
plot_x0_x_project(ax, Q, x0, x_project)

if save_gif:
    get_gif(fig, ax, gif_path=join(output_folder, 'two_sheet_hyperboloid.gif'))
if show:
    plt.show()
plt.close()

A = np.array([[1]])
b = np.array([-2])
c = 1
Q = Quadric(A=A, b=b, c=c)
fig, ax = Q.plot()

fig.savefig(join(output_folder, '1D.png'))

A = np.array([[1]])
b = np.array([0])
c = -1
Q = Quadric(A=A, b=b, c=c)
fig, ax = Q.plot()

fig.savefig(join(output_folder, '2D.png'))
from scipy.stats import ortho_group

A = np.array([[2, 0], [0, 1]])
b = np.array([-1, 1])
c = -2

V = ortho_group.rvs(2)
A2 = V @ A @ V.T
b2 = V @ b
c2 = -2

Q = Quadric(A=A2, b=b2, c=c2)

fig, ax = Q.plot()

fig.savefig(join(output_folder, 'ellipse.png'))
from scipy.stats import ortho_group

A = np.array([[2, 0, 0], [0, 1, 0], [0, 0, 0]])
b = np.array([-1, 1, 0])
c = -2

V = ortho_group.rvs(3)
A2 = V @ A @ V.T
b2 = V @ b
c2 = -2

Q = Quadric(A=A2, b=b2, c=c2)

fig, ax = Q.plot()

fig.savefig(join(output_folder, 'ellipsoid_cylinder.png'))

A = np.array([[0, 0, 0], [0, 2, 0], [0, 0, -1.5]])
b = np.array([0, 0, 0])
c = 0
Q = Quadric(A=A, b=b, c=c)


x0 = np.array([0, -1, 0])
x_project = project(Q, x0)


fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project)


fig.savefig(join(output_folder, 'elliptic_cone_cylinder.png'))
param = {}
param['A'] = np.array([[4, 0, 0], [0, -2, 0], [0, 0, 10]])
param['b'] = np.array([0, 0, 0])
param['c'] = 0
Q = Quadric(**param)
fig, ax = Q.plot()

fig.savefig(join(output_folder, 'elliptic_cone.png'))
param = {}
param['A'] = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
param['b'] = np.array([0, 0, 1])
param['c'] = -1.5
Q = Quadric(**param)
fig, ax = Q.plot()

fig.savefig(join(output_folder, 'elliptic_paraboloid.png'))
param = {}
param['A'] = np.array([[-1, 0, 0], [0, 2, 0], [0, 0, 0]])
param['b'] = np.array([0, 0, 1])
param['c'] = -1.5
Q = Quadric(**param)

x0 = np.array([0.7, -0.42, -1.45])


x_project = project(Q, x0)


fig, ax = Q.plot()

ax.grid(False)
ax.axis('off')

plot_x0_x_project(ax, Q, x0, x_project)


if save_gif:
    get_gif(fig, ax, gif_path=join(output_folder, 'hyperbolic_paraboloid.gif'))

if show:
    plt.show()

A = np.array([[1, 0, 0], [0, -2, 0], [0, 0, 0]])
b = np.array([-1, 2, 0])
c = -2.1
Q = Quadric(**{'A': A, 'b': b, 'c': c})

x0 = np.array([1, -2, 0])

x_project = project(Q, x0)
fig, ax = Q.plot(show_principal_axes=True)
plot_x0_x_project(ax, Q, x0, x_project)
if save_gif:
    get_gif(fig, ax, elev=15, gif_path=join(output_folder, 'hyperboloid_cylinder.gif'))
if show:
    plt.show()

A = np.array([[1, 0], [0, 0]])
b = np.array([0, 2])
c = -2
param = {'A': A, 'b': b, 'c': c}
Q = Quadric(**param)

fig, ax = Q.plot()

fig.savefig(join(output_folder, 'parabola.png'))

A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
b = np.array([0, 2, 0])
c = -2
param = {'A': A, 'b': b, 'c': c}
Q = Quadric(**param)

fig, ax = Q.plot()

fig.savefig(join(output_folder, 'paraboloid_cylinder.png'))

A = np.array([[1, 0], [0, 0]])
b = np.array([0, 0])

c = -1
Q = Quadric(A=A, b=b, c=c)

x0 = np.array([-2, 1.5])
x_project = project(Q, x0)

fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project)


fig.savefig(join(output_folder, 'parallel_lines.png'))
A = np.array([[0, 0, 0], [0, -2, 0], [0, 0, 0]])
b = np.array([0, 0, 0])

c = 1
Q = Quadric(A=A, b=b, c=c)

x0 = np.array([1, 1.5, 0])
x_project = project(Q, x0)

fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project)

fig.savefig(join(output_folder, 'parallel_planes.png'))

A = np.array([[2, 0], [0, -1.5]])
b = np.array([0, 0])
c = 0
Q = Quadric(A=A, b=b, c=c)


x0 = np.random.rand(2)
x_project = project(Q, x0)


fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)


fig.savefig(join(output_folder, 'secant_lines.png'))

A = np.array([[1, 0], [0, 0]])
b = np.array([-2, 0])

c = 1
Q = Quadric(A=A, b=b, c=c)

x0 = np.array([1, 1.5])
x_project = project(Q, x0)

fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project)

fig.savefig(join(output_folder, 'single_line.png'))
A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
b = np.array([-2, 0, 0])

c = 1
V = ortho_group.rvs(3)
A2 = V @ A @ V.T
b2 = V @ b
Q = Quadric(A=A2, b=b2, c=c)

x0 = np.array([1, 1.5, 0])
x_project = project(Q, x0)

fig, ax = Q.plot()
plot_x0_x_project(ax, Q, x0, x_project)

fig.savefig(join(output_folder, 'single_plane.png'))
