from typing import List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.d2.private.PrivateSquare import PrivateSquare
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2


class Square(PolygonMixin, ScadWidget):
    """
    Widget for creating squares.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: float,
                 center: bool = False,
                 extend_sides_by_eps: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param size: The size of the square.
        :param center: Whether the square is centered at the origin.
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
        admission.validate_required({'size'}, {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> float:
        """
        Returns the size of this square.
        """
        return self.uc(self._args['size'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether this square is centered at its position.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sides(self) -> int:
        """
        Returns the number of sides of this square.
        """
        return 4

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this rectangle.
        """
        if self.center:
            return [Vector2(-0.5 * self.size, -0.5 * self.size),
                    Vector2(-0.5 * self.size, 0.5 * self.size),
                    Vector2(0.5 * self.size, 0.5 * self.size),
                    Vector2(0.5 * self.size, -0.5 * self.size)]

        return [Vector2.origin,
                Vector2(0.0, self.size),
                Vector2(self.size, self.size),
                Vector2(self.size, 0.0)]

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return PrivateSquare(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
