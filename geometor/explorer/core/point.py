"""The `geometor.explorer.core.point` module defines the `Point` class, which
represents a point in 2D space."""
from geometor.explorer.core.element import Element


class Point(Element):
    """The `Point` class represents a point in 2D space."""

    def __init__(self, x: float, y: float):
        """Initializes a new `Point` object with the specified coordinates."""
        self.x = x
        self.y = y
