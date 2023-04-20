"""
This module provides the `Model` class, which is used to represent a geometric model
in 2D space. The `Model` class is based on the `list` data structure, and can contain
points, lines, circles, polygons, and segments.

"""

import sympy as sp
import sympy.geometry as spg

sp.init_printing()

from collections import defaultdict
from multiprocessing import Pool, cpu_count
from rich import print

from geometor.utils import *


class Model(list):

    """
    A collection of geometric elements, including points, lines, circles, and polygons,
    represented using the `sympy.geometry` library.

    When lines and circles are added to the model, intersection points of the new element with the preceding elements are identify and added.

    When new elements or points are added to the model, we check for exisitng duplicates.

    Construction method prefixes:
    - `set_`: creates a new point or object, replacing any existing object with the same coordinates.
    - `add_`: adds an object to the collection, or updates the attributes of an existing object with the same coordinates.
    - `construct_`: creates a new object based on existing points, and adds it to the collection.

    Attributes:
    - `parents`: a dictionary mapping each object in the collection to its parent objects, if any.
    - `classes`: a dictionary mapping each object in the collection to a list of its classes, if any.
    - `labels`: a dictionary mapping each object in the collection to its label, if any.

    Collection Methods:
    - `points()`: returns a list of all points in the collection.
    - `lines()`: returns a list of all lines in the collection.
    - `circles()`: returns a list of all circles in the collection.
    - `structs()`: returns a list of all lines and circles in the collection.
    - `summary()`: prints a summary of the collection, including the number of elements of each type.
    - `limits()`: returns the x and y limits of the model, based on the coordinates of its elements.
    """

    def __init__(self):
        """TODO: to be defined."""
        super().__init__(self)
        self.parents = defaultdict(dict)
        self.classes = defaultdict(list)
        self.labels = defaultdict(str)

    def set_point(self, x_val, y_val, parents={}, classes=[], label="") -> spg.Point:
        """generate a sympy.geometry.Point"""
        print(f"set_point:")
        print(f"    {x_val=}")
        print(f"    {y_val=}")
        print(f"    {parents=}")
        print(f"    {classes=}")
        print(f"    {label=}")
        x_val = sp.simplify(x_val)
        y_val = sp.simplify(y_val)
        pt = spg.Point(x_val, y_val)
        return self.add_point(pt, parents, classes, label)

    def add_point(self, pt: spg.Point, parents={}, classes=[], label="") -> spg.Point:
        """add point to model
        find duplicates
        clean values
        set parents and classes"""
        if isinstance(pt, spg.Point):
            # make new point with simplified values
            x = sp.sqrtdenest(pt.x.simplify())
            y = sp.sqrtdenest(pt.y.simplify())
            pt = spg.Point(x, y)
            if pt in self.points():
                # add attributes
                for parent in parents:
                    self.parents[pt][parent] = ""
                self.classes[pt].extend(classes)
                #  self.labels[pt] = label
                return pt

            else:
                for prev_pt in self.points():
                    if pt.equals(prev_pt):
                        for parent in parents:
                            self.parents[prev_pt][parent] = ""
                        self.classes[prev_pt].extend(classes)
                        #  self.labels[prev_pt] = label
                        return prev_pt

            self.append(pt)
            for parent in parents:
                self.parents[pt][parent] = ""
            self.classes[pt].extend(classes)
            self.labels[pt] = label

            print(f"    add_point: {pt}")
            return pt
        else:
            print(f"    NOT a point: {pt}")

    def construct_line(
        self, pt_1: spg.Point, pt_2: spg.Point, classes=[], label=""
    ) -> spg.Line:
        """
        create `spg.Line` object
        add `add_line`
        """
        print(f"construct_line: ")
        print(f"    {pt_1=}")
        print(f"    {pt_2=}")
        print(f"    {classes=}")
        print(f"    {label=}")
        struct = spg.Line(pt_1, pt_2)
        return self.add_line(struct, classes, label)

    def add_line(self, struct: spg.Line, classes=[], label="") -> spg.Line:
        """
        Add ``line`` to list.
        check for duplicates in elements.
        find intersection points for new element with all precedng elements
        TODO: return new points from intersections
        """
        # check if struct is in the element list
        if isinstance(struct, spg.Line):
            # check by reference
            if struct in self.lines():
                print_log("struct exists")
                for parent in struct.points:
                    self.parents[struct][parent] = ""
                self.classes[struct].extend(classes)
                return struct
            else:
                # double check by value
                for prev in self.lines():
                    # TODO: refine test of elements
                    diff = (
                        prev.equation().simplify() - struct.equation().simplify()
                    ).simplify()
                    if not diff:
                        print_log(
                            f"""
                    ! COINCIDENT
                        {el}
                        {prev}
                        """
                        )
                        for parent in struct.points:
                            self.parents[prev][parent] = ""
                        self.classes[prev].extend(classes)
                        return prev

                # add struct
                self.append(struct)
                print_log(f"    add_struct: {struct}")
                for parent in struct.points:
                    self.parents[struct][parent] = ""
                self.classes[struct].extend(classes)
                self.labels[struct] = label

                # check intersections
                for prev in self.structs():
                    if not struct.equals(prev):
                        results = struct.intersection(prev)
                        for pt in results:
                            self.add_point(pt, parents={prev: "", struct: ""})
                            self.parents[prev][pt] = ""
                            self.parents[struct][pt] = ""
                return struct
        else:
            print_log("not a line")

    def construct_circle(
        self, center_pt: spg.Point, radius_pt: spg.Point, classes=[], label=""
    ) -> spg.Circle:
        """
        create line object from points
        add_circle
        """
        print(f"construct_circle: ")
        print(f"    {center_pt=}")
        print(f"    {radius_pt=}")
        print(f"    {classes=}")
        radius_len = center_pt.distance(radius_pt)
        print(f"    {radius_len=}")
        print(f"    {label=}")
        struct = spg.Circle(center_pt, radius_len)
        struct.radius_pt = radius_pt
        return self.add_circle(struct, classes, label)

    def add_circle(self, struct: spg.Circle, classes=[], label="") -> spg.Circle:
        """
        add circle to model
        """
        # check if struct is in the element list
        if isinstance(struct, spg.Circle):
            # check by reference
            if struct in self.circles():
                print_log("struct exists")
                self.parents[struct][struct.center] = ""
                self.parents[struct][struct.radius_pt] = ""
                self.classes[struct].extend(classes)
                return struct
            else:
                # double check by value
                for prev in self.circles():
                    # TODO: refine test of elements
                    diff = (
                        prev.equation().simplify() - struct.equation().simplify()
                    ).simplify()
                    print_log(f"    > diff: {diff}")
                    if not diff:
                        self.parents[prev][struct.center] = ""
                        self.parents[prev][struct.radius_pt] = ""
                        self.classes[prev].extend(classes)
                        return prev

                # add struct
                self.append(struct)
                print(f"    add_struct: {struct}")
                self.parents[struct][struct.center] = ""
                self.parents[struct][struct.radius_pt] = ""
                self.classes[struct].extend(classes)
                self.labels[struct] = label

                # check intersections
                for prev in self.structs():
                    if not struct.equals(prev):
                        results = struct.intersection(prev)
                        for pt in results:
                            self.add_point(pt, parents={prev: "", struct: ""})
                            self.parents[prev][pt] = ""
                            self.parents[struct][pt] = ""
                return struct
        else:
            print_log("not a circle")

    def set_polygon(self, poly_pts, classes=[], label=""):
        """- takes array of points - make sympy.geometry.Polygon, Triangle or Segment"""
        el = spg.Polygon(*poly_pts)
        print(f"set_polygon: ")
        print(f"    {poly_pts=}")
        print(f"    {classes=}")
        print(f"    {label=}")
        return self.add_polygon(el, classes, label)

    def add_polygon(self, poly: spg.Polygon, classes=[], label="") -> spg.Polygon:
        """
        Add ``line`` to list.
        check for duplicates in elements.
        find intersection points for new element with all precedng elements
        TODO: return new points from intersections
        """
        # add struct
        self.append(poly)
        for parent in poly.vertices:
            self.parents[poly][parent] = ""
        self.classes[poly].extend(classes)
        self.labels[poly] = label

        return poly

    def set_segment(self, pt_1, pt_2, classes=[], label=""):
        """- takes 2 points - make sympy.geometry.Segment"""
        el = spg.Segment(pt_1, pt_2)
        print(f"set_segment: ")
        print(f"    {pt_1=}")
        print(f"    {pt_2=}")
        print(f"    {classes=}")
        print(f"    {label=}")
        return self.add_segment(el, classes, label)

    def add_segment(self, seg: spg.Segment, classes=[], label="") -> spg.Segment:
        """
        Add ``line`` to list.
        check for duplicates in elements.
        find intersection points for new element with all precedng elements
        TODO: return new points from intersections
        """
        # add struct
        self.append(seg)
        for parent in seg.points:
            self.parents[seg][parent] = ""
        self.classes[seg].extend(classes)
        self.labels[seg] = label

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
        structs = []
        temp = [
            el for el in self if isinstance(el, spg.Line) or isinstance(el, spg.Circle)
        ]
        for el in temp:
            if "guide" not in self.classes[el]:
                structs.append(el)

        return structs

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

    def summary(self, name=""):
        print_log(f"\nMODEL Summary: {name}")
        print_log(f"    elements: {len(self)}")
        lines = self.lines()
        print_log(f"       lines: {len(lines)}")
        circles = self.circles()
        print_log(f"     circles: {len(circles)}")
        pts = self.points()
        print_log(f"      points: {len(pts)}")

    def limits(self, margin=0.1):
        """\
        find x, y limits from points and circles of the model
        returns a list of lists of x, y limits"""
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


if __name__ == "__main__":
    m = Model()
    a = m.set_point(0, 0)
    b = m.set_point(1, 0)
    m.construct_line(a, b)
    m.construct_circle(a, b)
    m.construct_circle(b, a)
    print(m)
    m.summary()
