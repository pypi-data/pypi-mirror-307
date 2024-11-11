#!/usr/bin/env python3

import quadproj.fun as fun
from quadproj.quadrics import Quadric
import numpy as np


def test_fun_exception():
    dim = 3
    A = np.eye(dim)
    param = {'A': A, 'b': np.zeros(dim), 'c': 1}

    Q = Quadric(**param)

    assert Q.is_empty

    x0_not_std = np.zeros(dim)
    x0_not_std[0] = 0
    x0_not_std[1] = 1
    x0 = Q.to_normalized(x0_not_std)
    # Fun objects should raise EmptyQuadric errors when created
    # with an empty quadric.
    try:
        fun.Fun(Q, x0)
    except Quadric.EmptyQuadric:
        pass
