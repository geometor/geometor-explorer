'''
lines module
============
'''

from .common import *


def line(pt_a, pt_b):
    '''make sympy.geometry.Line'''
    el = spg.Line(pt_a, pt_b)
    return el


def line_get_y(l1, x):
    '''return y value for specific x'''
    a, b, c = l1.coefficients
    return (-a * x - c) / b


