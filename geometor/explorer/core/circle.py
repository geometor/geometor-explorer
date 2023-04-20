"""The `geometor.explorer.core.circle` module defines the `Circle` class, which represents a circle in 2D space."""
from geometor.explorer.core.element import Element
from geometor.explorer.core.point import Point


class Circle(Element):
    """The `Circle` class represents a circle in 2D space."""

    def __init__(self, center: Point, radius: float):
        """Initializes a new `Circle` object with the specified center point and radius."""
        self.center = center
        self.radius = radius
