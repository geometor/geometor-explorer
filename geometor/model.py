'''
The Model module provides a set of tools for constructing geometric models.
It relies heavily on sympy for providing the algebraic infrastructure
the functions here are for creating the abstract model, not the rendering
see the Render module for plotting with matplotlib
'''
import sympy as sp
import sympy.plotting as spp
import sympy.geometry as spg
from sympy.abc import x, y

import math as math
import numpy as np
from collections import defaultdict
import logging

from itertools import permutations, combinations
from multiprocessing import Pool, cpu_count

from geometor.utils import *
#  from geometor.render import *

# constants
num_workers = cpu_count()

Φ = sp.GoldenRatio
phi = sp.Rational(1, 2) + (sp.sqrt(5) / 2)

# globals
history = []
pts = []
elements = []
polygons = []
goldens = []
groups = {}


def set_bounds(limx, limy):
    return sp.Polygon(
        point(limx[0], limy[1]),
        point(limx[0], limy[0]),
        point(limx[1], limy[0]),
        point(limx[1], limy[1])
        )

# structural elements
def point(x_val, y_val, parents=set(), classes=[], style={}):
    '''make sympy.geometry.Point'''
    pt = spg.Point(sp.simplify(x_val), sp.simplify(y_val))
    pt.parents = parents
    pt.elements = parents
    pt.classes = classes
    pt.style = style
    return pt


def line(pt_a, pt_b, classes=[], style={}):
    '''make sympy.geometry.Line'''
    el = spg.Line(pt_a, pt_b)
    el.pts = {pt_a, pt_b}
    el.classes = classes
    el.style = style
    return el


def circle(pt_c, pt_r, classes=[], style={}):
    '''make sympy.geometry.Circle from two points'''
    el = spg.Circle(pt_c, pt_c.distance(pt_r))
    el.radius_pt = pt_r
    el.pts = {pt_r}
    el.classes = classes
    el.style = style
    return el


# graphical elements
def segment(pt_a, pt_b, classes=[], style={}):
    '''make sympy.geometry.Segment'''
    el = spg.Segment(pt_a, pt_b)
    el.classes = classes
    el.style = style
    return el


def polygon(poly_pts, classes=[], style={}):
    '''- takes array of points - make sympy.geometry.Polygon, Triangle or Segment'''
    el = spg.Polygon(*poly_pts)
    el.classes = classes
    el.style = style
    return el


def polygon_ids(ids, classes=[], style={}):
    '''create polygon from list of point ids'''
    return polygon([pts[i] for i in ids], classes=classes, style=style)


def unit_square(pt, classes=[], style={}):
    '''creates a unit square from the reference point
    adds points and returns polygon'''
    poly_pts = []
    poly_pts.append(pt)
    poly_pts.append(point(pt.x + 1, pt.y))
    poly_pts.append(point(pt.x + 1, pt.y + 1))
    poly_pts.append(point(pt.x, pt.y + 1))
    return polygon(poly_pts, classes=classes, style=style)



# model ******************************

def find_pt_index(pt):
    if isinstance(pt, spg.Point2D):
        for i, prev_pt in enumerate(pts):
            if pt.equals(prev_pt):
                #  i = pts.index(prev_pt)
                print_log(f'  ! {pt} found at index: {i}')
                return i
    else:
        return -1
    
def add_point(pt):
    '''add point to pts list - check if exists first'''
    logging.info(f'* add_point: {pt}')
    if isinstance(pt, spg.Point2D):
        # make new point with simplified values 
        x = sp.sqrtdenest(pt.x.simplify())
        y = sp.sqrtdenest(pt.y.simplify())
        pt = point(x, y, classes=pt.classes)
        for prev_pt in pts:
            if pt.equals(prev_pt):
                i = pts.index(prev_pt)
                logging.info(f'  ! {pt} found at index: {i}')
                # merge parents of points
                if hasattr(pt, 'elements'):
                    if hasattr(prev_pt, 'elements'):
                        prev_pt.elements.update(pt.elements)
                return prev_pt
        else:
            pts.append(pt)
            history.append(pt)
            logging.info(f'  + {pt}')
            return pt
    else:
        logging.info('    not a point')


def add_points(pt_array):
    '''add an array of points to pts list'''
    for pt in pt_array:
        add_point(pt)


def add_intersection_points(el):
    logging.info(f'* add_intersection_points: {el}')
    for prev in elements:
        for pt in el.intersection(prev):
            pt.classes = []
            pt.elements = {el, elements[index]}
            add_point(pt)

            
def add_intersection_points_mp(el):
    logging.info(f'* add_intersection_points: {el}')
    with Pool(num_workers) as pool:
        results = pool.map(el.intersection, elements)
        for index, result in enumerate(results):
            for pt in result:
                pt.classes = []
                pt.elements = set()
                pt.elements.update({el, elements[index]})
                if not hasattr(pt, 'parents'):
                    if not pt.classes.count('start'):
                        pt.parents = set()
                        pt.parents.update({el, elements[index]})
                pt = add_point(pt)
                el.pts.add(pt)
                elements[index].pts.add(pt)


def add_element(el):
    print_log(f'* add_element: {el}')
    # check if el is in the element list
    if not elements.count(el):
        # if not found by count, test each element anyway
        for prev in elements:

            #TODO: refine test of elements
            diff = (prev.equation().simplify() - el.equation().simplify()).simplify()
            #  logging.info(f'    > diff: {diff}')
            if not diff:
                logging.info(f'''
            ! COINCIDENT
                {el}
                {prev}
                ''')
                return prev
        else:
            history.append(el)
            add_intersection_points_mp(el)
            elements.append(el)
            logging.info(f'  + {el}')
            return el
    else:
        i = elements.index(el)
        logging.info(f'  ! {el} found at index: {i}')
        return elements[i]

def add_polygon(poly):
    polygons.append(poly)
    history.append(poly)
    return poly
    
# helpers ******************************
def begin():
    '''create inital two points -
    establishing the unit for the field'''
    A = point(sp.Rational(-1, 2), 0, classes=['start'])
    add_point(A)
    B = point(sp.Rational(1, 2), 0, classes=['start'])
    add_point(B)
    return A, B

def begin_zero():
    '''create inital two points -
    establishing the unit for the field'''
    A = point(0, 0, classes=['start'])
    add_point(A)
    B = point(1, 0, classes=['start'])
    add_point(B)
    return A, B

    
def bisector(pt1, pt2):
    '''perform fundamental operations for two points
    and add perpendicular bisector'''

    # baseline
    add_element(line(pt1, pt2))

    # vesica
    c1 = add_element(circle(pt1, pt2))
    c2 = add_element(circle(pt2, pt1))

    # bisector
    # last two points should be from the last two circles intersection
    el = line(pts[-1], pts[-2], classes=['bisector'])
    add_element(el)

    
def get_pts_by_class(classname):
    '''find all points with specifdied classname'''
    pts_by_class = []
    for pt in pts:
        if pt.classes.count(classname):
            pts_by_class.append(pt)
    return pts_by_class

def get_elements_by_class(classname):
    '''find all elements with specifdied classname'''
    elements_by_class = []
    for el in elements:
        if el.classes.count(classname):
            elements_by_class.append(el)
    return elements_by_class


def line_get_y(l1, x):
    '''return y value for specific x'''
    a, b, c = l1.coefficients
    return (-a * x - c) / b


def spread(l1, l2):
    '''calculate the spread of two lines'''
    a1, a2, a3 = l1.coefficients
    b1, b2, b3 = l2.coefficients

    spread = ((a1*b2 - a2*b1) ** 2) / ( (a1 ** 2 + b1 ** 2) * (a2 ** 2 + b2 ** 2) )
    return spread


def compare_points(pt1, pt2):
    if pt1.x.evalf() > pt2.x.evalf():
        return 1
    elif pt1.x.evalf() < pt2.x.evalf():
        return -1
    else:
        if pt1.y.evalf() > pt2.y.evalf():
            return 1
        elif pt1.y.evalf() < pt2.y.evalf():
            return -1
        else:
            return 0

def point_value(pt):
    #  return pt.x.evalf()
    return (pt.x.evalf(), pt.y.evalf())



def check_golden(section):
    '''check range of three points for golden section'''
    ab = segment(section[0], section[1]).length.simplify()
    bc = segment(section[1], section[2]).length.simplify()
    #  print('            ', ab)
    #  print('            ', bc)
    #  ratio = ab ** 2 / bc ** 2
    ratio = ab / bc 
    #  ratio = sp.simplify(ratio)
    #  print('            ', ratio)
    chk1 = (ratio / phi).evalf()
    #  print('            ', chk1)
    chk2 = (ratio / (1 / phi)).evalf()
    #  print('            ', chk2)
    #  if ratio == (1 / phi) or ratio == (phi):
    if chk1 == 1 or chk2 == 1:
        return True
    else:
        return False
    

def analyze_golden_lines(lines):
    sections = []

    print_log(f'\n    analyze_golden_lines: {len(lines)}')

    for i, el in enumerate(lines):
        print_log(f'    {i} • {el.coefficients}')
        sections.extend(analyze_golden(el))
    
    return sections


def analyze_golden(line):
    '''check all the points on a line for Golden Sections'''
    goldens = []
    line_pts = sorted(list(line.pts), key=point_value)
    sections = list(combinations(line_pts, 3))
    print_log(f'        coefficients: {line.coefficients})')
    print_log(f'        points:    {len(line_pts)}')
    print_log(f'        sections:  {len(sections)}')

    with Pool(num_workers) as pool:
        results = pool.map(check_golden, sections)
        for index, result in enumerate(results):
            if result:
                section = sections[index]
                ab = segment(section[0], section[1])
                bc = segment(section[1], section[2])
                goldens.append([ab, bc])
                logging.info(f'            GOLDEN: {sections[index]}')
            
    print_log(f'        goldens: { len(goldens) }')
    return goldens
    
def analyze_golden_pts(test_pts):
    '''check all the points on a line for Golden Sections'''
    goldens = []
    test_pts = sorted(list(test_pts), key=point_value)
    sections = list(combinations(test_pts, 3))
    print_log(f'        points:    {len(test_pts)}')
    print_log(f'        sections:  {len(sections)}')

    with Pool(num_workers) as pool:
        results = pool.map(check_golden, sections)
        for index, result in enumerate(results):
            if result:
                section = sections[index]
                ab = segment(section[0], section[1])
                bc = segment(section[1], section[2])
                goldens.append([ab, bc])
                logging.info(f'            GOLDEN: {sections[index]}')
            
    print_log(f'        goldens: { len(goldens) }')
    return goldens
    

def get_elements_lines():
    return [el for el in elements if isinstance(el, spg.Line2D)]


def get_elements_circles():
    return [el for el in elements if isinstance(el, spg.Circle)]


def analyze_model():
    '''Analyze all lines in model for golden sections'''
    print_log(f'\nanalyze_model:')

    lines = get_elements_lines()
    goldens = analyze_golden_lines(lines)
    groups = group_sections(goldens)

    return goldens, groups


def check_range(r):
    ad = segment(r[0], r[3]).length
    cd = segment(r[2], r[3]).length
    ac = segment(r[0], r[2]).length
    bc = segment(r[1], r[2]).length
    return sp.simplify((ad / cd) - (ac / bc))
    

def analyze_harmonics(line):
    line_pts = sorted(list(line.pts), key=point_value)
    #  for pt in line_pts:
        #  print(pt.x, pt.x.evalf(), pt.y, pt.y.evalf())
    ranges = list(combinations(line_pts, 4))
    harmonics = []
    for i, r in enumerate(ranges):
        chk = check_range(r)
        #  if chk == 1 or chk == -1:
        #  if chk == 0 or chk == -1:
        if chk == 0:
            print(i, chk)
            print(f'    {r}')
            harmonics.append(r)
    return harmonics
    

def group_sections(sections):
    groups = {}
    for section in sections:
        for seg in section:
            seg_len = seg.length.simplify()
            seg_len = sp.sqrtdenest(seg_len)
            if seg_len in groups:
                groups[seg_len].append(section)
            else:
                groups[seg_len] = [section]
    return groups



def model_summary(NAME, start_time):
    print_log(f'\nMODEL Summary: {NAME}')
    print_log(f'    history: {len(history)}')
    print_log(f'    elements: {len(elements)}')
    lines = get_elements_lines()
    print_log(f'        lines: {len(lines)}')
    circles = get_elements_circles()
    print_log(f'        circles: {len(circles)}')
    print_log(f'    points: {len(pts)}')
    print_log(f'\nelapsed: {elapsed(start_time)}')


def analyze_summary(NAME, start_time, goldens, groups):
    print_log(f'\nANALYZE Summary: {NAME}')
    print_log(f'    goldens: {len(goldens)}')
    print_log(f'    groups: {len(groups)}')
    print_log(f'\nelapsed: {elapsed(start_time)}')


def complete_summary(NAME, start_time, goldens, groups): 
    print_log(f'\nCOMPLETE: {NAME}')
    print_log(f'    elements: {len(elements)}')
    lines = get_elements_lines()
    print_log(f'        lines: {len(lines)}')
    circles = get_elements_circles()
    print_log(f'        circles: {len(circles)}')
    print_log(f'    points:   {len(pts)}')
    print_log(f'    ---')
    print_log(f'    goldens: {len(goldens)}')
    print_log(f'    groups: {len(groups)}')
    print_log(f'\nelapsed: {elapsed(start_time)}')
          

def bisect_pts(pt1, pt2):
    '''use sympy function
    add prpoerties to line
    return line'''
    seg = segment(pt1, pt2)
    ln = seg.perpendicular_bisector()
    ln.classes = ['bisector']
    ln.parents = {pt1, pt2}
    ln.pts = set()
    return ln

def bisect_pts2(pt1, pt2):
    '''use circles but don't add to model'''
    c1 = circle(pt1, pt2)
    c2 = circle(pt2, pt1)
    ints = c1.intersection(c2)
    ln = line(ints[0], ints[1])
    ln.classes = ['bisector']
    ln.parents = {pt1, pt2, ints[0], ints[1]}
    ln.pts = set()
    return ln

def bisect_lines(ln1, ln2):
    lns = ln1.bisectors(ln2)
    for ln in lns:
        ln.classes = ['bisector']
        ln.parents = {ln1.p1, ln1.p2, ln2.p1, ln2.p2}
        ln.pts = set()
    return lns


