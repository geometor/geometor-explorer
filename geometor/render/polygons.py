import matplotlib as mp
import matplotlib.pyplot as plt
import mplcursors

import sympy as sp
import sympy.geometry as spg

from .styles import *


def plot_polygon(ax, poly, edgecolor='#36c9', facecolor='#36c3', linestyle='-', linewidth=1, fill=True):
    '''takes a sympy Polygon and plots with the matplotlib Polygon patch'''
    if isinstance(poly, spg.Segment2D):
        plot_segment2(ax, poly)
    else:
        xy = [(pt.x.evalf(), pt.y.evalf()) for pt in poly.vertices]
        # print(xy)
        styles = {'facecolor':facecolor, 'edgecolor':edgecolor, 'linestyle':linestyle, 'linewidth':linewidth, 'fill':fill}
        for cl in poly.classes:
            if cl in classes:
                styles.update(classes[cl])
        patch = plt.Polygon(xy, **styles)
        ax.add_patch(patch)


def plot_polygons(ax, poly_array):
    for poly in poly_array:
        plot_polygon(ax, poly)


