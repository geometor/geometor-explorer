"""
plot_elements module
====================

functions for rendering elements
"""

from .common import *
from .styles import *

def plot_circle(ax, circle, classes, edgecolor='', facecolor='', linestyle='', linewidth='', fill=''):
    '''takes a sympy circle and plots with the matplotlib Circle patch'''
    center = (circle.center.x.evalf(), circle.center.y.evalf())
    radius = circle.radius

    styles = STYLES['default_circle'].copy()
    for cl in classes:
        if cl in STYLES:
            styles.update(STYLES[cl])
    if edgecolor:
        styles['edgecolor'] = edgecolor
    if facecolor:
        styles['facecolor'] = facecolor
    if linestyle:
        styles['linestyle'] = linestyle
    if linewidth:
        styles['linewidth'] = linewidth
    if fill:
        styles['fill'] = fill

    patch = plt.Circle(center, radius, **styles)
    ax.add_patch(patch)
    return [patch]


def plot_line(ax, el, classes, bounds, color='', linestyle='', linewidth=''):
    ends = bounds.intersection(el)
    xs = [pt.x.evalf() for pt in ends]
    ys = [pt.y.evalf() for pt in ends]

    styles = STYLES['default']['line'].copy()
    for cl in classes:
        if cl in STYLES:
            styles.update(STYLES[cl]['line'])
    # override defaults
    if color:
        styles['color'] = color
    if linestyle:
        styles['linestyle'] = linestyle
    if linewidth:
        styles['linewidth'] = linewidth

    return ax.plot(xs, ys, **styles)


def plot_elements(ax, elements, bounds):
    for el in elements:
        if type(el) == sp.Line2D:
            plot_line(ax, el, bounds)
        elif type(el) == sp.Circle:
            plot_circle(ax, el)
        else:
            print('No Match')

