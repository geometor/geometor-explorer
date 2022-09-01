"""
Model module
============

"""

import sympy as sp
import sympy.plotting as spp
import sympy.geometry as spg
import logging
from collections import defaultdict

class Model(list):

    """Docstring for Model. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__(self)
        self.parents = defaultdict(set)
        self.classes = defaultdict(set)
        

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
        '''add point to pts list - check if exists first'''
        logging.info(f'* add_point: {pt}')
        if isinstance(pt, spg.Point):
            # make new point with simplified values 
            x = sp.sqrtdenest(pt.x.simplify())
            y = sp.sqrtdenest(pt.y.simplify())
            pt = spg.Point(x, y)
            if pt in self.points():
                # add attributes
                self.parents[pt].add(parents)
                self.classes[pt].add(classes)
                return pt
                
            else:
                
                for prev_pt in self.points():
                    if pt.equals(prev_pt):
                        i = pts.index(prev_pt)
                        logging.info(f'  ! {pt} found at index: {i}')
                        # merge parents of points
                        if hasattr(pt, 'elements'):
                            if hasattr(prev_pt, 'elements'):
                                prev_pt.elements.update(pt.elements)
                        return prev_pt
            #  else:
                #  pts.append(pt)
                #  history.append(pt)
                #  logging.info(f'  + {pt}')
                #  return pt
        else:
            logging.info('    not a point')


if __name__ == '__main__':
    m = Model()
    m.gen_point(0, 0)
    print(m)
