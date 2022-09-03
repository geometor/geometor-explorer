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




def get_elements_by_class(classname):
    '''find all elements with specifdied classname'''
    elements_by_class = []
    for el in elements:
        if el.classes.count(classname):
            elements_by_class.append(el)
    return elements_by_class



