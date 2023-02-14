'''
GEOMETOR Analyze module

find patterns within a model.
'''

from rich import print

import sympy as sp
import sympy.geometry as spg

from geometor.model import *

goldens = []
groups = {}


def spread(l1: spg.Line, l2: spg.Line):
    '''calculate the spread of two lines'''
    a1, a2, a3 = l1.coefficients
    b1, b2, b3 = l2.coefficients

    spread = ((a1*b2 - a2*b1) ** 2) / ( (a1 ** 2 + b1 ** 2) * (a2 ** 2 + b2 ** 2) )
    return spread


def analyze_summary(NAME, start_time, goldens, groups):
    print_log(f'\nANALYZE Summary: {NAME}')
    print_log(f'    goldens: {len(goldens)}')
    print_log(f'    groups: {len(groups)}')
    print_log(f'\nelapsed: {elapsed(start_time)}')


def find_golden_sections(model):
    """TODO: Docstring for find_golden_sections.

    :model: TODO
    :returns: TODO

    """
    pass

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


def analyze_golden(model):
    sections = []
    sections_by_line = {}

    lines = model.lines()

    print_log(f'\n    analyze_golden_lines: {len(lines)}')

    for i, line in enumerate(model.lines()):
        print_log(f'    {i} • {line.coefficients}')
        line_pts = model.parents[line]
        line_sections = analyze_golden_line(line_pts)
        sections.extend(line_sections)
        sections_by_line[line] = line_sections
        print(line_sections)

    return sections, sections_by_line


def analyze_golden_line(line_pts):
    '''check all the points on a line for Golden Sections
    returns a list of golden section pairs '''
    goldens = []
    print(line_pts)
    line_pts = sort_points(line_pts)

    # this will walk the combinations of three points down the line
    sections = list(combinations(line_pts, 3))
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
    #  test_pts = sorted(list(test_pts), key=point_value)
    test_pts = sort_points(test_pts)
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


def analyze_model(m: Model):
    '''Analyze all lines in model for golden sections'''
    print_log(f'\nanalyze_model:')

    goldens = analyze_golden_lines(m.lines())
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
    groups = defaultdict(list)
    for section in sections:
        for seg in section:
            seg_len = seg.length.simplify()
            seg_len = sp.sqrtdenest(seg_len)

            groups[seg_len].append(section)
    return groups


