"""

This module provides a number of objects (mostly functions) useful for
embedding all functions used to compute the KKT points from the
projection of a point x0 to a quadric Q.


"""

import numpy as np
import matplotlib.pyplot as plt

eps = pow(10, -14)


def _f(Q, mu, x0, _x_std):
    """Secular function.

    Given the quadric `Q` and the `n` dimensional point `x0`,
    this function evaluates the (secular) function f.

    .. math:: f(\\mu) = \\sum_{i=1}^n \\lambda_i \\Big ( \\frac{x^0_i}{1+\\mu \\lambda_i}\\Big )^2-1

    Parameters
    ----------
    Q : Quadric instance
        The quadric onto which the point x0 has to be projected.
    mu : float
        Lagrange multiplier.
    x0 : ndarray
        1-D ndarray containing the point to be projected.

    Returns
    _______
    float
        Evaluation of f defined with Q and x0 at point mu.

    """
    mask_x0 = np.abs(x0) > eps
    mask_eig = np.abs(Q.eig) > eps

    mask_inf_condition = mask_x0 & mask_eig & (np.abs(mu * Q.eig + 1) < eps)
    if np.any(mask_inf_condition):
        return -np.sign(mu) * np.inf

    x_mu = _x_std(mu)
    out = x_mu.T @ (Q.eig * x_mu) + Q.c_norm
    if Q.is_parabolic:
        out += Q.b_norm[Q.pivot] * x_mu[Q.pivot]
    return out


def _d_f(Q, mu, x0, _x_std, _d_x_std):
    """Derivative of the secular function.

    Given the quadric `Q` and the `n` dimensional point `x0`,
    this function evaluates the derivative of the (secular) function f.

    .. math:: f'(\\mu) = -2 \\sum_{i=1}^n   -\\lambda_i \\left( b_i^r + 2 \\lambda_i x^0_i \\right) \\left( 2 x_0[i] - b_i^r \\mu \\right) \\frac{1}{2(1 + \\mu \\lambda_i)^3} - b_i^r \\left( b_i^r + 2 \\lambda_i x^0_i \\right) \\frac{1}{2 \\left( \\lambda_i \\mu + 1 \\right)^2}

    Parameters
    ----------
    Q : Quadric instance
        The quadric onto which the point x0 has to be projected.
    mu : float
        Lagrange multiplier.
    x0 : ndarray
        1-D ndarray containing the point to be projected.
    Returns
    _______
    float
        Evaluation of f' defined with Q and x0 at point mu.

    """

    x_mu = _x_std(mu)
    dx_mu = _d_x_std(mu)

    out = 2 * dx_mu.T @ (Q.eig * x_mu)
    if Q.is_parabolic:
        out += Q.b_norm[Q.pivot] * dx_mu[Q.pivot]
    return out


def _get_e1(Q, x0):
    """Obtain largest negative pole.

    Given the quadric `Q` and the `n` dimensional point `x0`,
    this function obtain the largest negative pole of the rational function :math:`f`
    (obtained as :math:`f(\\mu)` = `fun._f(Q, mu, x0)`).

    If no such pole exists, the function returns -inf.

    Remark that poles cancel by zeros will be omitted.

    Parameters
    ----------
    Q : Quadric instance
        The quadric onto which the point x0 has to be projected.
    x0 : ndarray
        1-D ndarray containing the point to be projected.
    Returns
    _______
    e1 : float
        Largest negative pole of f.
    """

    e1 = -np.inf
    for i, x in enumerate(x0):
        if abs(x) > eps and Q.eig[i] > eps:
            return -1 / Q.eig[i]
    return e1


def _get_e2(Q, x0):
    """Obtain smallest positive pole.

    Given the quadric `Q` and the `n` dimensional point `x0`,
    this function obtain the smallest positive pole of the rational function :math:`f`
    (obtained as :math:`f(\\mu)` = `fun._f(Q, mu, x0)`).

    If no such pole exists, the function returns inf.

    Remark that poles cancel by zeros will be omitted.

    Parameters
    ----------
    Q : Quadric instance
        The quadric onto which the point x0 has to be projected.
    x0 : ndarray
        1-D ndarray containing the point to be projected.
    Returns
    -------
    e2 : float
        Smallest positive pole of f.
    """

    e2 = np.inf
    for i, _ in enumerate(x0):
        if abs(x0[-i]) > eps and Q.eig[-i] < -eps:
            return -1 / Q.eig[-i]
    return e2


class Fun():
    """A function class.

    The Fun class provides useful function definitions for computing
    KKT points.

    Parameters
    ----------
    Q : Quadric instance
        The nonempty quadric onto which the point x0 has to be projected.
    x0 : ndarray
        1-D ndarray containing the point to be projected.
    Attributes
    ----------
    x_std : function
        Given mu, returns the associated standardized x.
    x_not_std : function
        Given mu, returns the associated not standardized x.
    f : function
        Given mu, returns f(mu).
    d_f : function
        Derivative of f.
    e1 : float
        Largest negative pole of f (-np.inf if no such pole exists).
    e2 : float
        Smallest positive pole of f (np.inf if no such pole exists).
    interval : tuple of float
        Search interval for the root: (e_1, e_2).
    dist : function
        Distance function to x0_not_std.
    """

    def __init__(self, Q, x0):

        eig_1 = Q.eig[Q.nonzero_ev_indices]
        x0_1 = x0[Q.nonzero_ev_indices]
        x0_2 = x0[Q.zero_ev_indices]
        _intermediate_result = Q.P_inv_2 @ Q.b_norm[Q.zero_ev_indices] / 2 * np.ones(len(Q.zero_ev_indices))

        def inv_I_lA(mu):
            return x0_1 / (1 + eig_1 * mu)  # Temporary function

        def inv_I_lA2(mu):
            return -x0_1 * eig_1 / (1 + eig_1 * mu)**2  # Temporary function

        def _x_std(mu):

            out = np.zeros(Q.dim)
            out[Q.nonzero_ev_indices] = inv_I_lA(mu)
            out[Q.zero_ev_indices] = x0_2 - _intermediate_result * mu
            return out

        def _d_x_std(mu):
            out = np.zeros(Q.dim)
            out[Q.nonzero_ev_indices] = inv_I_lA2(mu)
            out[Q.zero_ev_indices] = - _intermediate_result
            return out

        if not Q.is_parabolic and False:
            self.x_std = lambda mu: x0 / (1 + mu * Q.eig)
            self.d_x_std = lambda mu: -x0 * Q.eig / (1 + Q.eig * mu)**2
        else:
            self.x_std = lambda mu: _x_std(mu)
            self.d_x_std = lambda mu: _d_x_std(mu)

        self.x_not_std = lambda mu: Q.to_non_normalized(self.x_std(mu))

        self.Q = Q
        self.f = lambda mu: _f(Q, mu, x0, self.x_std)
        self.d_f = lambda mu: _d_f(Q, mu, x0, self.x_std, self.d_x_std)

        self.e1 = _get_e1(Q, x0)
        self.e2 = _get_e2(Q, x0)
        self.interval = self.e1, self.e2
        x0_not_std = Q.to_non_normalized(x0)

        self.dist = lambda _x: np.linalg.norm(_x - x0_not_std)

    def plot(self):
        m = 100
        t = np.linspace(max(self.e1, -self.e2, -1) - 10, min(self.e2, -self.e1, 1) + 10, m)
        y = np.zeros_like(t)
        plt.figure()
        for i, _t in enumerate(t):
            y[i] = self.f(_t)
        plt.scatter(self.e1, 0, label="e1")
        plt.scatter(self.e2, 0, label="e2")
        plt.legend()
        plt.plot(t, y)
        plt.show()
