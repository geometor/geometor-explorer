"""
segments module
===============

functions to plot segments
"""
from .common import *
from .styles import *


def plot_segment(ax, pt1, pt2, color='#fc09', linestyle='-', linewidth=3, marker='.', markersize=0):
    x1 = pt1.x.evalf()
    x2 = pt2.x.evalf()
    y1 = pt1.y.evalf()
    y2 = pt2.y.evalf()
    styles = {'color':color, 'linestyle':linestyle, 'linewidth':linewidth, 'marker':marker, 'markersize':markersize}
    ax.plot( [x1, x2], [y1, y2], **styles )


def plot_segment2(ax, seg, classes=[], color='', linestyle='-', linewidth=0, marker='', markersize=0):
    x1 = seg.points[0].x.evalf()
    x2 = seg.points[1].x.evalf()
    y1 = seg.points[0].y.evalf()
    y2 = seg.points[1].y.evalf()

    styles = STYLES['default_segment'].copy()
    for cl in classes:
        if cl in STYLES:
            styles.update(STYLES[cl])

    if color:
        styles['color'] = color
    if linestyle:
        styles['linestyle'] = linestyle
    if linewidth:
        styles['linewidth'] = linewidth
    if 'edgecolor' in styles:
        styles['color'] = styles['edgecolor']
        styles.pop('edgecolor')
    if 'facecolor' in styles:
        styles.pop('facecolor')

    return ax.plot( [x1, x2], [y1, y2], **styles )


def plot_segments(ax, segs, classes=[]):
    current = []
    for seg in segs:
        current.append(plot_segment2(ax, seg))

    return current

