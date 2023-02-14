"""
polygons module
===============

functions to plot polygons
"""
from .common import *
from .styles import *


def plot_polygon(ax, poly, classes=[], edgecolor='#36c9', facecolor='#36c3', linestyle='-', linewidth=1, fill=True):
    '''takes a sympy Polygon and plots with the matplotlib Polygon patch'''
    if isinstance(poly, spg.Segment2D):
        plot_segment2(ax, poly)
    else:
        if isinstance(poly, list):
            # Triangles are a list!?
            #  print(poly)
            #  breakpoint()
            xy = [(pt[0].evalf(), pt[1].evalf()) for pt in poly[0].vertices]
        else:
            #  breakpoint()
            xy = [(pt.x.evalf(), pt.y.evalf()) for pt in poly.vertices]
        # print(xy)
        styles = {'facecolor':facecolor, 'edgecolor':edgecolor, 'linestyle':linestyle, 'linewidth':linewidth, 'fill':fill}
        for cl in classes:
            if cl in STYLES:
                styles.update(STYLES[cl])
        patch = plt.Polygon(xy, **styles)
        ax.add_patch(patch)
        return patch


def plot_polygons(ax, poly_array):
    for poly in poly_array:
        plot_polygon(ax, poly)


