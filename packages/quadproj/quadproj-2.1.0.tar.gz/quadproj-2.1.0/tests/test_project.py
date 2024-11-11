from quadproj.project import get_KKT_point_root, bisection
from quadproj.project import my_newton, double_newton, project, plot_x0_x_project

import quadproj.fun as fun
from quadproj.quadrics import Quadric
from scipy.stats import ortho_group

import matplotlib.pyplot as plt
import numpy as np

eps = pow(10, -6)
eps_test = pow(10, -2)

SHOW = False


def test_get_e1():
    dim = 6
    A = np.eye(dim)
    A[0, 0] = 0.5
    A[2, 2] = -3
    param = {'A': A, 'b': np.zeros(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 1
    x0_not_std[2] = 3
    x0 = Q.to_normalized(x0_not_std)

    e1 = fun._get_e1(Q, x0)
    e2 = fun._get_e2(Q, x0)
    # we're switching equality sign so eigenvalue are [3 -0.5 -1 -1 -1 -1]
    # but x0 is [3 1 0 0 0 0] so we take 3 e1  and -0.5 for e2 (not -1)
    assert e1 == -1 / 0.5
    assert e2 == -1 / -3
    A = np.eye(dim)
    A[0, 0] = 0.5
    A[2, 2] = -2
    A[5, 5] = -4
    param = {'A': A, 'b': np.zeros(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.ones(dim)
    x0_not_std[0] = 10
    x0_not_std[1] = 2
    x0_not_std[2] = 3
    x0 = Q.to_normalized(x0_not_std)
    e1 = fun._get_e1(Q, x0)
    e2 = fun._get_e2(Q, x0)
    assert e1 == -1 / 1
    assert e2 == -1 / -4

    A = np.eye(dim)
    A[0, 0] = -0.5
    A[2, 2] = -2
    param = {'A': A, 'b': np.zeros(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 1
    x0_not_std[2] = 3
    x0 = Q.to_normalized(x0_not_std)
    assert fun._get_e1(Q, x0) == -np.inf
    assert fun._get_e2(Q, x0) == 0.5

    A = np.eye(dim)
    A[0, 0] = 2
    A[2, 2] = -1.5
    b = np.zeros(dim)
    b[0] = 4

    param = {'A': A, 'b': b, 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = -1
    x0_not_std[2] = 3
    x0 = Q.to_normalized(x0_not_std)
    assert fun._get_e1(Q, x0) == -np.inf
    assert fun._get_e2(Q, x0) == 1 / 1.5  # we have a pole/zero cancellation


def test_f():
    dim = 6
    A = np.eye(dim)
    A[0, 0] = -0.5
    A[2, 2] = -0.1
    param = {'A': A, 'b': np.zeros(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 0
    x0_not_std[1] = 1
    x0 = Q.to_normalized(x0_not_std)

    F = fun.Fun(Q, x0)

    assert F.e1 == -1
    assert F.e2 == np.inf
    mu_1 = bisection(F, 1)

    my_newton(F, mu_1)

    x0_not_std[0] = 1
    x0 = Q.to_normalized(x0_not_std)
    F = fun.Fun(Q, x0)
    assert F.e2 == 2


def test_double_newton():

    dim = 6
    A = np.eye(dim)
    A[0, 0] = -0.5
    A[2, 2] = -2
    param = {'A': A, 'b': np.zeros(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 0
    x0_not_std[1] = 1
    x0 = Q.to_normalized(x0_not_std)
    F = fun.Fun(Q, x0)
    assert F.e1 == - 1
    assert F.e2 == np.inf

    double_newton(F)


def test_double_newton_2():
    dim = 6
    _A = np.random.rand(dim, dim)

    A = (_A + _A.T) / 2

    param = {'A': A, 'b': np.zeros(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 0
    x0_not_std[1] = 1
    x0 = Q.to_normalized(x0_not_std)
    F = fun.Fun(Q, x0)

    double_newton(F)
    mu_star, x_star = get_KKT_point_root(Q, x0_not_std)


def test_project():
    dim = 6
    _A = (np.random.rand(dim, dim)) * 2

    A = (_A + _A.T) / 2 - 3 * np.eye(dim)

    param = {'A': A, 'b': np.zeros(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 0
    x0_not_std[1] = 1
    project(Q, x0_not_std)


def test_project_2D():
    np.random.seed(42)
    dim = 2
    A = np.random.rand(dim, dim)
    A = A + A.T
    A[0, 0] = 2

    param = {'A': A, 'b': np.random.rand(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 0
    x0_not_std[1] = 3
    x0 = Q.to_normalized(x0_not_std)
    F = fun.Fun(Q, x0)
    x_project = project(Q, x0_not_std)
    x_expected = np.array([-0.836, 2.468])
    assert Q.is_feasible(x_project)
    assert np.linalg.norm(x_project - x_expected) < eps_test
    Q.plot()
    circle1 = plt.Circle(x0_not_std, F.dist(x_project), edgecolor='r', facecolor='None')
    ax = plt.gca()
    ax.add_artist(circle1)
    if SHOW:
        plt.scatter(x0_not_std[0], x0_not_std[1], c='black')
        plt.scatter(x_project[0], x_project[1], c='red')
        plt.show()
        plt.clf()
        plt.close()


def test_project_parabola_2():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([0, 2]).T
    c = -2
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    x0 = np.array([0, 1.1])

    fun.Fun(Q, x0)

    x_tild = project(Q, x0)
    x_tild_expected = np.array([0, 1])

    assert np.linalg.norm(x_tild - x_tild_expected) < eps_test

    fig, ax = Q.plot(show=False, show_principal_axes=True)
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_tild, flag_circle=True)
        plt.show()
    plt.close(fig)


def test_project_parabola():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([0, 2])
    c = -2
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)

    x0 = np.array([0, -1])
    x_tild_expected = np.array([1.4142, 0])

    x_tild = project(Q, x0)
    fig, ax = Q.plot(show=False, show_principal_axes=True)
    plot_x0_x_project(ax, Q, x0, x_tild, flag_circle=True)
    if SHOW:
        plt.show()
    assert Q.is_feasible(x_tild)
    F = fun.Fun(Q, x0)
    assert np.allclose(x_tild, x_tild_expected)

    x_test_f = np.random.rand(1)[0]
    assert F.f(x_test_f), F.f2(x_test_f)
    assert F.d_f(x_test_f), F.d_f2(x_test_f)

    x0 = np.array([0, -2])
    x_tild = project(Q, x0)
    x_tild_expected = np.array([2, -1])

    assert np.linalg.norm(x_tild - x_tild_expected) < eps_test

    fig, ax = Q.plot(show=False, show_principal_axes=True)
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_tild, flag_circle=True)
        plt.show()
    plt.close(fig)


def test_project_parabola_rotated():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([0, 2])
    c = -2
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)

    V = _get_unitary_matrix(2)
    A = V @ A @ V.T
    b = V @ b
    c = c
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    assert Q.is_parabola
    x0 = V @ np.array([0, -1])
    x_tild = project(Q, x0)
    x_tild_expected = V @ np.array([1.4142, 0])
    fig, ax = Q.plot(show=False, show_principal_axes=True)
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_tild, flag_circle=True)
        plt.show()
    assert np.allclose(abs(x_tild), abs(x_tild_expected))
    plt.close(fig)


def test_project_1D():
    A = np.array([[1]])
    b = np.array([2])
    c = -1
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)

    x0 = np.random.rand(1)
    x_tild = project(Q, x0)

    assert Q.is_feasible(x_tild)


def test_project_empty_quadric():
    dim = 6
    A = np.eye(dim)
    param = {'A': A, 'b': np.zeros(dim), 'c': 1}
    Q = Quadric(**param)

    assert Q.is_empty

    x0 = np.random.rand(dim)

    assert project(Q, x0) is None


def test_plot_3D():
    np.random.seed(40)
    dim = 3
    A = np.random.rand(dim, dim)
    A = A + A.T + 5
    A[0, 0] = 2

    param = {'A': A, 'b': np.random.rand(dim), 'c': -2}
    Q = Quadric(**param)

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 0
    x0_not_std[1] = 3
    x0 = Q.to_normalized(x0_not_std)
    fun.Fun(Q, x0)
    project(Q, x0_not_std)
    Q.plot(show=SHOW)


def test_elliptic_paraboloid():
    A = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    b = np.array([0, 2, 1]).T
    c = -2
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    assert Q.is_elliptic_paraboloid
    x0 = np.array([0, 1.1, 1])
    x_project = project(Q, x0)

    assert Q.is_feasible(x_project)
    fig, ax = Q.plot()

    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)

    x_tild_expected = np.array([0, 0.418, 0.8143])

    assert np.linalg.norm(x_project - x_tild_expected) < eps_test
    test_starting_point_from_feasible_point(dim=3, param=param)


def test_elliptic_paraboloid_2():
    A = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    V = _get_unitary_matrix(3)
    A = V @ A @ V.T
    b = V @ np.array([0, 2, 1]).T
    c = -2
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    assert Q.is_elliptic_paraboloid
    x0 = V @ np.array([0, 1.1, 1])
    x_project = project(Q, x0)

    x_tild_expected = V @ np.array([0, 0.418, 0.8143])

    assert np.linalg.norm(x_project - x_tild_expected) < eps_test
    assert Q.is_feasible(x_project)
    fig, ax = Q.plot()

    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)


def test_elliptic_paraboloid_3():
    np.random.seed(1)
    A = np.array([[1, 0, 0], [0, 4, 0], [0, 0, 0]])
    V = _get_unitary_matrix(3)
    A = V @ A @ V.T
    b = V @ np.array([-0.81, 2.1, 0.34]).T
    c = -2
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    assert Q.is_elliptic_paraboloid
    x0 = np.array([-1, 1.1, 1])
    x_project = project(Q, x0)

    assert Q.is_feasible(x_project)
    fig, ax = Q.plot()

    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close()


def test_elliptic_paraboloid_4():
    np.random.seed(1)
    A = np.array([[1, 0, 0], [0, 4, 0], [0, 0, 0]])
    V = _get_unitary_matrix(3)
    A = V @ A @ V.T
    b = V @ np.array([-0.81, 2.1, 0.34]).T
    c = 2
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    print("Q", Q)
    assert Q.is_elliptic_paraboloid
    x0 = np.array([-1, 1.1, 1])
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)

    fig, ax = Q.plot()

    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close()


def test_elliptic_paraboloid_projection_degenerated():
    np.random.seed(1)
    A = np.array([[1, 0, 0], [0, 4, 0], [0, 0, 0]])
    b = np.array([0, 0, -1])
    c = 0
    param = {'A': A, 'b': b, 'c': c}
    Q = Quadric(**param)
    print("Q", Q)
    assert Q.is_elliptic_paraboloid
    x0 = np.array([0, 0, 1])
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)

    fig, ax = Q.plot()

    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close()
    x_tild_expected = np.array([0, 0.46770717, 0.875])
    assert np.allclose(x_project, x_tild_expected)

    x0 = np.array([0, 0, -1])
    x_project = project(Q, x0)
    fig, ax = Q.plot()

    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close()
    x_tild_expected = np.array([0, 0, 0])
    assert np.allclose(x_project, x_tild_expected)


def test_starting_point_from_feasible_point(dim=3, param=None, show=False):

    if param is None:
        param = _get_random_param(dim)

    Q = Quadric(**param)
    if Q.is_empty:
        return
    dim = Q.dim
    print("Master quadric type", Q.type)

    _x0 = np.random.rand(dim) - 0.5

    tol = 10e-10 * dim**2

    x_project = project(Q, _x0)
    assert Q.is_feasible(x_project, tol=tol)
    x0 = Q.get_starting_point_from_feasible_point(x_project)

    x_project_2 = project(Q, x0)
    if not Q.is_feasible(x_project_2, tol):
        F = fun.Fun(Q, Q.to_normalized(x0))
        x = np.linspace(-5, 5)
        y = np.zeros_like(x)
        for i, t in enumerate(x):
            y[i] = F.f(t)
        fig = plt.figure()
        plt.plot(x, y)
        plt.show()
        plt.close(fig)
    assert Q.is_feasible(x_project_2, tol)

    flag_raise = not Q.is_feasible(x_project_2)
    if np.linalg.norm(x_project - x_project_2) > eps_test:
        if np.linalg.norm(x_project_2 - x0) > np.linalg.norm(x_project - x0) + eps_test:
            flag_raise = True

    if Q.dim not in [2, 3]:
        if flag_raise:
            raise ValueError
        return

    if flag_raise:
        F = fun.Fun(Q, x0)
        F.plot()
        plt.show()
        plt.close()

    if SHOW or flag_raise:
        fig, ax = Q.plot(show_principal_axes=True)
        ax.scatter(x_project[0], x_project[1], color="purple")
        plot_x0_x_project(ax, Q, x0, x_project_2, flag_circle=True)
        plt.show()
        plt.close(fig)
    if flag_raise:
        raise ValueError
    assert Q.is_feasible(x_project_2)


def test_projection_hyperboloid():
    for dim in range(2, 20):
        test_starting_point_from_feasible_point(dim)


def test_projection_paraboloid():
    np.random.seed(42)

    for dim in range(2, 40):
        param = _get_random_param(dim, quadric_type="paraboloid")
        Q = Quadric(**param)
        test_starting_point_from_feasible_point(dim, param)
        assert Q.is_parabolic


def test_projection_ellipsoid():
    for dim in range(2, 50):
        param = _get_random_param(dim, quadric_type="ellipsoid")
        Q = Quadric(**param)
        assert Q.is_ellipsoid
        test_starting_point_from_feasible_point(dim, param)


def test_projection_paraboloid_2():
    np.random.seed(4)
    for dim in range(2, 50):
        param = _get_random_param(dim, quadric_type="paraboloid")
        param['c'] = 1
        Q = Quadric(**param)
        assert Q.is_parabolic
        test_starting_point_from_feasible_point(dim, param)


def test_projection_paraboloid_3():
    for dim in range(3, 50):

        param = _get_random_param(dim, quadric_type="paraboloid")
        param['c'] = (np.random.rand(1)[0] - 0.5) * 10
        Q = Quadric(**param)
        assert Q.is_parabolic

        test_starting_point_from_feasible_point(dim, param, show=False)


def test_single_hyperbolic_paraboloid():
    A = np.diag(np.array([0.647667, 0, -0.09]))
    b = np.array([-1.92168105, -0.55112181, 1.83034102])
    c = -0.31
    x0 = [2.49155525, 4.12922539, 1.31971592]
    Q = Quadric(A=A, b=b, c=c)

    x_project = project(Q, x0)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=False)
        plt.show()
    plt.close()


def test_single_paraboloid_2():
    A = np.diag(np.array([0.8856, 0, -0.005672]))
    b = np.array([-0.332, -1.3667, -1.796])
    c = 0.3915
    x0 = [0, 0, 1]
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_hyperbolic_paraboloid

    x_project = project(Q, x0)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=False)
        plt.show()
    plt.close(fig)


def test_hyperbola():
    A = np.diag(np.array([1.8856, -1.005672]))
    b = np.array([4.332, 1.796])
    c = -0.3915
    x0 = [0, 1]
    Q = Quadric(A=A, b=b, c=c)
    assert Q.gamma < 0

    x_project = project(Q, x0)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=False)
        plt.show()
    plt.close(fig)


def test_hyperbola_2():
    A = np.diag(np.array([1.8856, -1.005672]))
    b = np.array([0.332, 1.796])
    c = -0.3915
    x0 = [0, 1]
    Q = Quadric(A=A, b=b, c=c)

    x_project = project(Q, x0)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=False)
        plt.show()
    plt.close(fig)


def test_hyperbola_degenerated():
    A = np.diag(np.array([2, 0]))
    b = np.array([0, -3])
    c = -1
    x0 = [0, 1]
    Q = Quadric(A=A, b=b, c=c)

    x_project = project(Q, x0)
    x_expected = np.array([0.93541435, 0.25])
    assert np.allclose(x_project, x_expected)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=False)
        plt.show()
    plt.close(fig)


def test_projection_empty_parallel_plane():
    A = np.array([[-1, 0], [0, 0]])
    b = np.zeros(2)
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.zeros(2)

    assert Q.is_empty
    x_project = project(Q, x0)
    assert x_project is None


def test_projection_single_line():
    A = np.array([[1, 0], [0, 0]])
    b = np.array([-2, 0])

    c = 1
    param = {"A": A, "b": b, "c": c}

    test_starting_point_from_feasible_point(2, param, show=SHOW)


def test_projection_parallel_lines():
    np.random.seed(456)

    A = np.array([[1, 0], [0, 0]])
    b = np.array([0, 0])

    c = -1
    param = {"A": A, "b": b, "c": c}

    test_starting_point_from_feasible_point(2, param, show=SHOW)

    A = np.array([[1, 0], [0, 0]])
    b = np.array([1, 0])

    c = -1
    param = {"A": A, "b": b, "c": c}

    test_starting_point_from_feasible_point(2, param, show=SHOW)

    A = np.array([[1, 1], [1, 1]])

    b = np.array([0, 0])

    c = -1
    param = {"A": A, "b": b, "c": c}

    test_starting_point_from_feasible_point(2, param, show=SHOW)


def test_projection_ellipsoid_cylinder():
    param = {}
    param['A'] = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    param['b'] = np.array([0, 2, 0])
    param['c'] = -1.5
    Q = Quadric(**param)
    x0 = np.random.rand(3)

    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    test_starting_point_from_feasible_point(3, param, show=SHOW)


def test_projection_ellipsoid_cylinder_2():
    param = {}
    A = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    b = np.array([0, 2, 0])
    V = _get_unitary_matrix(3)
    param['A'] = V @ A @ V.T
    param['b'] = V @ b
    param['c'] = -1.5
    Q = Quadric(**param)
    x0 = np.random.rand(3) * 5

    assert Q.is_ellipsoid_cylinder
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    test_starting_point_from_feasible_point(3, param, show=SHOW)

    x0 = np.random.rand(3) * 0.1
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    test_starting_point_from_feasible_point(3, param, show=SHOW)


def test_projection_ellipsoid_cylinder_3():
    A = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
    b = np.array([0, 0, 0])
    c = -1.5
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_ellipsoid_cylinder
    x0 = np.array([1, 0, 0])

    x_project = project(Q, x0)
    x_expected = np.array([np.sqrt(1.5), 0, 0])
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)
    assert np.allclose(x_project, x_expected)

    x0 = np.array([1, 0, 6])
    x_project = project(Q, x0)
    x_expected = np.array([np.sqrt(1.5), 0, 6])
    assert np.allclose(x_project, x_expected)

    x0 = np.array([0, 0, 6])
    x_project = project(Q, x0)
    x_expected = np.array([0, np.sqrt(1.5 / 2), 6])
    assert np.allclose(x_project, x_expected)


def test_projection_hyperboloid_cylinder():
    A = np.array([[2, 0, 0], [0, -1, 0], [0, 0, 0]])
    b = np.array([0, 0, 0])
    c = -1.5
    param = {"A": A, "b": b, "c": c}
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_hyperboloid_cylinder
    x0 = np.array([1, 1, 0.1])

    x_project = project(Q, x0)
    x_expected = np.array([1.09901097, 0.95689615, 0.1])
    assert np.allclose(x_project, x_expected)

    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)

    test_starting_point_from_feasible_point(3, param)

    A = np.array([[-1, 0, 0], [0, 2, 0], [0, 0, 0]])
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.array([1, 1, 0.1])

    x_project = project(Q, x0)
    x_expected = np.array([0.95689615, 1.09901097, 0.1])
    assert np.allclose(x_project, x_expected)

    A = np.array([[-1, 0, 0], [0, 0, 0], [0, 0, 2]])
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.array([1, 0.1, 1])

    x_project = project(Q, x0)
    x_expected = np.array([0.95689615, 0.1, 1.09901097])
    assert np.allclose(x_project, x_expected)


def test_get_random_param():
    param = _get_random_param(dim=10, quadric_type="ellipsoid", n_cylinder_indices=1)
    Q = Quadric(**param)
    assert Q.is_ellipsoid_cylinder or Q.is_empty

    param = _get_random_param(dim=3, quadric_type="hyperboloid", n_cylinder_indices=1)
    Q = Quadric(**param)
    assert Q.is_hyperboloid_cylinder or Q.is_empty

    param = _get_random_param(dim=4, quadric_type="paraboloid", n_cylinder_indices=1)
    Q = Quadric(**param)
    assert Q.is_paraboloid_cylinder or Q.is_empty

    assert Q.is_cylindrical or Q.is_empty


def test_projection_elliptic_paraboloid():
    np.random.seed(1)
    A = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])  # + TODO all negative
    b = np.zeros(3)
    b[2] = -1
    c = 0  # TODO non zero c
    param = {"A": A, "b": b, "c": c}
    Q = Quadric(**param)

    x0 = np.random.rand(3)

    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    test_starting_point_from_feasible_point(3, param)


def test_projection_elliptic_paraboloid_2():
    np.random.seed(1)
    A = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])  # + TODO all negative
    b = np.array([1, 2, 3, 4])
    c = 0
    param = {"A": A, "b": b, "c": c}
    Q = Quadric(**param)

    x0 = np.random.rand(4)

    x_project = project(Q, x0)

    assert Q.is_elliptic_paraboloid

    assert Q.is_feasible(x_project)


def test_projection_elliptic_paraboloid_3():
    np.random.seed(1)
    A = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    b = np.array([1, 2, 3, 4])
    c = -1
    param = {"A": A, "b": b, "c": c}
    Q = Quadric(**param)

    x0 = np.random.rand(4)

    x_project = project(Q, x0)

    assert Q.is_elliptic_paraboloid

    assert Q.is_feasible(x_project)
    test_starting_point_from_feasible_point(3, param)
    param = {"A": A, "b": -b, "c": c}
    test_starting_point_from_feasible_point(3, param)
    param = {"A": -A, "b": -b, "c": c}
    test_starting_point_from_feasible_point(3, param)


def test_projection_hyperbolic_paraboloid():
    A = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
    b = np.zeros(3)
    b[2] = -1
    c = 0
    param = {"A": A, "b": b, "c": c}
    Q = Quadric(**param)

    x0 = np.random.rand(3)

    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    test_starting_point_from_feasible_point(3, param)


def test_projection_paraboloid_cylinder():
    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([0, 0, 1])
    c = -1
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.array([3, 0, 6])

    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    x_expected = np.array([0.26918101, 0., 0.92754158])
    assert np.allclose(x_project, x_expected)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)

    x0 = np.array([4, 0, 1])

    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)

    x0 = np.array([2, 3, 1])
    b = np.array([0, 0, 2])
    Q = Quadric(A=A, b=b, c=c)

    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)


    x0 = np.array([0, 2, 1])
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    assert np.allclose(x_project, [0, 2, 0.5])
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)

    x0 = np.array([0, 2, -1])
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    assert np.allclose(x_project, [1, 2, 0])
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)
    test_starting_point_from_feasible_point(3, {"A": A, "b": b, "c": c})


def test_projection_paraboloid_cylinder_rotated():

    A = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    b = np.array([0, 0, 1])
    c = -1
    V = _get_unitary_matrix(3)
    V = np.array([[-0.10073711, 0.34496094, 0.93319558],
                  [-0.99367317, 0.01192878, -0.11167512],
                  [0.04965544, 0.93854124, -0.34157676]])

    A = V @ A @ V.T
    b = V @ b
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_paraboloid_cylinder

    x0 = V @ np.array([3, 0, 6])
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)
    x_expected = V @ np.array([0.26918101, 0., 0.92754158])

    assert np.allclose(x_project, x_expected)

    x0 = np.array([3, 0, 1])

    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)
    test_starting_point_from_feasible_point(3, {"A": A, "b": b, "c": c})


def test_one_sheet_hyperboloid():
    A = np.array([[2, 0, 0], [0, -1, 0], [0, 0, -1.5]])
    b = np.array([0, -1, 1])
    c = 1
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.random.rand(3)
    x_project = project(Q, x0)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)


def test_elliptic_cone_2D():
    np.random.seed(17)
    A = np.array([[2, 0], [0, -1.5]])
    b = np.array([0, 0])
    c = 0
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_elliptic_cone
    x0 = np.random.rand(2)
    x_project = project(Q, x0)
    assert np.allclose(x_project, [0.38885735, 0.44901379])

    x0 = np.array([1, 0])
    x_project = project(Q, x0)
    assert np.allclose(x_project, [0.42857143, 0.49487166])

    x0 = np.array([0, 1])
    x_project = project(Q, x0)

    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)


def test_elliptic_cone():
    A = np.array([[2, 0, 0], [0, 1, 0], [0, 0, -1.5]])
    b = np.array([0, 0, 0])
    c = 0
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_elliptic_cone
    x0 = np.random.rand(3)
    x_project = project(Q, x0)
    fig, ax = Q.plot()
    if SHOW:
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()
    plt.close(fig)


def test_elliptic_cone_nonzero_c():
    A = np.array([[2, 0, 0], [0, 1, 0], [0, 0, -1.5]])
    b = np.array([0, 1, 0])
    c = b.T @ np.linalg.inv(A) @ b / 4  # such that extended matrix loose one rank
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_elliptic_cone
    x0 = np.random.rand(3)
    x_project = project(Q, x0)
    if SHOW:
        fig, ax = Q.plot()
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()


def test_cylinder_elliptic_cone():
    np.random.seed(17)
    A = np.array([[2, 0, 0], [0, 0, 0], [0, 0, -1.5]])
    b = np.array([0, 0, 0])
    c = 0
    Q = Quadric(A=A, b=b, c=c)
    assert Q.is_elliptic_cone_cylinder
    x0 = np.random.rand(3)
    x_project = project(Q, x0)
    assert np.allclose(x_project, [0.22106321, 0.53058676, 0.25526181])

    x0 = np.random.rand(3) * 0
    x0[0] = 1
    x_project = project(Q, x0)
    assert np.allclose(x_project, [0.42857143, 0, 0.49487166])
    if SHOW:
        fig, ax = Q.plot()
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()


def test_rotated_elliptic_cone():
    A = np.array([[2, 0, 0], [0, 1, 0], [0, 0, -1.5]])
    V = _get_unitary_matrix(3)
    A = V @ A @ V.T
    b = np.array([0, 0, 0])
    c = 0
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.random.rand(3)
    x_project = project(Q, x0)
    if SHOW:
        fig, ax = Q.plot()
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()


def test_shifted_elliptic_cone():
    np.random.seed(5)
    A = np.array([[2, 0, 0], [0, 1, 0], [0, 0, -1.5]])
    d = np.array([1, 2, 3.4])
    b = np.array([2 * A[0, 0] * d[0], 2 * A[1, 1] * d[1], +2 * A[2, 2] * d[2]])
    c = A[0, 0] * d[0]**2 + A[1, 1] * d[1]**2 + A[2, 2] * d[2]**2
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.random.rand(3) - d
    assert Q.is_feasible(-d)
    x_project = project(Q, x0)
    assert np.allclose(x_project, np.array([-0.87728319, -1.38003831, -2.87434401]))
    if SHOW:
        fig, ax = Q.plot()
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()


def test_rotated_and_shifted_elliptic_cone():
    np.random.seed(5)
    A = np.array([[2, 0, 0], [0, 1, 0], [0, 0, -1.5]])
    V = _get_unitary_matrix(3)
    d = np.array([1, 2, 3.4])
    c = A[0, 0] * d[0]**2 + A[1, 1] * d[1]**2 + A[2, 2] * d[2]**2
    b = V @ np.array([2 * A[0, 0] * d[0], 2 * A[1, 1] * d[1], +2 * A[2, 2] * d[2]])
    A = V @ A @ V.T
    Q = Quadric(A=A, b=b, c=c)
    x0 = np.random.rand(3) - d
    x_project = project(Q, x0)
    x_expected = np.array([0.06306791, -0.44393374, -1.1029644])
    assert np.allclose(x_project, x_expected)
    if SHOW:
        fig, ax = Q.plot()
        plot_x0_x_project(ax, Q, x0, x_project, flag_circle=True)
        plt.show()


def test_hyperboloid_cylinder():
    A = np.array([[2, 0, 0], [0, -1, 0], [0, 0, 0]])
    b = np.array([0, 0, 0])
    c = 2.1

    Q = Quadric(**{'A': A, 'b': b, 'c': c})

    x0 = np.array([0.5, -2, 0])
    x_project = project(Q, x0)
    fig, ax = Q.plot(show_principal_axes=True, flag_circle=True)
    plot_x0_x_project(ax, Q, x0, x_project)
    if SHOW:
        plt.show()
        plt.close()


def test_hyperboloid_cylinder_2():
    A = np.array([[2, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    b = np.array([1, 2, 0, 0])
    c = 2.1
    V = _get_unitary_matrix(4)

    A2 = V @ A @ V.T
    b2 = V @ b

    Q = Quadric(**{'A': A2, 'b': b2, 'c': c})
    assert Q.is_hyperboloid_cylinder

    x0 = np.array([1, -2, 0, 1])
    x_project = project(Q, x0)
    assert Q.is_feasible(x_project)


def _get_random_param_std(dim, quadric_type="hyperboloid", n_cylinder_indices=0):
    eig = np.random.randn(dim)
    b = np.random.rand(dim)

    if quadric_type == "paraboloid":
        p = dim - np.random.randint(1 + n_cylinder_indices, dim)
        eig[:-p] = 0
    elif quadric_type == "ellipsoid":
        min_eigenvalue = min(eig)
        if min_eigenvalue < 0:
            eig = eig - min_eigenvalue * 2
    eig[:n_cylinder_indices] = 0
    b[:n_cylinder_indices] = 0

    if quadric_type == "hyperboloid":
        if min(eig) * max(eig) >= 0:
            if min(eig) > 0:
                min_eig_idx = np.argmin(eig)
                eig[min_eig_idx] = -min_eig_idx
            else:
                max_eig_idx = np.argmax(eig)
                eig[max_eig_idx] = -max_eig_idx
    L = np.diag(eig)
    c = - np.random.rand(1)[0]
    return L, b, c


def _get_random_param(dim, quadric_type="hyperboloid", n_cylinder_indices=0):

    assert n_cylinder_indices < dim, "Cannot have all indices to be cylindrical"

    V = _get_unitary_matrix(dim)

    assert np.allclose(np.eye(dim), V @ V.T)

    L, b, c = _get_random_param_std(dim, quadric_type, n_cylinder_indices)
    param = {'A': L, 'b': b, 'c': c}

    A = V @ L @ V.T
    b2 = V @ b
    param = {'A': A, 'b': b2, 'c': c}

    return param


def _get_unitary_matrix(dim):
    return ortho_group.rvs(dim=dim)
