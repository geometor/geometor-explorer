'''
The Render Module
provides functions for plotting elements from the geoemtric model to
matplotlib.
'''

import matplotlib as mp
import matplotlib.pyplot as plt
import mplcursors

import sympy as sp
import sympy.plotting as spp
import sympy.geometry as spg

import logging
import math as math

from geometor.model import *
from geometor.utils import *

FIG_W = 16
FIG_H = 9

plt.rcParams['figure.figsize'] = [FIG_W, FIG_H]
plt.style.use('dark_background')

classes = {}
classes['default_line'] = {
        'color':'#999', 
        'linestyle':':', 
        'linewidth':1.5
        }
classes['default_line_segment'] = {
        'color':'#9999', 
        'linestyle':'-', 
        'linewidth':5
        }
classes['default_circle'] = {
        'color':'#C09', 
        'linestyle':':', 
        'linewidth':1.5, 
        'fill':False
        }
classes['default_circle_segment'] = {
        'color':'#C099', 
        'linestyle':'-', 
        'linewidth':5, 
        }
classes['default_segment'] = {
        'color':'#fc09', 
        'linestyle':'-', 
        'linewidth':5, 
        'marker':'', 
        'markersize':0,
        }

classes['blue'] = {'color':'#66F', 'linestyle':':'}
classes['red'] = {'color':'#F33', 'linestyle':':'}
classes['green'] = {'color':'#2F2', 'linestyle':':'}
classes['pappus'] = {'linestyle':'--'}
classes['pink'] = {'color':'#F99', 'linestyle':'--'}
classes['bisector'] = {'linestyle':'-.'}

classes['set1'] = {'color':'#09C', 'linestyle':':'}
classes['set1pt'] = {'color':'#09C', 'markersize':8, 'marker':'o'}

classes['set2'] = {'color':'#C33', 'linestyle':':'}
classes['set2pt'] = {'color':'#C33', 'markersize':8, 'marker':'o'}

classes['ring'] = {'color':'#4444', 'linestyle':'-'}

classes['gold'] = {'color':'#C90', 'linestyle':':'}
classes['goldpt'] = {'color':'#C90', 'markersize':8, 'marker':'o'}

classes['start'] = {'color':'#FFF6', 'markersize':7, 'marker':'o'}
classes['circle'] = {'color':'#0FF', 'markersize':7, 'marker':'o'}
classes['square'] = {'color':'#FF0', 'markersize':7, 'marker':'s'}
classes['diamond'] = {'color':'#F0F', 'markersize':7, 'marker':'D'}
classes['star'] = {'color':'#F99', 'markersize':12, 'marker':'*'}

classes['nine'] = {'edgecolor':'#3F06', 'facecolor':'#3F03', 'linestyle':'-', 'linewidth':1}
classes['yellow'] = {'edgecolor':'#FF09', 'facecolor':'#FF03', 'linestyle':'-', 'linewidth':1}
classes['cyan'] = {'color':'#0FF3', 'linestyle':'-'}
classes['cyanpt'] = {'color':'#C90', 'markersize':8, 'marker':'o'}
classes['magenta'] = {'color':'#F0F3', 'linestyle':'-'}


#  def plt_init(limx='', limy=''):
    #  '''configure the MatPlotLib stateful plot engine'''
    #  plt.style.use('dark_background')
    #  #  plt.figure(num=1, figsize=(7, 5), dpi=120)
    #  plt.gca().set_aspect('equal')

    #  if limx:
        #  ax.set_xlim(limx[0], limx[1])
    #  if limy:
        #  ax.set_ylim(limy[0], limy[1])
    #  ax.set_title('G E O M E T O R', fontdict={'color': '#960', 'size':'small'})
    #  plt.axis(False)
    #  plt.tight_layout()


def plt_init_polar():
    '''configure the MatPlotLib stateful plot engine'''
    mp.style.use('dark_background')


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


def plot_circle(ax, circle, color='', linestyle='', linewidth='', fill=''):
    '''takes a sympy circle and plots with the matplotlib Circle patch'''
    center = (circle.center.x.evalf(), circle.center.y.evalf())
    radius = circle.radius

    styles = classes['default_circle'].copy()
    for cl in circle.classes:
        if cl in classes:
            styles.update(classes[cl])
    if color:
        styles['color'] = color
    if linestyle:
        styles['linestyle'] = linestyle
    if linewidth:
        styles['linewidth'] = linewidth
    if fill:
        styles['fill'] = fill

    patch = plt.Circle(center, radius, **styles)
    ax.add_patch(patch)


def plot_line(ax, el, bounds, color='', linestyle='', linewidth=''):
    ends = bounds.intersection(el)
    xs = [pt.x.evalf() for pt in ends]
    ys = [pt.y.evalf() for pt in ends]

    styles = classes['default_line'].copy()
    for cl in el.classes:
        if cl in classes:
            styles.update(classes[cl])
    if color:
        styles['color'] = color
    if linestyle:
        styles['linestyle'] = linestyle
    if linewidth:
        styles['linewidth'] = linewidth

    ax.plot(xs, ys, **styles)


def plot_elements(ax, elements, bounds):
    for el in elements:
        if type(el) == sp.Line2D:
            plot_line(ax, el, bounds)
        elif type(el) == sp.Circle:
            plot_circle(ax, el)
        else:
            print('No Match')


def plot_points(ax, pts,
               color='w',
               linestyle='',
               marker='.',
               markersize=5,
               add_to_cursors=True,
               ):
    '''plot all the points in pts'''
    # collect x, y values into separate arrays
    xs = [pt.x.evalf() for pt in pts]
    ys = [pt.y.evalf() for pt in pts]

    def on_add(sel):
        i = sel.index
        sel.annotation.set_text(f'{i}:\nx: {pts[i].x}\ny: {pts[i].y}')
        xval = str(pts[i].x).replace('GoldenRatio', 'Φ')
        yval = str(pts[i].y).replace('GoldenRatio', 'Φ')
        sel.annotation.set_text(f'{i}:\nx: {xval}\ny: {yval}')
        sel.annotation.arrow_patch.set(arrowstyle="simple", ec="k", fc='w')

    point_plot = ax.plot(xs, ys,
            color='k',
            linestyle=linestyle,
            marker=marker,
            markersize=markersize+3
            )
    # use output for mpl cursors
    point_plot = ax.plot(xs, ys,
            color=color,
            linestyle=linestyle,
            marker=marker,
            markersize=markersize
            )

    if add_to_cursors:
        cursor = mplcursors.cursor(point_plot)
        cursor.connect("add", on_add)


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
    '''plot all the points in pts'''
    for pt in pts:
        #  styles = {'color':color, 'linestyle':linestyle, 'marker':marker, 'markersize':markersize}
        styles = {'markeredgecolor':color, 'fillstyle':'none', 'linestyle':linestyle, 'marker':marker, 'markersize':markersize}
        # collect x, y values into separate arrays
        xs = [pt.x.evalf()]
        ys = [pt.y.evalf()]
        ax.plot(xs, ys, **styles)


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


def plot_segment(ax, pt1, pt2, color='#fc09', linestyle='-', linewidth=3, marker='.', markersize=0):
    x1 = pt1.x.evalf()
    x2 = pt2.x.evalf()
    y1 = pt1.y.evalf()
    y2 = pt2.y.evalf()
    styles = {'color':color, 'linestyle':linestyle, 'linewidth':linewidth, 'marker':marker, 'markersize':markersize}
    ax.plot( [x1, x2], [y1, y2], **styles )


def plot_segment2(ax, seg, color='', linestyle='-', linewidth=0, marker='', markersize=0):
    x1 = seg.points[0].x.evalf()
    x2 = seg.points[1].x.evalf()
    y1 = seg.points[0].y.evalf()
    y2 = seg.points[1].y.evalf()
    #  styles = {'color':color, 'linestyle':linestyle, 'linewidth':linewidth, 'marker':marker, 'markersize':markersize}

    styles = classes['default_segment'].copy()
    for cl in seg.classes:
        if cl in classes:
            styles.update(classes[cl])
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
    ax.plot( [x1, x2], [y1, y2], **styles )


def plot_segments(ax, segs):
    for seg in segs:
        plot_segment2(ax, seg)


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

def plot_sequence(ax, sequence, bounds):
    '''plot sequence of all types of elements in layers'''
    seq_pts = [step for step in sequence if isinstance(step, spg.Point2D)]
    seq_polys = [step for step in sequence if isinstance(step, spg.Polygon)]
    seq_segments = [step for step in sequence if isinstance(step, spg.Segment2D)]
    seq_els = [step for step in sequence if isinstance(step, spg.Line2D) or isinstance(step, spg.Circle)]

    highlight_points(ax, seq_pts)
    plot_polygons(ax, seq_polys)
    plot_segments(ax, seq_segments)
    plot_elements(ax, seq_els, bounds)
    plot_points(ax, seq_pts)



def build_sequence(folder, ax, ax_btm, sequence, bounds, margin=1):
    '''create snapshot for each step in sequence'''
    folder = folder + '/sequences'
    for i in range(1, len(sequence)+1):
        last_step = sequence[0:i][-1]
        xlabel = str(last_step)
        typ = '_'
        if isinstance(last_step, spg.Point):
            pt = last_step
            ptx = sp.sqrtdenest(pt.x.simplify())
            pty = sp.sqrtdenest(pt.y.simplify())
            typ = 'point'
            xlabel = f'$\\left( \\ {sp.latex(ptx)}, \\ {sp.latex(pty)} \\ \\right)$'
        if isinstance(last_step, spg.Line):
            a, b, c = last_step.coefficients
            a = a.simplify()
            b = b.simplify()
            c = c.simplify()
            seg = segment(last_step.p1, last_step.p2)
            seg = sp.sqrtdenest(seg.length.simplify())
            typ = 'line'
            xlabel = f'$\\left[ \\ {sp.latex(a)} \\ : \\ {sp.latex(b)} \\ : \\ {sp.latex(c)} \\ \\right]$'
            xlabel += f' • seg: ${sp.latex(seg)}$'
        if isinstance(last_step, spg.Circle):
            eq = last_step.equation().simplify()
            rad = sp.sqrtdenest(last_step.radius.simplify())
            area = sp.sqrtdenest(last_step.area.simplify())
            typ = 'circle'
            #  areaf = str(float(area.evalf()))[0:6]
            areaf = str(round(float(area.evalf()), 4))
            xlabel = f'${sp.latex(eq)}$ • r: ${sp.latex(rad)}$ • A: ${sp.latex(area)}$'
            xlabel += ' $ \\approx ' + areaf + '$'
        if isinstance(last_step, spg.Polygon):
            area = sp.sqrtdenest(last_step.area.simplify())
            perim = sp.sqrtdenest(last_step.perimeter.simplify())
            #  areaf = str(float(area.evalf()))[0:6]
            areaf = str(round(float(area.evalf()), 4))
            #  perimf = str(float(perim.evalf()))[0:6]
            perimf = str(round(float(perim.evalf()), 4))
            typ = 'polygon'
            xlabel = f'area: ${sp.latex(area)}$ • perim: ${sp.latex(perim)}$'
            xlabel += ' $ \\approx ' + perimf + '$'
        if isinstance(last_step, spg.Segment):
            seg = sp.sqrtdenest(last_step.length.simplify())
            segf = str(round(float(seg.evalf()), 4))
            typ = 'segment'
            xlabel = f'seg: ${sp.latex(seg)}$'
            xlabel += ' $ \\approx ' + segf + '$'

        if hasattr(last_step, 'classes') and last_step.classes:
            typ += '-'
            typ += '_'.join(last_step.classes)

        ax_prep(ax, ax_btm, bounds, xlabel)

        if isinstance(last_step, spg.Point):
            plot_selected_points(ax, [last_step])
            parents = list(last_step.parents)
            
            if not pt.classes.count('start'):
                for el in parents:
                    if type(el) == sp.Line2D:
                        plot_line(ax, el, bounds, linestyle='-')
                    elif type(el) == sp.Circle:
                        plot_circle(ax, el, linestyle='-')
        if isinstance(last_step, spg.Line):
            seg = segment(last_step.p1, last_step.p2, classes=['default_line_segment'])
            seg.classes.extend(last_step.classes)
            
            plot_segment2(ax, seg, linestyle='-')
            plot_selected_points(ax, last_step.points)
            plot_line(ax, last_step, bounds, linestyle='-')
        if isinstance(last_step, spg.Circle):
            seg = segment(last_step.center, last_step.radius_pt, classes=['default_circle_segment'])
            seg.classes.extend(last_step.classes)

            plot_segment2(ax, seg, linestyle='-')
            plot_selected_points(ax, [last_step.center, last_step.radius_pt])
            plot_circle(ax, last_step, linestyle='-')
        if isinstance(last_step, spg.Segment):
            plot_selected_points(ax, last_step.points)
        if isinstance(last_step, spg.Polygon):
            plot_selected_points(ax, last_step.vertices)

        plot_sequence(ax, sequence[0:i], bounds)

        filename = f'{str(i).zfill(5)}-{typ}'
        snapshot(folder, f'{filename}.png')

        # zoom around section points
        current_pts = []
        if isinstance(last_step, spg.Point):
            current_pts.append(last_step)
        if isinstance(last_step, spg.Line):
            current_pts.extend(last_step.points)
        if isinstance(last_step, spg.Segment):
            current_pts.extend(last_step.points)
        if isinstance(last_step, spg.Circle):
            bd = last_step.bounds
            pmin = point(bd[0], bd[1])
            pmax = point(bd[2], bd[3])
            current_pts.extend([pmin, pmax])
        if isinstance(last_step, spg.Polygon):
            current_pts.extend(last_step.vertices)

        limx, limy = get_limits_from_points(current_pts, margin=margin)
        limx, limy = adjust_lims(limx, limy)
        ax.set_xlim(limx[0], limx[1])
        ax.set_ylim(limy[0], limy[1])
        
        snapshot(folder, f'{filename}-zoom.png')


def plot_group_sections(NAME, ax, ax_btm, history, sections, bounds, filename, title='golden sections'):
    xlabel = f'[{len(sections)}] • {title}'
    ax_prep(ax, ax_btm, bounds, xlabel)
    section_pts = set()
    group_pts = set()
    for i, section in enumerate(sections):
        num = str(i).zfill(5)
        section_pts = set()
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
        group_pts.update(section_pts)
        gold_points(ax, section_pts)
        plot_segments(ax, section)

    plot_sequence(ax, history, bounds)
    snapshot(f'{NAME}/groups', f'{filename}.png')

    # zoom around section points
    limx, limy = get_limits_from_points(group_pts, margin=.5)
    limx, limy = adjust_lims(limx, limy)
    ax.set_xlim(limx[0], limx[1])
    ax.set_ylim(limy[0], limy[1])
    
    snapshot(f'{NAME}/groups', f'{filename}-zoom.png')


def plot_all_groups(NAME, ax, ax_btm, history, groups, bounds):
    sorted_groups_keys = sorted(groups.keys(), key=lambda key: float(key.evalf()), reverse=True)
    for i, group in enumerate(sorted_groups_keys):
        i = str(i).zfill(5)
        
        groupf = str(float(group.evalf()))[0:6]
        title=f'${sp.latex(group)} \\ \\approx {groupf}\\ldots$'
        plot_group_sections(NAME, ax, ax_btm, history, groups[group], bounds, filename=i, title=title)


def plot_all_ranges(NAME, ax, ax_btm,  history, ranges, bounds):
    xlabel = f'ranges: {len(ranges)}'
    ax_prep(ax, ax_btm,  bounds, xlabel)
    for i, rng in enumerate(ranges):
        gold_points(ax, rng)
        seg = segment(rng[0], rng[3])
        plot_segment2(ax, seg)

    plot_sequence(ax, history, bounds)
    snapshot(f'{NAME}/ranges', f'all.png')


def plot_all_sections(NAME, ax, ax_btm,  history, sections, bounds):
    xlabel = f'golden sections: {len(sections)}'
    all_pts = set()
    ax_prep(ax, ax_btm,  bounds, xlabel)
    for i, section in enumerate(sections):
        #  print(i, section
        num = str(i).zfill(5)
        section_pts = set()
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
                all_pts.add(pt)
        gold_points(ax, section_pts)
        plot_segments(ax, section)

    plot_sequence(ax, history, bounds)
    snapshot(f'{NAME}/sections', f'all.png')

    # zoom around section points
    limx, limy = get_limits_from_points(all_pts, margin=.5)
    limx, limy = adjust_lims(limx, limy)
    ax.set_xlim(limx[0], limx[1])
    ax.set_ylim(limy[0], limy[1])
    
    snapshot(f'{NAME}/sections', f'all-zoom.png')


def adjust_ratio(w, h, r=FIG_W/FIG_H):
    if w / h < r:
        w = r * h
    if w / h > r:
        h = w / r
    return w, h

def adjust_lims(limx, limy, r=FIG_W/(FIG_H-1)):
    w = abs(limx[1] - limx[0])
    h = abs(limy[1] - limy[0])
    w2, h2 = adjust_ratio(w, h, r)
    xdiff = abs(w2 - w) / 2
    ydiff = abs(h2 - h) / 2
    limx[0] -= xdiff
    limx[1] += xdiff
    limy[0] -= ydiff
    limy[1] += ydiff
    return limx, limy


def plot_sections(NAME, ax, ax_btm,  history, sections, bounds):
    for i, section in enumerate(sections):
        num = str(i).zfill(5)
        s0 = section[0].length.simplify()
        s0 = sp.sqrtdenest(s0)
        s0f = str(float(s0.evalf()))[0:6]
        s1 = section[1].length.simplify()
        s1 = sp.sqrtdenest(s1)
        s1f = str(float(s1.evalf()))[0:6]
        xlabel = f'${s0f}\\ldots \\approx \\ {sp.latex(s0)} \\ :\\  {sp.latex(s1)} \\ \\approx {s1f}\\ldots$'
        ax_prep(ax, ax_btm,  bounds, xlabel)
        section_pts = set()
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
        gold_points(ax, section_pts)
        plot_segments(ax, section)
        plot_sequence(ax, history, bounds)
        snapshot(f'{NAME}/sections', f'{num}.png')
        
        # zoom around section points
        limx, limy = get_limits_from_points(section_pts, margin=.5)
        limx, limy = adjust_lims(limx, limy)

        ax.set_xlim(limx[0], limx[1])
        ax.set_ylim(limy[0], limy[1])
        
        snapshot(f'{NAME}/sections', f'{num}-zoom.png')


def plot_ranges(NAME, ax, ax_btm,  history, ranges, bounds):
    '''plot each range from points'''
    for i, rng in enumerate(ranges):
        ad = segment(rng[0], rng[3]).length.simplify()
        cd = segment(rng[2], rng[3]).length.simplify()
        ac = segment(rng[0], rng[2]).length.simplify()
        bc = segment(rng[1], rng[2]).length.simplify()
        #  return sp.simplify((ad / cd) - (ac / bc))
        ratio1 = str(float((ad/cd).evalf()))[0:6]
        ratio2 = str(float((ac/bc).evalf()))[0:6]

        num = str(i).zfill(5)
        xlabel = num
        # escape outer brackers for \frac
        xlabel = f'${ratio1}\\ldots \\approx \\ \\frac {{ {sp.latex(ad)} }} {{{sp.latex(cd)} }}$'
        xlabel += f'  :  '
        xlabel += f'$ \\frac {{ {sp.latex(ac)} }} {{{sp.latex(bc)} }} \\ \\approx {ratio2}\\ldots$'
        ax_prep(ax, ax_btm,  bounds, xlabel)
        #  print(i, rng)
        gold_points(ax, rng)
        seg = segment(rng[0], rng[3])
        plot_segment2(ax, seg)
        plot_sequence(ax, history, bounds)
        snapshot(f'{NAME}/ranges', f'{num}.png')
        
        # zoom around section points
        limx, limy = get_limits_from_points(rng, margin=.5)
        limx, limy = adjust_lims(limx, limy)
        ax.set_xlim(limx[0], limx[1])
        ax.set_ylim(limy[0], limy[1])
        
        snapshot(f'{NAME}/ranges', f'{num}-zoom.png')


# images**********************
def snapshot(folder, filename):
    import os
    sessions = os.path.expanduser('~') + '/Sessions'
    out = f'{sessions}/{folder}/'
    os.makedirs(out, exist_ok=True)
    plt.savefig(out + filename, dpi=120)
    print_log(f'    * {out + filename}')


def display(filename):
    from IPython import display
    display.Image(filename)


def get_bounds_from_sections(sections, r=FIG_W/(FIG_H-1)):
    section_pts = set()
    for i, section in enumerate(sections):
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
    limx, limy = get_limits_from_points(section_pts, margin=.25)
    limx, limy = adjust_lims(limx, limy, r=r)
    bounds = set_bounds(limx, limy)
    return bounds


def get_limits_from_points(pts, margin=1):
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
    

