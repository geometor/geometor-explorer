'''
The Render Module
provides functions for plotting elements from the geoemtric model to
matplotlib.
'''

from .common import *

from ..model import *
from ..utils import *

from .utils import *
from .colors import *
from .styles import *
from .plot_elements import *
from .points import *
from .segments import *
from .polygons import *
from .wedges import *

plt.rcParams['figure.figsize'] = [FIG_W, FIG_H]
plt.style.use('dark_background')


def plot_model(plot_name, ax, ax_label, model, margin=1):
    '''\
    plot sequence of all types of elements in layers

    '''

    # clear the axis - add the label
    ax.clear()
    ax.axis(False)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    ax_label.clear()
    ax_label.axis(False)

    # find boundary
    # TODO: bounds are rquired for extents of lines
    limx, limy = get_limits_from_points(model.points(), margin=margin)
    limx, limy = adjust_lims(limx, limy)
    bounds = set_bounds(limx, limy)

    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]
    ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))


    for i, el in enumerate(model):
        el_classes = model.classes[el]
        el_parents = model.parents[el]

        # gather info for xlabel
        # point
        if isinstance(el, spg.Point):
            typ = 'point'
            ptx = sp.sqrtdenest(el.x.simplify())
            pty = sp.sqrtdenest(el.y.simplify())
            xlabel = f'$\\left( \\ {sp.latex(ptx)}, \\ {sp.latex(pty)} \\ \\right)$'

        # line
        if isinstance(el, spg.Line):
            typ = 'line'
            a, b, c = el.coefficients
            a = a.simplify()
            b = b.simplify()
            c = c.simplify()
            seg = segment(el.p1, el.p2)
            seg = sp.sqrtdenest(seg.length.simplify())

            xlabel = f'$\\left[ \\ {sp.latex(a)} \\ : \\ {sp.latex(b)} \\ : \\ {sp.latex(c)} \\ \\right]$'
            xlabel += f' • seg: ${sp.latex(seg)}$'

        # circle
        if isinstance(el, spg.Circle):
            typ = 'circle'
            eq = el.equation().simplify()
            rad = sp.sqrtdenest(el.radius.simplify())
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))

            xlabel = f'${sp.latex(eq)}$ • r: ${sp.latex(rad)}$ • A: ${sp.latex(area)}$'
            xlabel += ' $ \\approx ' + areaf + '$'

        # polygon
        if isinstance(el, spg.Polygon):
            typ = 'polygon'
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            perim = sp.sqrtdenest(el.perimeter.simplify())
            perimf = str(round(float(perim.evalf()), 4))

            xlabel = f'area: ${sp.latex(area)}$ • perim: ${sp.latex(perim)}$'
            xlabel += ' $ \\approx ' + perimf + '$'

        # segment
        if isinstance(el, spg.Segment):
            typ = 'segment'
            seg = sp.sqrtdenest(el.length.simplify())
            segf = str(round(float(seg.evalf()), 4))

            xlabel = f'seg: ${sp.latex(seg)}$'
            xlabel += ' $ \\approx ' + segf + '$'

        # add classes to type name
        if el_classes:
            typ += '-'
            typ += '_'.join(el_classes)

        print(typ)
        print(xlabel)
        print()

        selected = []

        # point
        if isinstance(el, spg.Point):
            plot_point(ax, el, el_classes)
            selected.append(plot_selected_points(ax, [el]))
            #  for parent in el_parents:
                #  if isinstance(parent, spg.Line):
                    #  plot_line(ax, parent, bounds, linestyle='-')
                #  if isinstance(parent, spg.Circle):
                    #  plot_circle(ax, parent, linestyle='-')

        # line
        if isinstance(el, spg.Line):
            plot_line(ax, el, el_classes, bounds)

            selected.append(plot_selected_points(ax, [el.points]))
            #  seg = segment(el.p1, el.p2, classes=['default_line_segment'])
            #  seg.classes.extend(el.classes)

            #  plot_segment2(ax, seg, linestyle='-')
            #  plot_line(ax, el, bounds, linestyle='-')


        if False:

            # circle
            if isinstance(el, spg.Circle):
                seg = segment(el.center, el.radius_pt, classes=['default_circle_segment'])
                seg.classes.extend(el.classes)

                plot_segment2(ax, seg, linestyle='-')
                plot_selected_points(ax, [el.center, el.radius_pt])
                plot_circle(ax, el, linestyle='-')

            # segment
            if isinstance(el, spg.Segment):
                plot_selected_points(ax, el.points)

            # polygon
            if isinstance(el, spg.Polygon):
                plot_selected_points(ax, el.vertices)

        ax_label.clear()
        ax_label.axis(False)
        ax_label.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})

        filename = f'{str(i).zfill(5)}-{typ}'
        snapshot(plot_name + '/sequences', f'{filename}.png')

        for select in selected:
            selected_el = select.pop(0)
            selected_el.remove()


    xlabel = f'elements: {len(model)} | points: {len(model.points())}'
    ax_label.clear()
    ax_label.axis(False)
    ax_label.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})

    print(xlabel)

    snapshot(plot_name + '/sequences', 'summary.png')

    #  highlight_points(ax, seq_pts)
    #  plot_polygons(ax, seq_polys)
    #  plot_segments(ax, seq_segments)
    #  plot_elements(ax, seq_els, bounds)
    #  plot_points(ax, seq_pts)

def plot_sequence(ax, sequence, bounds):
    '''plot sequence of all types of elements in layers
    TODO: adapt model class

    '''
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
            #  for parent in parents:
                #  if isinstance(parent, spg.Line):
                    #  plot_line(ax, parent, bounds, linestyle='-')
                #  if isinstance(parent, spg.Circle):
                    #  plot_circle(ax, parent, linestyle='-')

            if not last_step.classes.count('start'):
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
    snapshot(f'{NAME}/ranges', f'summary.png')


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
    snapshot(f'{NAME}/sections', f'summary.png')

    # zoom around section points
    limx, limy = get_limits_from_points(all_pts, margin=.5)
    limx, limy = adjust_lims(limx, limy)
    ax.set_xlim(limx[0], limx[1])
    ax.set_ylim(limy[0], limy[1])

    snapshot(f'{NAME}/sections', f'summary-zoom.png')


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


