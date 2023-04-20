"""
circles module
================

"""

from .common import *


def circle(pt_c, pt_r):
    """make sympy.geometry.Circle from two points"""
    el = spg.Circle(pt_c, pt_c.distance(pt_r))
    el.radius_pt = pt_r
    return el
