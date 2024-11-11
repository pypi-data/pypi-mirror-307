#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import quadproj.fun as fun

"""

This module provides functions to project or
quasi-project a point to a `Quadric` object.


"""


class NoFeasibleDirection(Exception):
    """
    Python-exception-derived object raised by `quadproj.project` functions.

    Raised when no feasible direction are available for computing the
    quasi-projection.


    """
    pass


eps = pow(10, -10)


def get_poles(Q_std, x0_std):
    """Find all poles of a rational function.
    """
    poles = []
    for i, lambd in enumerate(Q_std.eig):
        if np.abs(x0_std[i]) > eps:
            poles.append(-1 / lambd)
    return poles


def project_1d(Q, x0_not_std):
    a = Q.A[0][0]
    b = Q.b[0]
    c = Q.c
    x_sol = np.roots([a, b, c])

    if x_sol.size == 0:
        raise ValueError("No solution")  # TODO LVH
    elif x_sol.size == 1:
        return x_sol

    x_1, x_2 = x_sol
    if abs(x_1 - x0_not_std) <= abs(x_2 - x0_not_std):
        return x_1
    return x_2


def project(Q, x0_not_std, flag_get_all_KKT=False):
    """Project a point to a quadric

        Given a matrix Q and a non-standardized
        point `x0_not_std`, this function computes one of the projection of
        x0 onto Q.


        Parameters
        ----------
        Q : Quadric instance
            The quadric onto which the point x0 has to be projected.
        x0_not_std : ndarray
            1-D ndarray containing the (not standardized) point to be projected.
        flag_get_all_KKT : bool, default False
            Whether we return all KKT points or not.

        Returns
        _______
        x_project_not_std : ndarray
            1-D ndarray like x0_not_std containing the (not standardized) projection.


        """

    class ProjectOutput():
        """Output object
        TODO

        Along with the projected point, this object contains all KKT points
        including the projection (`ProjectOutput.min`)
        and the point the furthest away (`ProjectOutput.max`).

        """
        def __init__(self):
            self.min = None
            self.max = None
            self.xd = []
            self.x_roots = []

    if Q.is_empty:
        return None
    if Q.is_feasible(x0_not_std):
        return x0_not_std
    if Q.dim == 1:
        return project_1d(Q, x0_not_std)

    x0 = Q.to_normalized(x0_not_std)

    Xd = []
    F = fun.Fun(Q, x0)

    mu_star, x_star = get_KKT_point_root(Q, x0_not_std)

    if mu_star is not None:
        Xd.append(x_star)
    eig = list(Q.eig)
    eig_bar = list(reversed(Q.eig_bar))  # in increasing order!
    i = Q.dim - 1
    for k, eig_bar_k in enumerate(eig_bar):
        L_k = []
        while i >= 0 and abs(eig[-1] - eig_bar_k) < eps:
            eig.pop()
            L_k.append(i)
            i -= 1
        K_k = [i2 for i2 in L_k if abs(Q.eig[i2]) > eps and abs(x0[i2]) < eps]

        if L_k and len(L_k) == len(K_k):
            squared_radius_k = get_squared_radius_k(Q, x0, L_k, eig_bar_k)
            if squared_radius_k > 0:
                xd_k = get_xd_k(Q, x0, K_k, eig_bar_k)
                xd_k_not_std = Q.to_non_normalized(xd_k)
                Xd.append(xd_k_not_std)
    if Q.is_conical:
        Xd.append(Q.d)
    for xd in Xd:
        if np.any(np.isnan(xd)):
            Xd.remove(xd)
    if not Xd:
        raise Q.EmptyQuadric()

    x_project_not_std = min(Xd, key=(F.dist))
    if not Q.is_feasible(x_project_not_std):
        if abs(Q.evaluate_point(x_project_not_std)) > pow(10, -4):  # TODO TO REMOVE
            if Q.dim < 4:
                fig, ax = Q.plot()
                plot_x0_x_project(ax, Q, x0_not_std, x_project_not_std, flag_circle=True)
                plt.show()

            raise ValueError("Obtained solution is not feasible... Something wrong happened.")
    return x_project_not_std


def get_KKT_point_root(Q, x0_not_std):
    """Get the root-based KKT point

        Given a quadric Q with a non-standardized
        point `x0_not_std`, this function computes the KKT point issued from the
        the root of the secular function.

        If no such root exists, then the function returns `None`, `None`.


        Parameters
        ----------
        Q : Quadric instance
            The quadric onto which the point x0 has to be projected.
        x0_not_std : ndarray
            1-D ndarray containing the (not standardized) point to be projected.

        Returns
        _______
        mu_star : float
            The root of the secular equation associated to one KKT point of the projection
        x_star_not_std : ndarray
            The point associated to Lagrange multiplier `mu_star`.

        """
    x0 = Q.to_normalized(x0_not_std)
    F = fun.Fun(Q, x0)
    if F.e1 != -np.inf:
        if F.e2 == np.inf:
            mu_1 = bisection(F, 1)
            output_newton = my_newton(F, mu_1)
        else:
            output_newton = double_newton(F)

    elif Q.is_parabolic:
        if F.e2 == np.inf:
            mu_1 = 0
            output_newton = my_newton(F, mu_1)

        else:
            mu_1 = bisection(F, -1)
            output_newton = my_newton(F, mu_1)
    else:
        return None, None
    mu_star = output_newton.x

    x_star_not_std = F.x_not_std(mu_star)

    if np.any(np.isnan(x_star_not_std)):
        print("Warning: detected a Nan as the result of the secular equation,\
              returning None instead.")
        return None, None
    return mu_star, x_star_not_std


def get_squared_radius_k(Q, x0, L_k, eig_bar_k):
    """Compute the degenerate solution radius.

    This function computes de square of the hypersphere radius (which may not exist)
    containing the KKT point associated to the degeneration in directions
    :math:`k \\in K_k`.

    It is possible that no (degenerated) points arise from the degeneration,
    in this case the returned (squared) radius is negative.

    Remark that this (squared) radius does not correspond to the distance to the
    objective.


    .. math:: r_k =  \\frac{1}{\\overline{\\lambda}_k} \\Big ( 1- \\sum_{j\\in I \\setminus K_{k}} \\lambda_j \\Big( \\frac{x^0_j}{1-\\lambda_j / \\overline{\\lambda}_k} \\Big)^2 \\Big )

    Parameters
    ----------
    Q : Quadric instance
        The quadric onto which the point x0 has to be projected.
    x0 : ndarray
        1-D ndarray containing the (standardized) point to be projected.
    L_k : list of int
        Indices of direction with eigenvalue `eig_bar_k`.
    K_k : list of int
        Subset of `L_k` with associated `x0` component equal to zero.

    Returns
    _______
    radius_k : float
        Length of the squared radius of the hypersphere that is the set of
        the KKT points associated to the degeneration direction.

    """
    mu_k = -1 / eig_bar_k
    b2 = Q.P_inv @ Q.b_norm / 2

    _sum = [Q.eig[j] * (x0[j] / (1 - Q.eig[j] / eig_bar_k))**2
            for j in range(Q.dim) if j not in L_k and j in Q.nonzero_ev_indices]
    _sum2 = [Q.b_norm[j] * (x0[j] - b2[j] * mu_k)
             for j in range(Q.dim) if j not in L_k and j in Q.zero_ev_indices]
    radius_k = 1 / eig_bar_k * (-Q.c_norm - sum(_sum) - sum(_sum2))
    return radius_k


def get_xd_k(Q, x0, K_k, eig_bar_k):
    """Compute one of the degenerate solution.

    This function computes the KKT point associated to the degeneration in directions
    :math:`k \\in K_k`.

    The set of solution is a hypersphere of dimension `len(K_k)`
    (with only two points for K_k a singleton).

    Here, we only returns one solution by arbitrarily setting all except one
    components to zero.

    By convention, we chose as a nonzero component the smallest index of `K_k`.



    Parameters
    ----------
    Q : Quadric instance
        The quadric onto which the point x0 has to be projected.
    x0 : ndarray
        1-D ndarray containing the (standardized) point to be projected.
    L_k : list of int
        Indices of direction with eigenvalue `eig_bar_k`.
    K_k : list of int
        Subset of `L_k` with associated `x0` component equal to zero.

    Returns
    _______
    radius_k : float
        Length of the squared radius of the hypersphere that is the set of
        the KKT points associated to the degeneration direction.

    """
    xd_k = np.zeros_like(x0)
    k_prime = K_k[0]

    b2 = Q.P_inv @ Q.b_norm / 2
    for i, x0_i in enumerate(x0):
        if i not in K_k:
            xd_k[i] = x0_i / (1 - Q.eig[i] / eig_bar_k) + b2[i] / eig_bar_k
        elif i == k_prime:
            squared_radius_k = get_squared_radius_k(Q, x0, K_k, eig_bar_k)
            xd_k[i] = np.sqrt(squared_radius_k)

    return xd_k


def bisection(F, sign=1):
    """Compute point with a given sign.

    This function:

    *   either (`sign = 1`) starts from `F.e1` :math:`= e_1` (with :math:`f(e_1) \\to \\infty`)
        and returns some mu :math:`= \\mu \\in [e_1, e_2]` such that :math:`f(\\mu) <0`;
    *   or (`sign = -1`) starts from `F.e2` :math:`= e_2` (with :math:`f(e_2) \\to -\\infty`)
        and returns some mu :math:`= \\mu \\in [e_1, e_2]` such that :math:`f(\\mu) >0`.

    Parameters
    ----------
    F : Fun instance
        Function object associated to some quadric instance.
    sign : {-1, 1}
        Whether we want to find a negative or a positive value.

    Returns
    _______
    mu : float
        Point with corresponding sign.

    """
    if sign == 1:
        direction = 'right'
    elif sign == -1:
        direction = 'left'
    else:
        raise ValueError('Illegal arguement sign={sign} but should be 1 or -1.')
    k = 1

    half_interval_length = (F.e2 - F.e1)
    if np.isinf(half_interval_length):
        half_interval_length = 1

    if direction == 'right':
        mu = F.e1 + half_interval_length
        while F.f(mu) < 0:
            mu = F.e1 + pow(10, -k) * half_interval_length
            k += 1
    else:
        mu = F.e2 - 1 * half_interval_length

        while F.f(mu) > 0:
            mu = F.e2 - pow(10, -k) * half_interval_length
            k += 1

    assert np.sign(F.f(mu)) == sign, 'Failed bisection'

    if mu > F.e2 or mu < F.e1:
        F.plot()

    assert mu < F.e2 and mu > F.e1, "Outside of interval"

    return mu


def my_newton(F, mu_0, **hist):
    """Newton-raphson root-finding algorithm.

    Starting from `mu_0` this functions computes a root of `F.f` inside
    [F.e1, F.e2].

    If any iterate steps out of the search interval, the algorithm stops
    without providing roots.

    Parameters
    ----------
    F : Fun instance
        Function object associated to some quadric instance.
    mu_0 : float
        Starting point.

    Returns
    _______
    output : Output instance
        Object containing the solver status.

    """

    output = SolverOutput()
    iteration_max = 100
    eps_rtol = pow(10, -10)
    eps_xtol = pow(10, -14)
    x = mu_0
    output.x0 = mu_0
    output.interval = F.interval
    new_x = x
    while (output.iteration < iteration_max and output.rtol > eps_rtol and
           output.xtol > eps_xtol and output.is_in_interval(F.interval)):
        output.fx = F.f(x)
        output.dfx = F.d_f(x)
        if abs(output.dfx) < eps_rtol and abs(output.fx) > 0.1:
            if hist.get("df"):
                df_replacement = hist["df"][-1]
            else:
                df_replacement = np.random.randn(1)[0]

            new_x = x - output.fx / df_replacement
        else:
            new_x = x - output.fx / output.dfx  # what if we're on a max/min???
        output.xtol = abs(x - new_x)
        x = new_x
        output.x = new_x
        output.rtol = abs(output.fx)
        output.iteration += 1
        if hist:
            hist['df'].append(output.dfx)
            hist['f'].append(output.fx)
            hist['x'].append(new_x)

    output.converged = False
    if output.iteration == iteration_max:
        output.message = "max number of iteration reached"
    elif output.rtol <= eps_rtol:
        output.message = "converged"
        output.converged = True
    elif output.xtol <= eps_xtol:
        output.message = "weak improvement, stopping the alg early.\
                You may want to check the value of the derivative around the root"
    elif not output.is_in_interval(F.interval):
        output.message = "Point is outside the interval of research"

    return output


def double_newton(F, **hist):
    """Root-finding algorithm using up to two Newton schemes.

    Given the interval :math:`\\mathcal{I} = ]e_1, e_2[`, it \
    is proven that there is at most one root.

    Parameters
    ----------
    F : Fun instance
        Function object associated to some quadric instance.
    mu_0 : float
        Starting point.

    Returns
    _______
    output : Output instance
        Object containing the solver status.

    """

    # Check if Newton starting from 0 works...
    # print('**** Launching first netwon ****')
    output = my_newton(F, 0, **hist)
    # print('**** End first netwon ****')
    if output.converged:
        output.message += " starting from mu_s = 0"
        return output

    if F.f(0) < 0:
        # print("Bisection right")
        mu_s = bisection(F, 1)
        # print("End bisection right")
    elif F.f(0) > 0:
        # print("Bisection left")
        mu_s = bisection(F, -1)
        # print("End bisection left")
    else:
        mu_s = 0
    # removing history of previous newton
    if hist:
        hist['f'].clear()
        hist['x'].clear()
    # print('**** Launching second netwon ****')
    output = my_newton(F, mu_s, **hist)
    # print('**** End second netwon ****')
    output.message += f" starting from mu_s = {mu_s}"

    return output


def plot_x0_x_project(ax, Q, x0, x_project, flag_circle=False):
    """Plot a point and its projection onto a quadric.

    This function plot on the `matplotlib.axes` ax the point x0
    and the point x_project, supposedly the projection of x0 onto
    Q.

    As a way to check whether the projection is correct and without
    being troubled with the axis scaling, setting `flag_circle=True`
    also plot a (topological) ball of radius ||x0-x_project|| that is
    centred in x0.

    Parameters
    ----------
    ax : matplotlib.axes
        The ax object where to (scatter) plot the points.
    Q : quadproj.quadrics.Quadric instance
        The quadric object.
    x0 : ndarray
        1D-ndarray of size `Q.dim`, point to be projected.
    x_project : ndarray
        1D-ndarray of size `Q.dim`, projected point.
    flag_circle : bool
        Whether we plot the red ball to check the optimality of x_project.
    Returns
    -------
    ax : matplotlib.axes
        The (plotted) axis.
    """
    if Q.dim == 2:
        ax.scatter(x0[0], x0[1], color='black', label=r'$x^0$')
        ax.scatter(x_project[0], x_project[1], color='red', zorder=2,
                   label=r'$\mathrm{P}_{\mathcal{Q}} (x^0)$')
        ax.legend()
        F = fun.Fun(Q, Q.to_normalized(x0))
        if flag_circle:
            circle = plt.Circle(x0, F.dist(x_project), edgecolor='r', facecolor='None',
                                linestyle='--')
            ax = plt.gca()
            ax.add_artist(circle)
    elif Q.dim == 3:
        ax.scatter3D(x0[0], x0[1], x0[2], color='black', label=r'$x^0$')
        ax.scatter(x_project[0], x_project[1], x_project[2], color='red', zorder=2,
                   label=r'$\mathrm{P}_{\mathcal{Q}} (x^0)$')
        ax.legend()
        F = fun.Fun(Q, Q.to_normalized(x0))
        if flag_circle:
            r = F.dist(x_project)
            u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
            x = r * np.cos(u) * np.sin(v) + x0[0]
            y = r * np.sin(u) * np.sin(v) + x0[1]
            z = r * np.cos(v) + x0[2]
            ax.plot_wireframe(x, y, z, color='red', alpha=0.3)

    return ax


class SolverOutput:
    """A class to gather solver output.

    The SolverOutput class provides useful information concerning the solver
    solution.

    Attributes
    ----------
    converged : bool
        Whether the solver converged to the solution.
    message : string
        Output message.
    iteration : int
        Number of iterations.
    x : float
        Current iterate.
    fx : float
        Current iterate objective.
    dfx : float
        Current iterate derivative.
    rtol : float
        Relative objective tolerance.
    xtol : float
        Relative solution tolerance.

    """
    def __init__(self):
        self.converged = False
        self.message = ''
        self.iteration = 0
        self.x = None
        self.x0 = None
        self.interval = None
        self.fx = None
        self.dfx = None
        self.rtol = float('inf')
        self.xtol = float('inf')

    def __str__(self):
        output_str = f"""
        converged: {self.converged} \n
        iterations: {self.iteration} \n
        current iterate: {self.x} \n
        message: {self.message} \n
        fx: {self.fx} \n
        dfx: {self.dfx} \n
        x0: {self.x0} \n
        interval of search: {self.interval} \n"""
        return output_str

    def is_in_interval(self, interval):
        """Check if the iterate remains in the interval.


        Parameters
        ----------
        interval : tuple
            Search interval.

        Returns
        _______
        float
            Whether the current iterate is inside the search interval.

        """
        if interval[0] == interval[1]:
            return True

        if self.x is None or interval is None:
            return True
        else:
            return self.x >= interval[0] and self.x <= interval[1]
