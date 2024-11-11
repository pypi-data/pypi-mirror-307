from typing import List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.d2.private.PrivateSquare import PrivateSquare
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2


class Rectangle(PolygonMixin, ScadWidget):
    """
    Widget for creating rectangles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Vector2 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 extend_sides_by_eps: bool | Set[int] | None = None):
        """
        Object constructor.

        :param size: The size of the rectangle.
        :param width: The width (the size along the x-axis) of the rectangle.
        :param depth: The depth (the size along the y-axis) of the rectangle.
        :param center: Whether the rectangle is centered at its position.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        """
        PolygonMixin.__init__(self, extend_sides_by_eps=extend_sides_by_eps, delta=None)
        ScadWidget.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'size'}, {'width', 'depth'})
        admission.validate_required({'width', 'size'},
                                    {'depth', 'size'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> Vector2:
        """
        Returns the size of this rectangle.
        """
        return Vector2(x=self.width, y=self.depth)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """
        Returns the width (the size along the x-axis) of this rectangle.
        """
        if 'size' in self._args:
            return self.uc(self._args['size'].x)

        return self.uc(self._args['width'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth (the size along the y-axis) of this rectangle.
        """
        if 'size' in self._args:
            return self.uc(self._args['size'].y)

        return self.uc(self._args['depth'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the rectangle is centered at this origin.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sides(self) -> int:
        """
        Returns the number of sides of this rectangle.
        """
        return 4

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this rectangle.
        """
        if self.center:
            return [Vector2(-0.5 * self.width, -0.5 * self.depth),
                    Vector2(-0.5 * self.width, 0.5 * self.depth),
                    Vector2(0.5 * self.width, 0.5 * self.depth),
                    Vector2(0.5 * self.width, -0.5 * self.depth)]

        return [Vector2.origin,
                Vector2(0.0, self.depth),
                Vector2(self.width, self.depth),
                Vector2(self.width, 0.0)]

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateSquare(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
