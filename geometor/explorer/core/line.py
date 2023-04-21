"""The `geometor.explorer.core.line` module defines the `Line` class, which represents a line segment in 2D space."""
from geometor.explorer.core.element import Element
from geometor.explorer.core.point import Point


class Line(Element):
    """The `Line` class represents a line segment in 2D space."""

    def __init__(self, start: Point, end: Point):
        """Initializes a new `Line` object with the specified start and end points."""
        self.start = start
        self.end = end
