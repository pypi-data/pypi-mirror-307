from __future__ import annotations

import numpy as np

from pypalp import Polytope


def test_dim():
    p = Polytope([[1, 1], [-1, 1], [1, -1], [-1, -1]])
    assert p.dim() == 2

    p = Polytope(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [-1, -1, -1, -1],
        ]
    )
    assert p.dim() == 4


def test_vertices():
    points = np.array([[1, 1], [-1, 1], [1, -1], [-1, -1]], dtype=np.int64)
    vertices = points
    sorted_vertices = sorted(tuple(pt) for pt in vertices)

    p = Polytope(points)
    computed_vertices = p.vertices()
    sorted_computed_vertices = sorted(tuple(pt) for pt in computed_vertices)

    print(f"vertices: {vertices}")
    print(f"computed_vertices: {computed_vertices}")

    assert len(computed_vertices) == 4
    assert sorted_computed_vertices == sorted_vertices

    points = np.array([[1, 1], [-1, 1], [1, -1], [-1, -1], [0, 1]], dtype=np.int64)
    vertices = points[:-1]
    sorted_vertices = sorted(tuple(pt) for pt in vertices)

    p = Polytope(points)
    computed_vertices = p.vertices()
    sorted_computed_vertices = sorted(tuple(pt) for pt in computed_vertices)

    print(f"vertices: {vertices}")
    print(f"computed_vertices: {computed_vertices}")

    assert len(computed_vertices) == 4
    assert sorted_computed_vertices == sorted_vertices


def test_points():
    vertices = np.array([[1, 1], [-1, 1], [1, -1], [-1, -1]], dtype=np.int64)
    points = np.array(
        [[1, 1], [-1, 1], [1, -1], [-1, -1], [0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]],
        dtype=np.int64,
    )
    sorted_points = sorted(tuple(pt) for pt in points)

    p = Polytope(vertices)
    computed_points = p.points()
    sorted_computed_points = sorted(tuple(pt) for pt in computed_points)

    assert len(computed_points) == 9
    assert sorted_computed_points == sorted_points


def test_ip():
    vertices = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [-1, -1, -1, -1],
    ]

    p = Polytope(vertices)

    assert p.is_ip()


def test_reflexive():
    vertices = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [-1, -1, -1, -1],
    ]

    p = Polytope(vertices)

    assert p.is_reflexive()


def test_constructors():
    vertices = [
        [-1, -1, -1, -1],
        [0, -1, -1, -1],
        [0, 3, -1, -1],
        [1, -1, 3, -1],
        [0, -1, -1, 0],
        [0, 3, -1, 0],
        [-1, -1, -1, 2],
    ]
    sorted_vertices = sorted(tuple(pt) for pt in vertices)

    p1 = Polytope(vertices)
    p2 = Polytope([4, 7, 7, 10, 12, 40])
    p3 = Polytope("4 7 7 10 12  40=d  rn  H:28  16  M: 23  7  N:25  6  P:3  F:2  7 12")

    v1 = sorted(tuple(pt) for pt in p1.vertices())
    v2 = sorted(tuple(pt) for pt in p2.vertices())
    v3 = sorted(tuple(pt) for pt in p3.vertices())

    assert v1 == v2 == v3 == sorted_vertices


def test_normal_form():
    p1_str = "1 1 1  1  1   5=d  TS  H: 1 101  M:126  5  N: 6  5  P:0  F:0"
    p1_nf = [[1, 0, 0, 0], [1, 5, 0, 0], [1, 0, 5, 0], [1, 0, 0, 5], [-4, -5, -5, -5]]
    p1_anf = [[5, 0, 0, 0], [0, 5, 0, 0], [0, 0, 5, 0], [0, 0, 0, 5], [0, 0, 0, 0]]

    p1 = Polytope(p1_str)
    assert p1.normal_form().tolist() == p1_nf
    assert p1.normal_form(affine=True).tolist() == p1_anf

    p2_str = "1 3 3 10 14  31=d  Tn  H:14 106  M:143  9  N:21  7  P:0  F:0"
    p2_nf = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [3, -4, -1, -1],
        [-4, 3, -1, -1],
        [4, -6, -2, -1],
        [-6, 4, -2, -1],
        [-6, -6, -2, 9],
    ]
    p2_anf = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 3, 3, 4],
        [7, 3, 3, 4],
        [10, 4, 5, 6],
        [0, 4, 5, 6],
        [0, 4, 15, 6],
        [0, 0, 0, 0],
    ]

    p2 = Polytope(p2_str)
    assert p2.normal_form().tolist() == p2_nf
    assert p2.normal_form(affine=True).tolist() == p2_anf


def test_nef_partitions():
    p = Polytope(
        [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [-1, -1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, -1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, -1, -1],
        ]
    )

    nefparts_no_hodge = p.nef_partitions(with_hodge_numbers=False)
    assert len(nefparts_no_hodge) == 11
    for i, nefpart in enumerate(nefparts_no_hodge):
        assert nefpart[1] is None
        assert nefpart[2] is None
        if i == 0:
            assert nefpart[0] == [[0, 1, 5, 6], [2, 3, 4, 7]]
        elif i == 1:
            assert nefpart[0] == [[0, 1, 3, 5], [2, 4, 6, 7]]

    nefparts_proj_prod_no_hodge = p.nef_partitions(
        keep_products=True, keep_projections=True, with_hodge_numbers=False
    )
    assert len(nefparts_proj_prod_no_hodge) == 15

    nefparts_sym_proj_prod_no_hodge = p.nef_partitions(
        keep_symmetric=True,
        keep_products=True,
        keep_projections=True,
        with_hodge_numbers=False,
    )
    assert len(nefparts_sym_proj_prod_no_hodge) == 127

    nefparts_hodge = p.nef_partitions()
    assert len(nefparts_hodge) == 11
    for i, nefpart in enumerate(nefparts_hodge):
        if i == 0:
            assert nefpart[0] == [[0, 1, 5, 6], [2, 3, 4, 7]]
            assert nefpart[1] == [
                [1, 0, 0, 1],
                [0, 3, 51, 0],
                [0, 51, 3, 0],
                [1, 0, 0, 1],
            ]
            assert nefpart[2] == -96
        elif i == 1:
            assert nefpart[0] == [[0, 1, 3, 5], [2, 4, 6, 7]]
            assert nefpart[1] == [
                [1, 0, 0, 1],
                [0, 3, 51, 0],
                [0, 51, 3, 0],
                [1, 0, 0, 1],
            ]
            assert nefpart[2] == -96
