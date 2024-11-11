import math
import random
from abc import ABC, abstractmethod
from typing import List, Set

from super_scad.d2.private.PrivatePolygon import PrivatePolygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.type.Angle import Angle


class PolygonMixin(ABC):
    """
    A mixin for all polygonal and polygonal like widgets in SuperSCAD.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 extend_sides_by_eps: bool | Set[int] | None,
                 delta: float | None):
        """
        Object constructor.

        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        self._inner_angles: List[float] | None = None
        """
        The inner angles of the polygon (in the same order as the primary points).
        """

        self._normal_angles: List[float] | None = None
        """
        The absolute angles of the normal of each node.
        """

        self._is_clockwise: bool | None = None
        """
        Whether the nodes of the polygon are in a clockwise order.
        """

        self._extend_sides_by_eps: bool | Set[int] | None = extend_sides_by_eps
        """
        Whether to extend sides by eps for a clear overlap.
        """

        self._delta: float | None = delta
        """
        The minimum distance between nodes, vertices and line segments for reliable computation of the separation
        between line segments and nodes.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_clockwise_order(nodes: List[Vector2], delta: float) -> bool:
        """
        Returns whether the nodes of a polygon are given in a clockwise order.

        @param nodes: The nodes of the polygon.
        @param delta: The minimum distance between the line segment and the nodes.
        """
        radius = 0.0
        for node in nodes:
            radius = max(radius, abs(node.x), abs(node.y))

        n = len(nodes)
        for index1 in range(10 * n):
            min_distance = radius
            for index2 in range(1, n):
                if index2 != index1 % n:
                    min_distance = min(min_distance, Vector2.distance(nodes[index1 % n], nodes[index2]))

            p1 = nodes[(index1 - 1) % n]
            p2 = nodes[index1 % n]
            p3 = nodes[(index1 + 1) % n]

            if not PolygonMixin._to_close(p1, (p3 - p1).angle, (p3 - p1).length, delta, p2):
                q1 = p2 - Vector2.from_polar_coordinates(0.5 * min_distance, ((p2 - p1).angle + (p2 - p3).angle) / 2.0)
                q2 = Vector2.from_polar_coordinates(2.0 * radius, random.uniform(0.0, 360.0))
                number_of_intersections = PolygonMixin._count_intersections(nodes, q1, q2, delta)
                if number_of_intersections is not None:
                    orientation = Vector2.orientation(p1, p2, q1)
                    assert orientation != 0.0

                    return (orientation > 0.0) == (number_of_intersections % 2 == 1)

        raise ValueError('Not a proper polygon.')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _to_close(offset: Vector2, angle: float, length: float, delta: float, node: Vector2) -> bool:
        """
        Returns whether a node is to close to a line segment for reliable computation of the separation between line
        segments and nodes.

        @param offset: The start point of the line segment.
        @param angle: The angle of the line segment.
        @param length: The length of the line segment.
        @param node: The node.
        """
        diff = (node - offset).rotate(-angle)

        return -delta <= diff.x <= (length + delta) and -delta <= diff.y <= delta

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _do_intersect(segment_start: Vector2,
                      segment_end: Vector2,
                      vertex_start: Vector2,
                      vertex_end: Vector2) -> bool:
        """
        Returns whether a line segment and a vertex intersect.

        @param segment_start: The start point of the line segment.
        @param segment_end: The end point of the line segment.
        @param vertex_start: The start point of the vertex.
        @param vertex_end:  The end point of the vertex.
        """

        o1 = Vector2.orientation(segment_start, segment_end, vertex_start)
        o2 = Vector2.orientation(segment_start, segment_end, vertex_end)
        o3 = Vector2.orientation(vertex_start, vertex_end, segment_start)
        o4 = Vector2.orientation(vertex_start, vertex_end, segment_end)

        return (math.copysign(1, o1) != math.copysign(1, o2)) and (math.copysign(1, o3) != math.copysign(1, o4))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _count_intersections(nodes: List[Vector2],
                             segment_start: Vector2,
                             segment_end: Vector2,
                             delta: float) -> int | None:
        """
        Returns the number of intersections between a line segment (segment_start, segment_end) and the vertices of the
        polygon.

        :param nodes: The nodes of the polygon.
        :param segment_start: Start point of the line segment.
        :param segment_end: End point of the line segment.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        intersections = 0

        offset = segment_start
        angle = (segment_end - segment_start).angle
        length = Vector2.distance(segment_start, segment_end)

        n = len(nodes)
        for i in range(n):
            vertex_start = nodes[i]
            vertex_end = nodes[(i + 1) % n]

            if PolygonMixin._to_close(offset, angle, length, delta, vertex_start):
                return None

            if PolygonMixin._do_intersect(segment_start, segment_end, vertex_start, vertex_end):
                intersections += 1

        return intersections

    # ------------------------------------------------------------------------------------------------------------------
    def _compute_angles(self, context: Context) -> None:
        """
        Returns the inner angles of the polygon (in the same order as the primary points).

        :param context: The build context.
        """
        self._inner_angles = []
        self._normal_angles = []

        nodes = self.nodes
        self._is_clockwise = self.is_clockwise_order(nodes, self.delta(context))

        n = len(nodes)
        for i in range(n):
            if self._is_clockwise:
                p1 = nodes[(i - 1) % n]
                p2 = nodes[i]
                p3 = nodes[(i + 1) % n]
            else:
                p1 = nodes[(i + 1) % n]
                p2 = nodes[i]
                p3 = nodes[(i - 1) % n]

            inner_angle = Angle.normalize((p3 - p2).angle - (p2 - p1).angle - 180.0)
            normal_angle = Angle.normalize((p1 - p2).angle + 0.5 * inner_angle)

            self._inner_angles.append(inner_angle)
            self._normal_angles.append(normal_angle)

    # ------------------------------------------------------------------------------------------------------------------
    def is_clockwise(self, context: Context) -> bool:
        """
        Returns whether the nodes of this polygon are in a clockwise order.

        :param context: The build context.
        """
        if self._is_clockwise is None:
            self._compute_angles(context)

        return self._is_clockwise

    # ------------------------------------------------------------------------------------------------------------------
    def inner_angles(self, context: Context) -> List[float]:
        """
        Returns the inner angles of the polygon (in the same order as the primary points).

        :param context: The build context.
        """
        if self._inner_angles is None:
            self._compute_angles(context)

        return self._inner_angles

    # ------------------------------------------------------------------------------------------------------------------
    def normal_angles(self, context: Context) -> List[float]:
        """
        Returns the absolute angles of the normal of each node.

        :param context: The build context.
        """
        if self._normal_angles is None:
            self._compute_angles(context)

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
    def delta(self, context: Context) -> float:
        """
        The minimum distance between nodes, vertices and line segments for reliable computation of the separation
        between line segments, vertices and nodes.

        :param context: The build context.
        """
        if self._delta is None:
            self._delta = 0.5 * context.resolution

        return self._delta

    # ------------------------------------------------------------------------------------------------------------------
    def extend_sides_by_eps(self) -> Set[int]:
        """
        Returns the set of sides that must be extended by eps for clear overlap.
        """
        if not self._extend_sides_by_eps:
            return set()

        if self._extend_sides_by_eps is True:
            return {index for index in range(self.sides)}

        if isinstance(self._extend_sides_by_eps, set):
            return self._extend_sides_by_eps

        raise ValueError(f'Parameter extend_sides_by_eps must be a boolean, '
                         f'set of integers or None, got {type(self._extend_sides_by_eps)}')

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
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        extend_sides_by_eps = self.extend_sides_by_eps()
        if not extend_sides_by_eps:
            return self._build_polygon(context)

        return self._build_polygon_extended(context)

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon_extended(self, context: Context):
        """
        Builds a polygon with extended sides.

        @param context: The build context.
        """
        extend_sides_by_eps = self.extend_sides_by_eps()

        nodes = self.nodes
        inner_angles = self.inner_angles(context)
        normal_angles = self.normal_angles(context)
        clockwise = self.is_clockwise(context)

        new_nodes = []
        n = len(nodes)
        for index in range(n):
            node = nodes[index]
            inner_angle = inner_angles[index]
            normal_angle = normal_angles[index]

            if inner_angle <= 180.0:
                # Outer corner.
                if index in extend_sides_by_eps:
                    # This side is extended by eps.
                    if (index - 1) % n in extend_sides_by_eps:
                        # The previous side is extended by eps, also.
                        if clockwise:
                            angle = normal_angle - 0.5 * inner_angle - 90.0
                        else:
                            angle = normal_angle + 0.5 * inner_angle + 90.0
                        new_nodes.append(node + Vector2.from_polar_coordinates(context.eps, angle))
                        new_nodes.append(
                                node + Vector2.from_polar_coordinates(context.eps, normal_angle + 180.0))
                    else:
                        # The previous side is not extended by eps.
                        new_nodes.append(node)
                    if clockwise:
                        angle = normal_angle + 0.5 * inner_angle + 90.0
                    else:
                        angle = normal_angle - 0.5 * inner_angle - 90.0
                    new_nodes.append(node + Vector2.from_polar_coordinates(context.eps, angle))
                else:
                    # This side is not extended by eps.
                    if (index - 1) % n in extend_sides_by_eps:
                        # The previous side is extended by eps.
                        if clockwise:
                            angle = normal_angle - 0.5 * inner_angle - 90.0
                        else:
                            angle = normal_angle + 0.5 * inner_angle + 90.0
                        new_nodes.append(node + Vector2.from_polar_coordinates(context.eps, angle))
                    new_nodes.append(node)
            else:
                # Inner corner.
                if index in extend_sides_by_eps:
                    # This side is extended by eps.
                    if (index - 1) % n in extend_sides_by_eps:
                        # The previous side is extended by eps, also.
                        alpha = 0.5 * (360.0 - inner_angle)
                        eps0 = Vector2.from_polar_coordinates(context.eps / math.sin(math.radians(alpha)),
                                                              normal_angle + 180.0)
                        new_nodes.append(node + eps0)
                    else:
                        # The next side is not extended by eps.
                        if clockwise:
                            angle = normal_angle - 0.5 * inner_angle
                        else:
                            angle = normal_angle + 0.5 * inner_angle
                        new_nodes.append(node + Vector2.from_polar_coordinates(context.eps, angle))
                else:
                    # This side is not extended by eps.
                    if (index - 1) % n in extend_sides_by_eps:
                        # The previous side is extended by eps.
                        if clockwise:
                            angle = normal_angle + 0.5 * inner_angle
                        else:
                            angle = normal_angle - 0.5 * inner_angle
                        new_nodes.append(node + Vector2.from_polar_coordinates(context.eps, angle))
                    else:
                        # The next side is not extended by eps, also.
                        new_nodes.append(node)

        return PrivatePolygon(points=new_nodes, convexity=self.convexity)

# ----------------------------------------------------------------------------------------------------------------------
