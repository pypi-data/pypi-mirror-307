[![codecov](https://codecov.io/gl/Loicvh/quadproj/branch/master/graph/badge.svg?token=H2LI6Z1SMI)](https://codecov.io/gl/Loicvh/quadproj)
[![pipeline status](https://gitlab.com/loicvh/quadproj/badges/master/pipeline.svg)](https://gitlab.com/loicvh/quadproj/-/commits/master)
[![PyPI](https://img.shields.io/pypi/v/quadproj)](https://pypi.org/project/quadproj/)
[![PyPI - License](https://img.shields.io/pypi/l/quadproj)](https://pypi.org/project/quadproj/)
[![Conda](https://img.shields.io/conda/v/loicvh/quadproj)](https://anaconda.org/loicvh/quadproj)
[![Documentation](https://img.shields.io/badge/docs-%20-green)](https://loicvh.gitlab.io/quadproj/)


# quadproj

A simple library to project a point onto a quadratic surface, or *quadric*.

## How to install quadproj?

It is a one-liner!

```python3
python3 -m pip install quadproj
```

See [installation page](https://loicvh.gitlab.io/quadproj/installation.html) for further information and the requirements.

## Documentation

The documentation is hosted on GitLab: [https://loicvh.gitlab.io/quadproj](https://loicvh.gitlab.io/quadproj)

## How does quadproj work?

The projection is obtained by computing exhaustively all KKT point from the optimization problem defining the projection. The authors of [[1]](https://loicvh.eu/aca/abstracts/OJMO_2022.html) show that for non-cylindrical central quadrics, the solutions belong to the KKT points that consist in the intersection between:

- a unique root of a nonlinear function on a specific interval;
- a set of closed-form points.

Either set can be empty but for a nonempty quadric, at least one is nonempty and contains (one of the) projections.

The full explanation is provided in [[1]](https://loicvh.eu/aca/abstracts/OJMO_2022.html).


## How to use quadproj?

See the [quickstart](https://loicvh.gitlab.io/quadproj/quickstart.html) page or the [API documentation](https://loicvh.gitlab.io/quadproj/modules.html).



## Dependencies

See [requirements.txt](https://gitlab.com/loicvh/quadproj/-/blob/master/requirements.txt).


## [1]
(2021) L. Van Hoorebeeck, P.-A. Absil and A. Papavasiliou, “Projection onto quadratic hypersurfaces”, submitted. ([preprint](https://loicvh.eu/aca/_downloads/dc8ab520a768f81e13569c647c7553d7/OJMO_2022_preprint.pdf), [abstract/BibTex](https://loicvh.eu/aca/abstracts/OJMO_2022.html))

