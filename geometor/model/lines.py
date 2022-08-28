'''
Line nodule
'''

from .common import *

def line(pt_a, pt_b, classes=[], style={}):
    '''make sympy.geometry.Line'''
    el = spg.Line(pt_a, pt_b)
    el.pts = {pt_a, pt_b}
    el.classes = classes
    el.style = style
    return el


def line_get_y(l1, x):
    '''return y value for specific x'''
    a, b, c = l1.coefficients
    return (-a * x - c) / b


