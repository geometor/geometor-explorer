"""
points module
=============

functions to plot points
"""
from .common import *
from .styles import *

def plot_point(ax, pt,
               classes=[],
               color='w',
               linestyle='',
               marker='.',
               markersize=5,
               add_to_cursors=False,
               ):
    '''plot all the points in pts'''

    # collect x, y values into separate arrays
    xs = [pt.x.evalf()]
    ys = [pt.y.evalf()]

    def on_add(sel):
        # TODO: establish an indexed list of all objects added to the cursor with details
        # TODO: remove the ``pts`` reference below
        i = sel.index
        #  xval = str(pts[i].x).replace('GoldenRatio', 'Φ')
        xval = sp.latex(pts[i].x)
        #  yval = str(pts[i].y).replace('GoldenRatio', 'Φ')
        yval = sp.latex(pts[i].y)
        sel.annotation.set_text(f'{i}:\nx: ${xval}$\ny: ${yval}$')
        sel.annotation.set(color='k', fontsize='x-large', bbox=dict(boxstyle='round,pad=0.5', fc='w'))
        sel.annotation.arrow_patch.set(arrowstyle="simple", ec="k", fc='w')

    pt_outer = ax.plot(xs, ys,
            color='k',
            linestyle=linestyle,
            marker=marker,
            markersize=markersize+3,
            zorder=Z_POINT_OUTER
            )

    pt_inner = ax.plot(xs, ys,
            color=color,
            linestyle=linestyle,
            marker=marker,
            markersize=markersize,
            zorder=Z_POINT_INNER
            )

    # plot highlight
    pt_highlight = None
    if classes:
        styles = {'color':'y', 'linestyle':'', 'marker':'o', 'markersize':markersize+2}
        for cl in classes:
            if cl in STYLES:
                styles.update(STYLES[cl])

        pt_highlight = ax.plot(xs, ys, **styles, 
                zorder=Z_POINT_HILITE)

    if add_to_cursors:
        cursor = mplcursors.cursor(pt_inner)
        cursor.connect("add", on_add)

    return [pt_inner, pt_outer, pt_highlight]


def highlight_points(ax, pts,
               color='y',
               linestyle='',
               marker='o',
               markersize=7,
               ):
    '''plot all the points in pts'''
    for pt in pts:
        if isinstance(pt, spg.Point2D):
            if len(pt.classes):
                styles = {'color':color, 'linestyle':linestyle, 'marker':marker, 'markersize':markersize}
                for cl in pt.classes:
                    if cl in classes:
                        styles.update(classes[cl])
                # collect x, y values into separate arrays
                xs = [pt.x.evalf()]
                ys = [pt.y.evalf()]

                ax.plot(xs, ys, **styles)



def plot_selected_points(ax, pts,
               color='#FF09',
               linestyle='',
               marker='o',
               markersize=15,
               ):
    styles = {'markeredgecolor':color, 'fillstyle':'none', 'linestyle':linestyle, 'marker':marker, 'markersize':markersize}

    xs = [pt.x.evalf() for pt in pts]
    ys = [pt.y.evalf() for pt in pts]

    return ax.plot(xs, ys, **styles)


def gold_points(ax, pts,
               color='#C90',
               linestyle='',
               marker='o',
               markersize=12,
               ):
    '''plot all the points in pts'''
    for pt in pts:
        #  styles = {'color':color, 'linestyle':linestyle, 'marker':marker, 'markersize':markersize}
        styles = {'markeredgecolor':color, 'fillstyle':'none', 'linestyle':linestyle, 'marker':marker, 'markersize':markersize}
        # collect x, y values into separate arrays
        xs = [pt.x.evalf()]
        ys = [pt.y.evalf()]
        ax.plot(xs, ys, **styles)

