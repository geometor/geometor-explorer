"""
elements module
===============
"""

from .common import *

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

