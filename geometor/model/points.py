"""
points module
=============
"""

from .common import *

# structural elements
def point(x_val, y_val, classes=[]):
    '''make sympy.geometry.Point'''
    pt = spg.Point(sp.simplify(x_val), sp.simplify(y_val))
    # TODO: put classes elsewhere
    pt.classes = classes
    return pt

        
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


def sort_points(pts):
    return sorted(list(pts), key=point_value)


def get_pts_by_class(pts, classname):
    '''find all points with specified classname'''
    pts_by_class = []
    for pt in pts:
        if pt.classes.count(classname):
            pts_by_class.append(pt)
    return pts_by_class


#  def find_pt_index(pts, pt):
    #  if isinstance(pt, spg.Point2D):
        #  for i, prev_pt in enumerate(pts):
            #  if pt.equals(prev_pt):
                #  #  i = pts.index(prev_pt)
                #  print_log(f'  ! {pt} found at index: {i}')
                #  return i
    #  else:
        #  return -1
    

#  def add_point(pt):
    #  '''add point to pts list - check if exists first'''
    #  logging.info(f'* add_point: {pt}')
    #  if isinstance(pt, spg.Point2D):
        #  # make new point with simplified values 
        #  x = sp.sqrtdenest(pt.x.simplify())
        #  y = sp.sqrtdenest(pt.y.simplify())
        #  pt = point(x, y, classes=pt.classes)
        #  for prev_pt in pts:
            #  if pt.equals(prev_pt):
                #  i = pts.index(prev_pt)
                #  logging.info(f'  ! {pt} found at index: {i}')
                #  # merge parents of points
                #  if hasattr(pt, 'elements'):
                    #  if hasattr(prev_pt, 'elements'):
                        #  prev_pt.elements.update(pt.elements)
                #  return prev_pt
        #  else:
            #  pts.append(pt)
            #  history.append(pt)
            #  logging.info(f'  + {pt}')
            #  return pt
    #  else:
        #  logging.info('    not a point')


#  def add_points(pt_array):
    #  '''add an array of points to pts list'''
    #  for pt in pt_array:
        #  add_point(pt)


