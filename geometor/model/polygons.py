"""
polygons module
===============
"""

from .common import *

def polygon(poly_pts, classes=[], style={}):
    '''- takes array of points - make sympy.geometry.Polygon, Triangle or Segment'''
    el = spg.Polygon(*poly_pts)
    el.classes = classes
    el.style = style
    return el


def polygon_ids(ids, classes=[], style={}):
    '''create polygon from list of point ids'''
    return polygon([pts[i] for i in ids], classes=classes, style=style)


def unit_square(pt, classes=[], style={}):
    '''creates a unit square from the reference point
    adds points and returns polygon'''
    poly_pts = []
    poly_pts.append(pt)
    poly_pts.append(point(pt.x + 1, pt.y))
    poly_pts.append(point(pt.x + 1, pt.y + 1))
    poly_pts.append(point(pt.x, pt.y + 1))
    return polygon(poly_pts, classes=classes, style=style)

