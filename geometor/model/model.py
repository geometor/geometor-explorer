"""
Model module
============

"""

import sympy as sp
import sympy.plotting as spp
import sympy.geometry as spg
import logging
from collections import defaultdict
from geometor.utils import *

class Model(list):

    """Docstring for Model. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__(self)
        self.parents = defaultdict(set)
        self.classes = defaultdict(list)
        

    def points(self) -> list:
        """filter points from model
        :returns: list

        """
        return [el for el in self if isinstance(el, spg.Point)]
        

    def gen_point(self, x_val, y_val, parents=set(), classes=[]) -> spg.Point:
        '''generate a sympy.geometry.Point'''
        x_val = sp.simplify(x_val)
        y_val = sp.simplify(y_val)
        pt = spg.Point(x_val, y_val)
        return self.add_point(pt, parents, classes)


    def add_point(self, pt: spg.Point, parents=set(), classes=[]) -> spg.Point:
        '''add point to model
        find duplicates
        clean values
        set parents and classes'''
        #  logging.info(f'* add_point: {pt}')
        if isinstance(pt, spg.Point):
            # make new point with simplified values 
            x = sp.sqrtdenest(pt.x.simplify())
            y = sp.sqrtdenest(pt.y.simplify())
            pt = spg.Point(x, y)
            if pt in self.points():
                # add attributes
                self.parents[pt].update(parents)
                self.classes[pt].extend(classes)
                return pt
                
            else:
                for prev_pt in self.points():
                    if pt.equals(prev_pt):
                        self.parents[prev_pt].update(parents)
                        self.classes[prev_pt].extend(classes)
                        return prev_pt

            #  logging.info(f'  + {pt}')
            self.append(pt)
            self.parents[pt].update(parents)
            self.classes[pt].extend(classes)
            return pt
        else:
            logging.info('    not a point')

    def add_line(self, struct: spg.Line, parents=set(), classes=[]) -> spg.Line:
        '''
        Add ``line`` to list. 
        check for duplicates in elements.
        find intersection points for new element with all precedng elements
        '''
        # check if el is in the element list
        if isinstance(struct, spg.Line):
            # check by reference
            if struct in self.lines():
                print_log('struct exists')
                self.parents[struct].update(parents)
                self.classes[struct].extend(classes)
                return struct
            else:
                # double check by value
                for prev in self.lines():
                    #TODO: refine test of elements
                    diff = (prev.equation().simplify() - el.equation().simplify()).simplify()
                    #  logging.info(f'    > diff: {diff}')
                    if not diff:
                        logging.info(f'''
                    ! COINCIDENT
                        {el}
                        {prev}
                        ''')
                        self.parents[prev].update(parents)
                        self.classes[prev].extend(classes)
                        return prev
                else:

                    # add struct
                    self.append(struct)
                    self.parents[struct].update(parents)
                    self.classes[struct].extend(classes)
                    # check intersections
                    for prev in self.structs():
                        if not struct.equals(prev):
                            results = struct.intersection(prev)
                            for pt in results:
                                self.add_point(pt, parents={prev, struct})
                    return struct
        else:
            print_log('not a line')
    

    def structs(self):
        """
        filtered list of structs 
        currently lines and circles
        """
        return [el for el in self if isinstance(el, spg.Line) or isinstance(el, spg.Circle)]

    def lines(self):
        """
        filtered list of lines
        """
        return [el for el in self if isinstance(el, spg.Line)]


    def circles(self):
        return [el for el in self if isinstance(el, spg.Circle)]

    def summary(self, name = ''):
        print_log(f'\nMODEL Summary: {name}')
        print_log(f'    elements: {len(self)}')
        lines = self.lines()
        print_log(f'       lines: {len(lines)}')
        circles = self.circles()
        print_log(f'     circles: {len(circles)}')
        pts = self.points()
        print_log(f'      points: {len(pts)}')


if __name__ == '__main__':
    m = Model()
    a = m.gen_point(0, 0)
    b = m.gen_point(1, 0)
    print(m)
    m.summary()
