"""The `geometor.core.construction` module defines the `Construction` class, which represents a geometric construction.

Example usage:
    # Create a new `Construction` object
    construction = Construction()

    # Add a new point to the construction
    point = construction.add_point(x=0, y=0)

    # Add a new line to the construction
    line = construction.add_line(start=Point(x=0, y=0), end=Point(x=1, y=1))

    # Add a new circle to the construction
    circle = construction.add_circle(center=Point(x=0, y=0), radius=1)

    # Render the construction using matplotlib
    construction.render()
"""

from typing import List

from geometor.explorer.core.element import Element
from geometor.explorer.core.point import Point
from geometor.explorer.core.line import Line
from geometor.explorer.core.circle import Circle


class Construction:
    """The `Construction` class represents a geometric construction.

    This class stores a collection of `Element` objects, which represent the geometric elements of the construction.

    Attributes:
        elements (`List[geometor.core.element.Element]`): A list of `Element` objects in the construction.
    """

    def __init__(self, elements: List[Element] = None):
        """Initializes a new `Construction` object with an optional list of `Element` objects."""
        self.elements = elements or []

    def add_point(self, x: float, y: float) -> Point:
        """Adds a new `Point` object to the construction with the specified coordinates and returns the point."""
        point = Point(x=x, y=y)
        self.elements.append(point)
        return point

    def add_line(self, start: Point, end: Point) -> Line:
        """Adds a new `Line` object to the construction with the specified start and end points and returns the line."""
        line = Line(start=start, end=end)
        self.elements.append(line)
        return line

    def add_circle(self, center: Point, radius: float) -> Circle:
        """Adds a new `Circle` object to the construction with the specified center point and radius and returns the circle."""
        circle = Circle(center=center, radius=radius)
        self.elements.append(circle)
        return circle

    def render(self):
        """Renders the construction using matplotlib."""
        pass  # Placeholder for rendering logic
