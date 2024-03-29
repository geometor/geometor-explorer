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


def plot_label(ax_label, i, xlabel, el_label):
    ax_label.clear()
    ax_label.axis(False)
    ax_label.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})
    ax_label.text(0, 0.5, i, ha='left', va='center', fontdict={'color': 'r', 'size':'24'})
    if el_label:
        el_label = f'${el_label}$'
    ax_label.text(1, 0.5, el_label, ha='right', va='center', fontdict={'color': 'r', 'size':'24'})



def plot_model(plot_name, ax, ax_label, M, margin=0.1):
    '''\
    plot sequence of all types of elements in layers

    '''

    cursor_points = []

    # clear the axis - add the label
    ax.clear()
    ax.axis(False)
    ax.set_aspect('equal')
    #  ax.set_xticks([-1, 0, 1], labels=[r'$-1$', '$0$', '$1$'])
    #  ax.set_xticks([0.5], labels=[r'$\frac{1}{2}$'], minor=True)

    #  ax.tick_params(color='#222222', labelcolor='#999999', grid_color='#222222')
    #  ax.set_yticks([-1, 0, 1], labels=[-1, 0, 1 ])

    ax_label.clear()
    ax_label.axis(False)

    # find boundary
    # TODO: bounds are rquired for extents of lines
    #  limx, limy = get_limits_from_points(model.points(), margin=margin)
    limx, limy = M.limits()
    limx, limy = adjust_lims(limx, limy, ratio=1)
    bounds = set_bounds(limx, limy)

    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]

    ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))
    ax.invert_yaxis()


    for i, el in enumerate(M):
        el_classes = M.classes[el]
        el_parents = list(M.parents[el])[0:2]
        el_label = M.labels[el]

        selected = []


        # point
        if isinstance(el, spg.Point):
            typ = 'point'
            ptx = sp.sqrtdenest(el.x.simplify())
            pty = sp.sqrtdenest(el.y.simplify())
            xlabel = f'$\\left[ \\ {sp.latex(ptx)}, \\ {sp.latex(pty)} \\ \\right]$'

            pt_inner, *pts = plot_point(ax, el, M, el_classes)
            cursor_points.append(pt_inner.pop())
            selected.append(plot_selected_points(ax, [el]))
            if 'given' not in el_classes:
                for parent in el_parents:
                    if isinstance(parent, spg.Line):
                        selected.append(plot_line(ax, parent, [], bounds, linestyle='-'))
                    if isinstance(parent, spg.Circle):
                        selected.append(plot_circle(ax, parent, [], linestyle='-'))

        # line
        if isinstance(el, spg.Line):
            typ = 'line'
            eq = el.equation().simplify()
            xlabel = f'${sp.latex(eq)} = 0$'
            #  a, b, c = el.coefficients
            #  a = a.simplify()
            #  b = b.simplify()
            #  c = c.simplify()
            #  seg = segment(el.p1, el.p2)
            #  seg = sp.sqrtdenest(seg.length.simplify())

            pt1_label = M.labels[el.p1]
            pt2_label = M.labels[el.p2]
            el_label = r'\overline{' + pt1_label + pt2_label + '}'

            #  xlabel = f'$\\left[ \\ {sp.latex(a)} \\ : \\ {sp.latex(b)} \\ : \\ {sp.latex(c)} \\ \\right]$'
            #  xlabel += f' • seg: ${sp.latex(seg)}$'

            plot_line(ax, el, el_classes, bounds)

            selected.append(plot_selected_points(ax, el.points))

            seg = segment(el.p1, el.p2)
            seg_classes=['default_line_segment']
            seg_classes.extend(el_classes)

            selected.append(plot_segment2(ax, seg, seg_classes, linestyle='-'))
            selected.append(plot_line(ax, el, el_classes, bounds, linestyle='-'))

        # circle
        if isinstance(el, spg.Circle):
            typ = 'circle'
            eq = el.equation().simplify()
            rad = sp.sqrtdenest(el.radius.simplify())
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))

            xlabel = f'${sp.latex(eq)} = 0$'
            #  xlabel = f'${sp.latex(eq)}$ • r: ${sp.latex(rad)}$ • A: ${sp.latex(area)}$'
            #  xlabel += ' $ \\approx ' + areaf + '$'

            pt1_label = M.labels[el.center]
            pt2_label = M.labels[el.radius_pt]
            el_label = f'({pt1_label}, {pt2_label})'

            plot_circle(ax, el, el_classes)

            seg = segment(el.center, el.radius_pt)
            seg_classes=['default_line_segment']
            circle_styles = STYLES['default_circle']
            seg_classes.extend(el_classes)

            selected.append(plot_segment2(ax, seg, seg_classes, color=circle_styles['edgecolor'], linestyle='-'))
            selected.append(plot_selected_points(ax, [el.center, el.radius_pt]))
            selected.append(plot_circle(ax, el, el_classes, linestyle='-'))


        # segment
        if isinstance(el, spg.Segment):
            typ = 'segment'
            seg = sp.sqrtdenest(el.length.simplify())
            segf = str(round(float(seg.evalf()), 4))

            xlabel = f'seg: ${sp.latex(seg)}$'
            xlabel += ' $ \\approx ' + segf + '$'

            plot_segment2(ax, el, el_classes)
            selected.append(plot_selected_points(ax, el.points))

        # polygon
        if isinstance(el, spg.Polygon):
            typ = 'polygon'
            area = sp.sqrtdenest(el.area.simplify())
            areaf = str(round(float(area.evalf()), 4))
            perim = sp.sqrtdenest(el.perimeter.simplify())
            perimf = str(round(float(perim.evalf()), 4))

            xlabel = f'area: ${sp.latex(area)}$ • perim: ${sp.latex(perim)}$'
            xlabel += ' $ \\approx ' + perimf + '$'

            # TODO: refactor plygons
            plot_polygon(ax, [el])
            selected.append(plot_selected_points(ax, el.vertices))

        # add classes to type name
        if el_classes:
            typ += '-'
            typ += '_'.join(el_classes)

        print(typ)
        print(xlabel)
        print()

        plot_label(ax_label, f'{i:03}', xlabel, el_label)

        filename = f'{str(i).zfill(5)}-{typ}'
        snapshot_2(f'./{plot_name}/step', f'{filename}.png')
        snapshot_2(f'./{plot_name}/step', f'{filename}.svg')

        for select in selected:
            selected_el = select.pop(0)
            selected_el.remove()



    xlabel = f'elements: {len(M)} | points: {len(M.points())}'
    plot_label(ax_label, '', xlabel, '')

    print(xlabel)

    snapshot_2(f'./{plot_name}/step', 'summary.png')
    snapshot_2(f'./{plot_name}/step', 'summary.svg')

    mplcursors.cursor(cursor_points, highlight=True)



def plot_sections(NAME, ax, ax_label, sections ):
    bounds = get_bounds_from_sections(sections)

    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]

    for i, section in enumerate(sections):
        num = str(i).zfill(5)

        s0 = section[0].length.simplify()
        s0 = sp.sqrtdenest(s0)
        s0f = str(float(s0.evalf()))[0:6]
        s1 = section[1].length.simplify()
        s1 = sp.sqrtdenest(s1)
        s1f = str(float(s1.evalf()))[0:6]
        xlabel = f'${s0f}\\ldots \\approx \\ {sp.latex(s0)} \\ :\\  {sp.latex(s1)} \\ \\approx {s1f}\\ldots$'

        section_pts = set()
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)

        selected = []

        selected.append(gold_points(ax, section_pts ))
        selected.extend(plot_segments(ax, section))

        ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
        ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))

        plot_label(ax_label, '', xlabel, '')

        snapshot(f'{NAME}/sections', f'{num}.png')

        # zoom around section points
        limx, limy = get_limits_from_points(section_pts, margin=.5)
        limx, limy = adjust_lims(limx, limy)

        ax.set_xlim(limx[0], limx[1])
        ax.set_ylim(limy[0], limy[1])

        snapshot(f'{NAME}/sections', f'{num}-zoom.png')

        for select in selected:
            selected_el = select.pop(0)
            selected_el.remove()


def plot_all_sections(NAME, ax, ax_label,  model, sections):
    xlabel = f'golden sections: {len(sections)}'
    all_pts = set()

    selected = []

    for i, section in enumerate(sections):
        #  print(i, section
        num = str(i).zfill(5)
        section_pts = set()
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
                all_pts.add(pt)

        selected.append(gold_points(ax, section_pts ))
        selected.extend(plot_segments(ax, section))

    limx, limy = get_limits_from_points(model.points())
    limx, limy = adjust_lims(limx, limy)
    ax.set_xlim(limx[0], limx[1])
    ax.set_ylim(limy[0], limy[1])

    plot_label(ax_label, '', xlabel, '')

    snapshot(f'{NAME}/sections', f'summary.png')

    # zoom around section points
    limx, limy = get_limits_from_points(all_pts, margin=.5)
    limx, limy = adjust_lims(limx, limy)
    ax.set_xlim(limx[0], limx[1])
    ax.set_ylim(limy[0], limy[1])

    snapshot(f'{NAME}/sections', f'summary-zoom.png')

    for select in selected:
        selected_el = select.pop(0)
        selected_el.remove()



def plot_group_sections(NAME, ax, ax_label, model, sections, filename, title='golden sections'):
    xlabel = f'[{len(sections)}] • {title}'
    section_pts = set()
    group_pts = set()

    selected = []

    for i, section in enumerate(sections):
        num = str(i).zfill(5)
        section_pts = set()
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
        group_pts.update(section_pts)

        selected.append(gold_points(ax, section_pts ))
        selected.extend(plot_segments(ax, section))

    plot_label(ax_label, '', xlabel, '')

    snapshot(f'{NAME}/groups', f'{filename}.png')

    # zoom around section points
    limx, limy = get_limits_from_points(group_pts, margin=.5)
    limx, limy = adjust_lims(limx, limy)
    ax.set_xlim(limx[0], limx[1])
    ax.set_ylim(limy[0], limy[1])

    snapshot(f'{NAME}/groups', f'{filename}-zoom.png')

    for select in selected:
        selected_el = select.pop(0)
        selected_el.remove()


def plot_all_groups(NAME, ax, ax_label, model, groups):
    sorted_groups_keys = sorted(groups.keys(), key=lambda key: float(key.evalf()), reverse=True)
    for i, group in enumerate(sorted_groups_keys):
        i = str(i).zfill(5)

        groupf = str(float(group.evalf()))[0:6]
        title=f'${sp.latex(group)} \\ \\approx {groupf}\\ldots$'
        plot_group_sections(NAME, ax, ax_label, model, groups[group], filename=i, title=title)


def plot_all_ranges(NAME, ax, ax_btm,  history, ranges, bounds):
    xlabel = f'ranges: {len(ranges)}'
    ax_prep(ax, ax_btm,  bounds, xlabel)
    for i, rng in enumerate(ranges):
        gold_points(ax, rng)
        seg = segment(rng[0], rng[3])
        plot_segment2(ax, seg)

    plot_sequence(ax, history, bounds)
    snapshot(f'{NAME}/ranges', f'summary.png')


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


