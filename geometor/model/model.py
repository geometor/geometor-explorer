"""
Model class
===========


"""

from .common import *

class Model(list):

    """Docstring for Model. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__(self)
        self.parents = defaultdict(set)
        self.classes = defaultdict(list)


    def set_point(self, x_val, y_val, parents=set(), classes=[]) -> spg.Point:
        '''generate a sympy.geometry.Point'''
        print(f'set_point:')
        print(f'    {x_val=}')
        print(f'    {y_val=}')
        print(f'    {parents=}')
        print(f'    {classes=}')
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
            print(f'    add_point: {pt}')
            return pt
        else:
            logging.info('    not a point')


    def construct_line(self, pt1: spg.Point, pt2: spg.Point, classes=[]) -> spg.Line:
        """
        create `spg.Line` object
        add `add_line`
        """
        print(f'construct_line: ')
        print(f'    {pt_1=}')
        print(f'    {pt_2=}')
        print(f'    {classes=}')
        struct = spg.Line(pt1, pt2)
        return self.add_line(struct, classes)


    def add_line(self, struct: spg.Line, classes=[]) -> spg.Line:
        '''
        Add ``line`` to list.
        check for duplicates in elements.
        find intersection points for new element with all precedng elements
        TODO: return new points from intersections
        '''
        # check if struct is in the element list
        if isinstance(struct, spg.Line):
            # check by reference
            if struct in self.lines():
                print_log('struct exists')
                self.parents[struct].update(struct.points)
                self.classes[struct].extend(classes)
                return struct
            else:
                # double check by value
                for prev in self.lines():
                    #TODO: refine test of elements
                    diff = (prev.equation().simplify() - struct.equation().simplify()).simplify()
                    #  logging.info(f'    > diff: {diff}')
                    if not diff:
                        logging.info(f'''
                    ! COINCIDENT
                        {el}
                        {prev}
                        ''')
                        self.parents[prev].update(struct.points)
                        self.classes[prev].extend(classes)
                        return prev

                # add struct
                self.append(struct)
                print(f'    add_struct: {struct}')
                self.parents[struct].update(struct.points)
                self.classes[struct].extend(classes)

                # check intersections
                for prev in self.structs():
                    if not struct.equals(prev):
                        results = struct.intersection(prev)
                        for pt in results:
                            self.add_point(pt, parents={prev, struct})
                            self.parents[prev].update({pt})
                            self.parents[struct].update({pt})
                return struct
        else:
            print_log('not a line')


    def construct_circle(self, center_pt: spg.Point, radius_pt: spg.Point, classes=[]) -> spg.Circle:
        """
        create line object from points
        add_circle
        """
        print(f'construct_circle: ')
        print(f'    {center_pt=}')
        print(f'    {radius_pt=}')
        print(f'    {classes=}')
        radius_len = center_pt.distance(radius_pt)
        print(f'    {radius_len=}')
        struct = spg.Circle(center_pt, radius_len)
        struct.radius_pt = radius_pt
        return self.add_circle(struct, classes)


    def add_circle(self, struct: spg.Circle, classes={}) -> spg.Circle:
        """
        add circle to model
        """
        # check if struct is in the element list
        if isinstance(struct, spg.Circle):
            # check by reference
            if struct in self.circles():
                print_log('struct exists')
                self.parents[struct].update({struct.center, struct.radius_pt})
                self.classes[struct].extend(classes)
                return struct
            else:
                # double check by value
                for prev in self.circles():
                    # TODO: refine test of elements
                    diff = (prev.equation().simplify() - struct.equation().simplify()).simplify()
                    #  logging.info(f'    > diff: {diff}')
                    if not diff:
                        self.parents[prev].update({struct.center, struct.radius_pt})
                        self.classes[prev].extend(classes)
                        return prev

                # add struct
                self.append(struct)
                print(f'    add_struct: {struct}')
                self.parents[struct].update({struct.center, struct.radius_pt})
                self.classes[struct].extend(classes)
                # check intersections
                for prev in self.structs():
                    if not struct.equals(prev):
                        results = struct.intersection(prev)
                        for pt in results:
                            self.add_point(pt, parents={prev, struct})
                            self.parents[prev].update({pt})
                            self.parents[struct].update({pt})
                return struct
        else:
            print_log('not a circle')


    def set_polygon(self, poly_pts, classes=[], style={}):
        '''- takes array of points - make sympy.geometry.Polygon, Triangle or Segment'''
        el = spg.Polygon(*poly_pts)
        return self.add_polygon(el, classes=classes)


    def add_polygon(self, poly: spg.Polygon, classes=[]) -> spg.Polygon:
        '''
        Add ``line`` to list.
        check for duplicates in elements.
        find intersection points for new element with all precedng elements
        TODO: return new points from intersections
        '''
        # add struct
        self.append(poly)
        self.parents[poly].update(poly.vertices)
        self.classes[poly].extend(classes)

        return poly

    def set_segment(self, pt_1, pt_2, classes=[], style={}):
        '''- takes 2 points - make sympy.geometry.Segment'''
        el = spg.Segment(pt_1, pt_2)
        return self.add_segment(el, classes=classes)


    def add_segment(self, seg: spg.Segment, classes=[]) -> spg.Segment:
        '''
        Add ``line`` to list.
        check for duplicates in elements.
        find intersection points for new element with all precedng elements
        TODO: return new points from intersections
        '''
        # add struct
        self.append(seg)
        self.parents[seg].update(seg.vertices)
        self.classes[seg].extend(classes)

        return seg

    # Lists
    def points(self) -> list:
        """filter points from model
        :returns: list

        """
        return [el for el in self if isinstance(el, spg.Point)]


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
        """
        filtered list of circles
        """
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


    def limits(self, margin=0.1):
        '''\
        find x, y limits from points and circles of the model
        returns a list of lists of x, y limits'''
        limx = [0, 0]
        limy = [0, 0]
        for el in self:
            if isinstance(el, spg.Point):
                ptx = float(el.x.evalf())
                pty = float(el.y.evalf())
                limx[0] = ptx if ptx < limx[0] else limx[0]
                limx[1] = ptx if ptx > limx[1] else limx[1]
                limy[0] = pty if pty < limy[0] else limy[0]
                limy[1] = pty if pty > limy[1] else limy[1]

            if isinstance(el, spg.Circle):
                xmin, ymin, xmax, ymax = el.bounds
                xmin = float(xmin.evalf())
                ymin = float(ymin.evalf())
                xmax = float(xmax.evalf())
                ymax = float(ymax.evalf())
                limx[0] = xmin if xmin < limx[0] else limx[0]
                limx[1] = xmax if xmax > limx[1] else limx[1]
                limy[0] = ymin if ymin < limy[0] else limy[0]
                limy[1] = ymax if ymax > limy[1] else limy[1]

        #  w = limx[1] - limx[0]
        #  h = limy[1] - limy[0]
        #  if w > h

        #  # TODO: change margin to percentage
        #  limx[0] -= margin
        #  limx[1] += margin
        #  limy[0] -= margin
        #  limy[1] += margin

        return [limx, limy]


if __name__ == '__main__':
    m = Model()
    a = m.set_point(0, 0)
    b = m.set_point(1, 0)
    m.construct_line(a, b)
    m.construct_circle(a, b)
    m.construct_circle(b, a)
    print(m)
    m.summary()
