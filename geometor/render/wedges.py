"""
wedges module
=============

functions to plot wedges
"""
from .common import *
from .styles import *

def plot_wedge(ax, ctr_pt, rad_pt, sweep_pt, color='#0f03', linestyle='', linewidth=6, fill=True):
    '''takes a sympy circle and plots with the matplotlib Circle patch'''
    center = (float(ctr_pt.x.evalf()), float(ctr_pt.y.evalf()))
    rad_val = float(ctr_pt.distance(rad_pt).evalf())
    print(center, rad_val)
    radius_line = spg.Line(ctr_pt, rad_pt)
    sweep_line = spg.Line(ctr_pt, sweep_pt)
    base_line = spg.Line(spg.Point(0,0), spg.Point(1,0))

    # t = polygon
    a1 = math.degrees(base_line.angle_between(radius_line).evalf())
    a2 = math.degrees(base_line.angle_between(sweep_line).evalf())
    cy = float(ctr_pt.y.evalf())
    ry = float(rad_pt.y.evalf())
    if cy > ry:
        a1 = -a1
    print(a1, a2)
    patch = mp.patches.Wedge(center, rad_val, a1, a2,
                          color=color,
                          linestyle=linestyle,
                          linewidth=linewidth,
                          fill=fill )
    ax.add_patch(patch)


def plot_wedge_2(ax, ctr_pt, rad_val, a1, a2, fc='#0ff1', ec='#0002', linestyle='', linewidth=6, fill=True):
    '''light wrapper for Wegde patch'''
    center = (float(ctr_pt.x.evalf()), float(ctr_pt.y.evalf()))
    patch = mp.patches.Wedge(center, rad_val, a1, a2,
                          fc=fc,
                          ec=ec,
                          linestyle=linestyle,
                          linewidth=linewidth,
                          fill=fill )
    ax.add_patch(patch)


