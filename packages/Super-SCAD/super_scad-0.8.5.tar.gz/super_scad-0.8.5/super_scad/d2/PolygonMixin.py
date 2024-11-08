import random
import typing
from abc import ABC, abstractmethod
from typing import List

from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.type.Angle import Angle

Polygon = typing.NewType('Polygon', None)


class PolygonMixin(ABC):
    """
    A mixin for all polygonal and polygonal like widgets in SuperSCAD.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self._inner_angles: List[float] | None = None
        """
        The inner angles of the polygon (in the same order as the primary points).
        """

        self._normal_angles: List[float] | None = None
        """
        The absolute angles of the normal of each node.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _count_intersections(nodes: List[Vector2], p1: Vector2, q1: Vector2) -> int:
        """
        Returns the number of intersections between a line segment (p1, q1) and the vertices of the polygon.

        @param nodes: The nodes of the polygon.
        @param p1: Start point of the line segment.
        @param q1: End point of the line segment.
        """
        intersections = 0

        n = len(nodes)
        for i in range(n):
            p2 = nodes[i]
            q2 = nodes[(i + 1) % n]

            if Vector2.do_intersect(p1, q1, p2, q2):
                intersections += 1

        return intersections

    # ------------------------------------------------------------------------------------------------------------------
    def _compute_angles(self) -> None:
        """
        Returns the inner angles of the polygon (in the same order as the primary points).
        """
        self._inner_angles = []
        self._normal_angles = []

        radius: float = 0.0
        nodes = self.nodes
        for point in nodes:
            radius = max(radius, point.x, point.y)

        n = len(nodes)
        for i in range(n):
            p1 = nodes[(i - 1) % n]
            p2 = nodes[i]
            p3 = nodes[(i + 1) % n]

            q1 = Vector2((p1.x + p2.x + p3.x) / 3, (p1.y + p2.y + p3.y) / 3)
            q2 = Vector2.from_polar_coordinates(2.0 * radius, random.uniform(0.0, 360.0))

            number_of_intersections = PolygonMixin._count_intersections(nodes, q1, q2)

            inner_angle = Vector2.angle_3p(p1, p2, p3)
            if number_of_intersections % 2 == 0:
                inner_angle = 360.0 - inner_angle
            inner_angle = Angle.normalize(inner_angle)

            clockwise = Angle.normalize((p2 - q1).angle - (p1 - q1).angle) > 180.0
            if clockwise and number_of_intersections % 2 == 0:
                normal_angle = (p1 - p2).angle - 0.5 * inner_angle
            elif not clockwise and number_of_intersections % 2 == 0:
                normal_angle = (p1 - p2).angle + 0.5 * inner_angle
            elif clockwise and number_of_intersections % 2 == 1:
                normal_angle = (p1 - p2).angle + 0.5 * inner_angle
            elif not clockwise and number_of_intersections % 2 == 1:
                normal_angle = (p1 - p2).angle - 0.5 * inner_angle
            else:
                raise RuntimeError('Should not happen.')
            normal_angle = Angle.normalize(normal_angle)

            self._inner_angles.append(inner_angle)
            self._normal_angles.append(normal_angle)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_angles(self) -> List[float]:
        """
        Returns the inner angles of the polygon (in the same order as the primary points).
        """
        if self._inner_angles is None:
            self._compute_angles()

        return self._inner_angles

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def normal_angles(self) -> List[float]:
        """
        Returns the absolute angles of the normal of each node.
        """
        if self._normal_angles is None:
            self._compute_angles()

        return self._normal_angles

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this polygon.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sides(self) -> int:
        """
        Returns the number of sides of this polygon.
        """
        return len(self.nodes)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the convexity of this polygon.
        """
        return None

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
