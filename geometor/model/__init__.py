'''
The Model module provides a set of tools for constructing geometric models.
It relies heavily on sympy for providing the algebraic infrastructure
the functions here are for creating the abstract model, not the rendering
see the Render module for plotting with matplotlib
'''
from .common import *

from .points import *
from .lines import *
from .circles import *
from .polygons import *
from .polynomials import *
from .elements import *
from .history import *

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



# graphical elements
def segment(pt_a, pt_b, classes=[], style={}):
    '''make sympy.geometry.Segment'''
    el = spg.Segment(pt_a, pt_b)
    el.classes = classes
    el.style = style
    return el




# model ******************************


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
    '''Add ``line`` or ``circle`` to ``elements`` and ``history`` list. 
    check for duplicates in elements.
    find intersection points for new element with all precedng elements'''
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
    line_pts = sort_points(line.pts)
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


