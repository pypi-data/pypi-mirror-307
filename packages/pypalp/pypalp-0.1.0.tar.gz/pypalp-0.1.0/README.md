# PyPALP: a Python Package for Analyzing Lattice Polytopes

[![Python CI](https://github.com/ariostas/pypalp/actions/workflows/python.yml/badge.svg)](https://github.com/ariostas/pypalp/actions/workflows/python.yml)

This project provides Python bindings for the [PALP](http://hep.itp.tuwien.ac.at/~kreuzer/CY/CYpalp.html) package developed by M. Kreuzer and H. Skarke. The purpose of this project is to make PALP more easily installable and accessible. The original PALP code can be found in their [website](http://hep.itp.tuwien.ac.at/~kreuzer/CY/CYpalp.html) or in their [GitLab](https://gitlab.com/stringstuwien/PALP). PyPALP uses a fork with minor modifications, which can be found [here](https://github.com/ariostas/PALP).

The functionality and documentation of this project are currently fairly limited. If there is enough interest, I will continue to expand on both functionality and documentation. Please open an issue to ask for more functionality, or even better, make a pull request!

PALP is written in C and was never meant to have Python bindings. Some of the design choices make it quite tricky to do so, but I have found some hacky ways to work around them. I have tried to document the

## Installation

PyPALP can be installed in most cases simply by running
```bash
pip install pypalp
```

If you want to tweak compilation parameters or anything else, you can clone the repository and build the wheel yourself.
```bash
git clone --recurse-submodules https://github.com/ariostas/pypalp.git
cd pypalp
pip install .
```

## Usage

Here is a basic example that shows the available functionality.

```python
>>> from pypalp import Polytope
>>>
>>> # Constructing polytopes
>>> polytope_from_points = Polytope([[1, 1], [-1, 1], [1, -1], [-1, -1]])
>>> polytope_from_weight_system = Polytope([4, 7, 7, 10, 12, 40])
>>> polytope_from_weight_system_string = Polytope("4 7 7 10 12  40=d  rn  H:28  16  M: 23  7  N:25  6  P:3  F:2  7 12")
>>>
>>> # Available computations
>>> p = Polytope([[1,0,0,0,0],[0,1,0,0,0],[-1,-1,0,0,0],[0,0,1,0,0],[0,0,-1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,-1,-1]])
>>> p
A 5-dimensional PALP polytope
>>> p.dim()
5
>>> p.vertices()
array([[ 1,  0,  0,  0,  0],
       [ 0,  1,  0,  0,  0],
       [-1, -1,  0,  0,  0],
       [ 0,  0,  1,  0,  0],
       [ 0,  0, -1,  0,  0],
       [ 0,  0,  0,  1,  0],
       [ 0,  0,  0,  0,  1],
       [ 0,  0,  0, -1, -1]])
>>> p.points()
array([[ 1,  0,  0,  0,  0],
       [ 0,  1,  0,  0,  0],
       [-1, -1,  0,  0,  0],
       [ 0,  0,  1,  0,  0],
       [ 0,  0, -1,  0,  0],
       [ 0,  0,  0,  1,  0],
       [ 0,  0,  0,  0,  1],
       [ 0,  0,  0, -1, -1],
       [ 0,  0,  0,  0,  0]])
>>> p.is_ip()
True
>>> p.is_reflexive()
True
>>> p.normal_form()
array([[ 1,  0,  0,  0,  0],
       [-1,  0,  0,  0,  0],
       [ 0,  1,  0,  0,  0],
       [ 0,  0,  1,  0,  0],
       [ 0,  0,  0,  1,  0],
       [ 0,  0, -1, -1,  0],
       [ 0,  0,  0,  0,  1],
       [ 0, -1,  0,  0, -1]])
>>> p.normal_form(affine=True)
array([[ 2,  0,  0,  0,  0],
       [ 0,  1,  0,  0,  0],
       [ 0,  0,  1,  0,  0],
       [ 3, -1, -1,  0,  0],
       [ 0,  0,  0,  1,  0],
       [ 0,  0,  0,  0,  1],
       [ 3,  0,  0, -1, -1],
       [ 0,  0,  0,  0,  0]])
>>> # Nef partitions are returned as a list of 3-tuples (partitions, hodge_diamond, chi)
>>> p.nef_partitions(codim=2, keep_symmetric=False, keep_products=False, keep_projections=False, with_hodge_numbers=True)
[([[0, 1, 5, 6], [2, 3, 4, 7]], [[1, 0, 0, 1], [0, 3, 51, 0], [0, 51, 3, 0], [1, 0, 0, 1]], -96), ([[0, 1, 3, 5], [2, 4, 6, 7]], [[1, 0, 0, 1], [0, 3, 51, 0], [0, 51, 3, 0], [1, 0, 0, 1]], -96), ([[0, 1, 3, 5, 6], [2, 4, 7]], [[1, 0, 0, 1], [0, 3, 60, 0], [0, 60, 3, 0], [1, 0, 0, 1]], -114), ([[0, 1, 3, 4, 5], [2, 6, 7]], [[1, 0, 0, 1], [0, 3, 51, 0], [0, 51, 3, 0], [1, 0, 0, 1]], -96), ([[0, 1, 3, 4, 5, 6], [2, 7]], [[1, 0, 0, 1], [0, 3, 69, 0], [0, 69, 3, 0], [1, 0, 0, 1]], -132), ([[0, 1, 2, 5], [3, 4, 6, 7]], [[1, 0, 0, 1], [0, 9, 27, 0], [0, 27, 9, 0], [1, 0, 0, 1]], -36), ([[0, 1, 2, 5, 6], [3, 4, 7]], [[1, 0, 0, 1], [0, 3, 75, 0], [0, 75, 3, 0], [1, 0, 0, 1]], -144), ([[0, 1, 2, 3], [4, 5, 6, 7]], [[1, 0, 0, 1], [0, 19, 19, 0], [0, 19, 19, 0], [1, 0, 0, 1]], 0), ([[0, 1, 2, 3, 5], [4, 6, 7]], [[1, 0, 0, 1], [0, 6, 51, 0], [0, 51, 6, 0], [1, 0, 0, 1]], -90), ([[0, 1, 2, 3, 5, 6], [4, 7]], [[1, 0, 0, 1], [0, 3, 75, 0], [0, 75, 3, 0], [1, 0, 0, 1]], -144), ([[0, 1, 2, 3, 4, 5], [6, 7]], [[1, 0, 0, 1], [0, 3, 75, 0], [0, 75, 3, 0], [1, 0, 0, 1]], -144)]
```

## License

The original PALP code, as well as the binding code in PyPALP are distributed under the [GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.txt).
