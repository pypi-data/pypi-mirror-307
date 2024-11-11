#!/usr/bin/env python3

import numpy as np
from quadproj.quadrics import Quadric
from .test_project import _get_unitary_matrix
import matplotlib.pyplot as plt

from scipy.stats import ortho_group


eps_test = pow(10, -6)
SHOW = True


def test_initiate_quadrics():
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = 0

    Quadric(**param)


def test_initiate_quadrics2():
    A = np.diag([1, -1, -1, -1, -1, -1, 0])
    b = np.zeros(A.shape[0])
    b[-1] = 1
    c = 1
    Quadric(A=A, b=b, c=c)


def test_equivalence_std():
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = 0

    Q = Quadric(**param)
    x0_not_std = np.array([0, 1])
    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x0 = Q.to_normalized(x0_not_std)
    assert abs(Q.evaluate_point(x0_not_std) - np.dot(np.dot(x0, Q.L), x0) - Q.c_norm) < eps_test

    param = {}
    param['A'] = np.array([[-1, 0], [0, 2]])
    param['b'] = np.array([1, 0])
    param['c'] = -2
    param['diagonalize'] = True
    Q = Quadric(**param)
    x0_not_std = np.array([1, 1])

    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x0 = Q.to_normalized(x0_not_std)

    assert np.all(x0_not_std == Q.to_non_normalized(x0)), \
        'Transform to and from standardized yield an error'
    assert abs(Q.evaluate_point(x0_not_std) -
               np.dot(np.dot(x0, Q.L), x0) + 1) < eps_test


def test_equivalence_parabolic():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([-1, 2])
    c = 0
    Q = Quadric(A=A, b=b, c=c)
    x0_not_std = np.array([0, 0])
    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x0 = Q.to_normalized(x0_not_std)
    assert abs(Q.evaluate_point(x0_not_std) - x0.T @ Q.A_norm @ x0 - Q.b_norm @ x0 - Q.c_norm) < eps_test

    A = np.array([[1, -1], [-1, 0]])
    b = np.array([-1, 2])
    c = 0
    Q = Quadric(A=A, b=b, c=c)
    x0_not_std = np.array([0, 0])
    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x0 = Q.to_normalized(x0_not_std)
    assert np.allclose(x0_not_std, Q.to_non_normalized(x0))
    assert abs(Q.evaluate_point(x0_not_std) - x0.T @ Q.A_norm @ x0 - Q.b_norm @ x0 - Q.c_norm) < eps_test

    A = np.array([[1, -1], [-1, 0]])
    b = np.array([-1, 2])
    c = 4
    Q = Quadric(A=A, b=b, c=c)
    x0_not_std = np.array([2, 3])
    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x0 = Q.to_normalized(x0_not_std)
    assert np.allclose(x0_not_std, Q.to_non_normalized(x0))
    assert abs(Q.evaluate_point(x0_not_std) - x0.T @ Q.A_norm @ x0 - Q.b_norm @ x0 - Q.c_norm) < eps_test


def test_equivalence_elliptic_paraboloid():
    A = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    b = np.array([1, 1, 1]).T
    c = -4
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    assert Q.is_elliptic_paraboloid
    x0_not_std = np.array([0, 1, 1])
    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x0 = Q.to_normalized(x0_not_std)
    assert np.allclose(x0_not_std, Q.to_non_normalized(x0))
    assert np.allclose(x0, Q.to_normalized(x0_not_std))
    assert abs(Q.evaluate_point(x0_not_std) - x0.T @ Q.A_norm @ x0 - Q.b_norm @ x0 - Q.c_norm) < eps_test

    # what if we rotate it
    V = _get_unitary_matrix(3)
    A = V @ A @ V.T
    b = V @ b
    c = -4
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    assert Q.is_elliptic_paraboloid
    x0_not_std = V @ np.array([0, 1, 1])
    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    assert np.allclose(abs(x0), abs(Q.to_normalized(x0_not_std)))
    x0 = Q.to_normalized(x0_not_std)
    assert np.allclose(x0_not_std, Q.to_non_normalized(x0))
    assert np.allclose(x0, Q.to_normalized(x0_not_std))
    assert abs(Q.evaluate_point(x0_not_std) - x0.T @ Q.A_norm @ x0 - Q.b_norm @ x0 - Q.c_norm) < eps_test


def test_equivalence_paraboloid_cylinder():
    A = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    b = np.array([0, -1, 3, 1])
    c = -9
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_paraboloid_cylinder
    print("A norm", Q.A_norm)
    print("b norm", Q.b_norm)
    print("c norm", Q.c_norm)

    x0_not_std = np.array([1, 0, 2])
    x0_not_std = np.array([2, 0, 1, 2])
    x0 = Q.to_normalized(x0_not_std)

    old_Q = Q
    # what if we rotate it
    V = _get_unitary_matrix(4)
    A = V @ A @ V.T
    b = V @ b
    c = c
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    assert Q.is_elliptic_paraboloid
    assert np.allclose(Q.A_norm, old_Q.A_norm)
    assert np.allclose(Q.c_norm, old_Q.c_norm)
    assert np.allclose(Q.gamma, old_Q.gamma)
    x0_not_std = V @ x0_not_std
    assert Q.is_feasible(x0_not_std), 'Two points are equivalent iff they are feasible'
    x02 = Q.to_normalized(x0_not_std)
    assert abs(Q.evaluate_point(x0_not_std) - x02.T @ Q.A_norm @ x02 - Q.b_norm @ x02 - Q.c_norm) < eps_test

    assert np.allclose(x0_not_std, Q.to_non_normalized(x02))
    assert np.allclose(x0, Q.to_non_normalized(Q.to_normalized(x0)))
    assert np.allclose(x0_not_std, Q.to_normalized(Q.to_non_normalized(x0_not_std)))
    assert abs(Q.evaluate_point(x0_not_std) - x02.T @ Q.A_norm @ x02 - Q.b_norm @ x02 - Q.c_norm) < eps_test


def test_plot_1D():
    A = np.array([[1]])
    b = np.array([0])
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    Q.plot(show=SHOW)

    A = np.array([[1]])
    b = np.array([-2])
    c = 1
    Q = Quadric(A=A, b=b, c=c)
    Q.plot(show=SHOW)


def test_plot_2D():
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, 1]])
    param['b'] = np.array([1, 1])
    param['c'] = 0.3
    try:
        Q = Quadric(**param)
    except Quadric.EmptyQuadric:
        print('Correctly catch empty quadric!')

    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = -1
    plt.close()
    Q = Quadric(**param)
    Q.plot(show_principal_axes=True)
    param = {}
    param['A'] = np.array([[2, 0.4], [0.4, 1]])
    param['b'] = np.array([1, 1])
    param['c'] = -1
    Q = Quadric(**param)
    if SHOW:
        plt.show()
        plt.close()
        fig, ax = plt.subplots()
        Q.plot(fig=fig, ax=ax, show=True, show_principal_axes=True)
    param['A'] = np.array([[2, 0.4], [0.4, -1]])
    param['b'] = np.array([1, 1])
    param['c'] = -1
    Q = Quadric(**param)
    if SHOW:
        plt.close()
        fig, ax = plt.subplots()
        Q.plot(fig=fig, ax=ax, show=True, show_principal_axes=True)
        plt.show()
        plt.close('all')


def test_plot_3D():

    print('\n\n Two sheets hyperboloid \n\n')

    param = {}
    param['A'] = np.array([[-2, 0.4, 0.5], [0.4, 1, 0.6], [0.5, 0.6, -3]])
    param['b'] = np.array([1, 1, 0])
    param['c'] = -1.5
    Q = Quadric(**param)

    Q.plot(show=SHOW, show_principal_axes=True)

    print('\n\n Ellipsoid cylinder \n\n')
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    param['b'] = np.array([0, 2, 0])
    param['c'] = -1.5
    Q = Quadric(**param)
    assert Q.is_cylindrical
    Q.plot(show=SHOW, show_principal_axes=False)

    print('\n\n Paraboloid \n\n')
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]]) / 1
    param['b'] = np.array([0, 0, 1])
    param['c'] = -1.5
    Q = Quadric(**param)
    Q.plot(show=SHOW, show_principal_axes=True)
    print('\n\n Ellipsoid \n\n')

    param = {}
    param['A'] = np.array([[2, 0.4, 0.5], [0.4, 1, 0.6], [0.5, 0.6, 3]])
    param['b'] = np.array([1, 1, 0])
    param['c'] = -1.5
    Q = Quadric(**param)

    Q.plot(show=SHOW)
    plt.close('all')
    print('\n\n One sheet hyperboloid \n\n')
    param = {}
    param['A'] = np.array([[2, 0.4, 0.5], [0.4, 1, 0.6], [0.5, 0.6, -3]])
    param['b'] = np.array([1, 1, 0])
    param['c'] = -1.5
    Q = Quadric(**param)

    Q.plot(show=SHOW, show_principal_axes=True)

    plt.close('all')


def test_switching_equality():
    A = np.array([[-1, 0], [0, 0]])
    b = np.array([0, 1])
    c = 0

    Q = Quadric(A=A, b=b, c=c)
    assert np.linalg.norm(Q.A + A) < eps_test

    A = np.array([[1, 0], [0, 1]])
    Q = Quadric(A=A, b=b, c=c)
    assert np.linalg.norm(Q.A - A) < eps_test

    Q = Quadric(A=-A, b=-b, c=-c)
    assert np.linalg.norm(Q.A - A) < eps_test

    A = np.array([[-1, 0], [0, 1]])
    Q = Quadric(A=A, b=b, c=c)
    assert np.linalg.norm(Q.A - A) < eps_test


def test_parallel_lines():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([0, 0])
    c = 1
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_empty

    c = -1
    Q = Quadric(A=A, b=b, c=c)
    assert not Q.is_empty

    Q.plot(show=SHOW)

    A = np.array([[0, 0], [0, 1]])
    b = np.array([0, 0])
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    Q.plot(show=SHOW)


def test_single_point():
    A = np.array([[4]])
    b = np.array([12])

    c = 9
    Q = Quadric(A=A, b=b, c=c)
    assert not Q.is_empty
    Q.is_feasible(-3 / 2)

    Q.plot(show=SHOW)


def test_single_point_2():
    A = np.array([[1, 0], [0, 2]])
    b = np.array([0, 0])

    c = 0
    Q = Quadric(A=A, b=b, c=c)
    assert not Q.is_empty

    Q.plot(show=SHOW)


def test_single_line():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([-2, 0])

    c = 1
    Q = Quadric(A=A, b=b, c=c)
    assert not Q.is_empty

    Q.plot(show=SHOW)


def test_single_plane():
    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([-2, 0, 0])

    c = 1
    Q = Quadric(A=A, b=b, c=c)

    assert Q.is_single_plane
    Q.plot(show=SHOW)


def test_single_plane_rotated():
    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([-2, 0, 0])

    V = ortho_group.rvs(3)

    A2 = V @ A @ V.T
    b2 = V @ b

    c = 1
    Q = Quadric(A=A2, b=b2, c=c)

    assert Q.is_single_plane
    Q.plot(show=SHOW)


def test_parallel_planes():
    A = np.array([[0, 0, 0], [0, -2, 0], [0, 0, 0]])
    b = np.array([0, 0, 0])

    c = 1
    Q = Quadric(A=A, b=b, c=c)

    assert Q.is_parallel_planes
    Q.plot(show=SHOW)


def test_parallel_planes_rotated():
    A = np.array([[0, 0, 0], [0, -4, 0], [0, 0, 0]])
    b = np.array([0, 0, 0])

    V = ortho_group.rvs(3)

    A2 = V @ A @ V.T
    b2 = V @ b

    c = 17
    Q = Quadric(A=A2, b=b2, c=c)

    assert Q.is_parallel_planes
    Q.plot(show=SHOW)


def test_is_paraboloid_cylinder():
    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([0, -1, 1])
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_paraboloid_cylinder
    assert Q.is_feasible(np.array([0, 1 , 2]))
    if SHOW:
        fig, ax = Q.plot(show=False)
        ax.scatter(0, 1, 2, color="r")
        plt.show()


def test_paraboloid():
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, -2, 0], [0, 0, 0]]) / 1
    param['b'] = np.array([0, 0, 1])
    param['c'] = -1.5
    Q = Quadric(**param)
    assert Q.is_parabolic
    Q.plot(show=SHOW, show_principal_axes=True)


def test_paraboloid_cylinder():
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    param['b'] = np.array([0, 2, 0])
    param['c'] = -2
    Q = Quadric(**param)
    assert Q.is_paraboloid_cylinder
    Q.plot(show=SHOW)


def test_elliptic_cone():
    param = {}
    param['A'] = np.array([[4, 0, 0], [0, -2, 0], [0, 0, 10]])
    param['b'] = np.array([0, 0, 0])
    param['c'] = 0
    Q = Quadric(**param)
    Q.plot(show=SHOW)
    assert Q.is_elliptic_cone


def test_elliptic_cone_cylinder():
    param = {}
    param['A'] = np.array([[4, 0, 0], [0, -2, 0], [0, 0, 0]])
    param['b'] = np.array([0, 0, 0])
    param['c'] = 0
    Q = Quadric(**param)
    Q.plot(show=SHOW)
    assert Q.is_elliptic_cone_cylinder
