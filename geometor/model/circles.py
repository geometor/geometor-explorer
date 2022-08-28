"""
circles module
"""

from ..common import *

def circle(pt_c, pt_r, classes=[], style={}):
    '''make sympy.geometry.Circle from two points'''
    el = spg.Circle(pt_c, pt_c.distance(pt_r))
    el.radius_pt = pt_r
    el.pts = {pt_r}
    el.classes = classes
    el.style = style
    return el

