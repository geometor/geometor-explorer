'''Helper functions and resources for the Pappus study'''
from geometor.model import *

A = []
B = []

types = ['square', 'circle', 'diamond']


def pappus_start(A3x, B1, B2, B3x):
    pts.clear()
    elements.clear()
    history.clear()

    A = []
    A.append( add_point( point(0, 0, classes=['A', 'start', 'square']) ) )
    A.append( add_point( point(1, 0, classes=['A', 'start', 'circle']) ) )
    line_a = add_element(line(A[0], A[1], classes=['blue']) )
    A.append( add_point( point(A3x, 0, classes=['A', 'start', 'diamond']) ) )
    line_a.pts.add(A[-1])

    B = []
    B1 = add_point(B1)
    B2 = add_point(B2)
    B.append( B1 )
    B.append( B2 )

    line_b = line(B1, B2, classes=['blue']) 
    add_element(line_b)
    y_val = line_get_y(line_b, B3x)
    B.append( add_point( point(B3x, y_val, classes=['B', 'start']) ) )
    line_b.pts.add(B[-1])

    return A, B


def set_meet(u, v, A, B):
    '''join pairs of points to find the meet'''
    j1 = add_element( line(A[u], B[v], classes=['red']) )
    j2 = add_element( line(A[v], B[u], classes=['green']) )
    join_spread = spread(j1, j2)
    print(f'join {u} {v}')
    print(f'  j1: {j1.coefficients}')
    print(f'  j2: {j2.coefficients}')
    print(f'  spread: {join_spread}')
    meet = j1.intersection(j2)
    # check if parallel or conicident
    if meet and isinstance(meet[0], spg.Point2D):    
        # find meets from points list
        pt = pts[pts.index(meet[0])]
        pt.classes.append('meet')
        type = types[3 - (u + v)]
        pt.classes.append(type)
        print(f'  meet ({pt.x}, {pt.y})')

