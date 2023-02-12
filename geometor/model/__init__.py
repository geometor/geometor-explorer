'''
Model Package
=============

The Model module provides a set of tools for constructing geometric models.
It relies heavily on sympy for providing the algebraic infrastructure
the functions here are for creating the abstract model, not the rendering
see the Render module for plotting with matplotlib
'''
from .common import *

from .points import *
from .lines import *
from .circles import *
from .polygons import *
from .polynomials import *
from .model import *

# constants
num_workers = cpu_count()

Φ = sp.GoldenRatio
phi = sp.Rational(1, 2) + (sp.sqrt(5) / 2)


# graphical elements
def segment(pt_a, pt_b):
    '''make sympy.geometry.Segment'''
    el = spg.Segment(pt_a, pt_b)
    return el


# helpers ******************************
def begin():
    '''create inital two points -
    establishing the unit for the field'''
    A = point(sp.Rational(-1, 2), 0, classes=['start'])
    add_point(A)
    B = point(sp.Rational(1, 2), 0, classes=['start'])
    add_point(B)
    return A, B


def begin_zero():
    '''create inital two points -
    establishing the unit for the field'''
    A = point(0, 0, classes=['start'])
    add_point(A)
    B = point(1, 0, classes=['start'])
    add_point(B)
    return A, B

    
def bisector(pt1, pt2):
    '''perform fundamental operations for two points
    and add perpendicular bisector'''

    # baseline
    add_element(line(pt1, pt2))

    # vesica
    c1 = add_element(circle(pt1, pt2))
    c2 = add_element(circle(pt2, pt1))

    # bisector
    # last two points should be from the last two circles intersection
    el = line(pts[-1], pts[-2], classes=['bisector'])
    add_element(el)


def bisect_pts(pt1, pt2):
    '''use sympy function
    add prpoerties to line
    return line'''
    seg = segment(pt1, pt2)
    ln = seg.perpendicular_bisector()
    ln.classes = ['bisector']
    ln.parents = {pt1, pt2}
    ln.pts = set()
    return ln


def bisect_pts2(pt1, pt2):
    '''use circles but don't add to model'''
    c1 = circle(pt1, pt2)
    c2 = circle(pt2, pt1)
    ints = c1.intersection(c2)
    ln = line(ints[0], ints[1])
    ln.classes = ['bisector']
    ln.parents = {pt1, pt2, ints[0], ints[1]}
    ln.pts = set()
    return ln


def bisect_lines(ln1, ln2):
    lns = ln1.bisectors(ln2)
    for ln in lns:
        ln.classes = ['bisector']
        ln.parents = {ln1.p1, ln1.p2, ln2.p1, ln2.p2}
        ln.pts = set()
    return lns


