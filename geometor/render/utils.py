"""
utils module
=============

functions to plot utils
"""
from .common import *
from ..utils import *
from ..model import *

FIG_W = 16
FIG_H = 9

def set_bounds(limx, limy) -> sp.Polygon:
    return sp.Polygon(
        point(limx[0], limy[1]),
        point(limx[0], limy[0]),
        point(limx[1], limy[0]),
        point(limx[1], limy[1])
        )

def snapshot(folder, filename):
    import os
    sessions = os.path.expanduser('~') + '/Sessions'
    out = f'{sessions}/{folder}/'
    os.makedirs(out, exist_ok=True)
    filename = out + filename
    plt.savefig(filename, dpi=120)
    print_log(f'    * {filename}')
    return filename


def snapshot_2(folder, filename, transparent=False):
    import os
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, filename)
    plt.savefig(filename, dpi=120, transparent=transparent)
    print_log(f'    * {filename}')
    return filename


def display(filename):
    from IPython import display
    display.Image(filename)


def ax_prep(ax, ax_btm, bounds, xlabel):
    ax.clear()
    ax_btm.clear()
    ax.axis(False)
    ax_btm.axis(False)
    #  ax.spines['bottom'].set_color('k')
    #  ax.spines['top'].set_color('k')
    #  ax.spines['right'].set_color('k')
    #  ax.spines['left'].set_color('k')
    #  ax.tick_params(axis='x', colors='k')
    #  ax.tick_params(axis='y', colors='k')
    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]
    ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))
    ax.invert_yaxis()

    #  ax.set_xlabel(xlabel, fontdict={'color': 'w', 'size':'20'})
    ax_btm.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})


def adjust_ratio(w, h, r=FIG_W/FIG_H):
    if w / h < r:
        w = r * h
    if w / h > r:
        h = w / r
    return w, h

def adjust_lims(limx, limy, ratio=FIG_W/(FIG_H-1), margin_ratio=0.1):
    w = abs(limx[1] - limx[0])
    w_margin = w * margin_ratio
    limx[0] -= w_margin
    limx[1] += w_margin
    w = abs(limx[1] - limx[0])

    h = abs(limy[1] - limy[0])
    h_margin = h * margin_ratio
    limy[0] -= h_margin
    limy[1] += h_margin
    h = abs(limy[1] - limy[0])

    w2, h2 = adjust_ratio(w, h, ratio)
    xdiff = abs(w2 - w) / 2
    ydiff = abs(h2 - h) / 2

    limx[0] -= xdiff
    limx[1] += xdiff
    limy[0] -= ydiff
    limy[1] += ydiff

    return limx, limy


def get_limits_from_points(pts, margin=0.1):
    '''find x, y limits from a set of points'''
    limx = [0, 0]
    limy = [0, 0]
    if pts:
        pt = list(pts)[0]
        ptx = float(pt.x.evalf())
        pty = float(pt.y.evalf())
        limx[0] = ptx
        limx[1] = ptx
        limy[0] = pty
        limy[1] = pty

        for pt in pts:
            ptx = float(pt.x.evalf())
            pty = float(pt.y.evalf())
            # print(x, y)
            limx[0] = ptx if ptx < limx[0] else limx[0]
            limx[1] = ptx if ptx > limx[1] else limx[1]
            limy[0] = pty if pty < limy[0] else limy[0]
            limy[1] = pty if pty > limy[1] else limy[1]

    limx[0] -= margin
    limx[1] += margin
    limy[0] -= margin
    limy[1] += margin

    return [limx, limy]


def get_bounds_from_sections(sections, r=FIG_W/(FIG_H-1)):
    section_pts = set()
    for i, section in enumerate(sections):
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
    limx, limy = get_limits_from_points(section_pts, margin=.25)
    limx, limy = adjust_lims(limx, limy, ratio=r)
    bounds = set_bounds(limx, limy)
    return bounds

####
# more generalized plot setup
def ax_set_bounds(ax, bounds):
    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]
    ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))

def ax_set_spines(ax):
    ax.spines['bottom'].set_color('k')
    ax.spines['top'].set_color('k')
    ax.spines['right'].set_color('k')
    ax.spines['left'].set_color('k')
    ax.tick_params(axis='x', colors='k')
    ax.tick_params(axis='y', colors='k')

def ax_prep_caption(bounds, xlabel):
    plt.rcParams['figure.figsize'] = [16, 9]
    #  plt.tight_layout()
    fig, (ax, ax_btm) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [10, 1]})
    ax.clear()
    ax_btm.clear()
    ax.axis(False)
    ax_btm.axis(False)
    ax_set_bounds(ax, bounds)
    ax.invert_yaxis()

    ax_btm.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})

    return fig, ax, ax_btm

def ax_prep_square(bounds=False):
    plt.rcParams['figure.figsize'] = [16, 16]
    plt.tight_layout()
    fig, ax = plt.subplots(1, 1)
    ax.clear()
    ax.axis(False)
    if bounds:
        ax_set_bounds(ax, bounds)
    ax.invert_yaxis()
    return fig, ax

def ax_prep_full(bounds):
    plt.rcParams['figure.figsize'] = [16, 9]
    plt.tight_layout()
    fig, ax = plt.subplots(1, 1)
    ax.clear()
    ax.axis(False)
    ax_set_bounds(ax, bounds)
    ax.invert_yaxis()
    return fig, ax


