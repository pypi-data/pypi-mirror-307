import math
import typing
from dataclasses import dataclass

Vector2 = typing.NewType('Vector2', None)


@dataclass(frozen=True)
class Vector2:
    """
    A coordinate in 2D space.
    """

    # ------------------------------------------------------------------------------------------------------------------
    x: float
    """
    The x-coordinate of this point.
    """

    y: float
    """
    The y-coordinate of this point.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    # ------------------------------------------------------------------------------------------------------------------
    def __add__(self, other: Vector2):
        return Vector2(self.x + other.x, self.y + other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other: Vector2):
        return Vector2(self.x - other.x, self.y - other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, other: float):
        return Vector2(self.x / other, self.y / other)

    # ------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other: float):
        return Vector2(self.x * other, self.y * other)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def from_polar_coordinates(length: float, angle: float) -> Vector2:
        """
        Creates a 2-dimensional vector from polar coordinates.

        @param length: The length of the vector.
        @param angle: The angle of the vector.
        """
        return Vector2(length * math.cos(math.radians(angle)), length * math.sin(math.radians(angle)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of this vector.
        """
        return math.degrees(math.atan2(self.y, self.x))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_origin(self) -> bool:
        """
        Returns whether this vector is the origin.
        """
        return self.x == 0.0 and self.y == 0.0

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_not_origin(self) -> bool:
        """
        Returns whether this vector is not the origin.
        """
        return self.x != 0.0 or self.y != 0.0

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> float:
        """
        Returns the length of this vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def normal(self) -> Vector2:
        """
        Returns the unit vector of this vector.
        """
        length = self.length

        return Vector2(self.x / length, self.y / length)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _on_segment(p: Vector2, q: Vector2, r: Vector2) -> bool:
        """
        Given three collinear points p, q, r, returns whether point q lies on the line segment (p, r).

        @param p: Point p.
        @param q: Point q.
        @param r: Point r.
        """
        if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
                (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _orientation(p: Vector2, q: Vector2, r: Vector2) -> int:
        """
        Returns the orientation of an ordered triplet (p, q, r).
        * 0 : Collinear points
        * 1 : Clockwise points
        * 2 : Counterclockwise

        @param p: Point p.
        @param q: Point q.
        @param r: Point r.
        """
        val = ((q.y - p.y) * (r.x - q.x)) - ((q.x - p.x) * (r.y - q.y))
        if val > 0:
            return 1

        elif val < 0:
            return 2

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def do_intersect(p1: Vector2, q1: Vector2, p2: Vector2, q2: Vector2) -> bool:
        """
        Returns whether line segments (p1, q1) and (p1, q2) intersect.

        @see https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/ for some background information.

        @param p1: The start point of the first segment.
        @param q1: The end point of the first segment.
        @param p2: The start point of the second segment.
        @param q2: The end point of the second segment.
        """
        o1 = Vector2._orientation(p1, q1, p2)
        o2 = Vector2._orientation(p1, q1, q2)
        o3 = Vector2._orientation(p2, q2, p1)
        o4 = Vector2._orientation(p2, q2, q1)

        if (o1 != o2) and (o3 != o4):
            return True

        if (o1 == 0) and Vector2._on_segment(p1, p2, q1):
            return True

        if (o2 == 0) and Vector2._on_segment(p1, q2, q1):
            return True

        if (o3 == 0) and Vector2._on_segment(p2, p1, q2):
            return True

        if (o4 == 0) and Vector2._on_segment(p2, q1, q2):
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def angle_3p(p: Vector2, q: Vector2, r: Vector2) -> float:
        """
        Returns the angle between line segments (p, q) and (r, q).

        @param p: Point p.
        @param q: Point q
        @param r: Point r.
        """
        return math.degrees(math.acos(((q - p).length ** 2 +
                                       (q - r).length ** 2 -
                                       (p - r).length ** 2) / (2 * (q - p).length * (q - r).length)))


# ----------------------------------------------------------------------------------------------------------------------
