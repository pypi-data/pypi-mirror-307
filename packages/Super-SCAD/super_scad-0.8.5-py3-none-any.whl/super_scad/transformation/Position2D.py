from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Rotate2D import Rotate2D
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type import Vector2
from super_scad.type.Angle import Angle


class Position2D(ScadSingleChildParent):
    """
    A convenience widget that first rotates its child about the z-axis and then translates its child widget along the
    specified vector.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | None = None,
                 vector: Vector2 | None = None,
                 x: float | None = None,
                 y: float | None = None,
                 child: ScadWidget):
        """
        Object constructor.

        :param angle: The angle of rotation (around the z-axis).
        :param vector: The vector over which the child widget is translated.
        :param x: The distance the child widget is translated to along the x-axis.
        :param y: The distance the child widget is translated to along the y-axis.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'vector'}, {'x', 'y'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of rotation (around the z-axis).
        """
        return Angle.normalize(self._args.get('angle', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vector(self) -> Vector2:
        """
        Returns the vector over which the child widget is translated.
        """
        if 'vector' in self._args:
            return self.uc(self._args['vector'])

        return Vector2(self.x, self.y)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def x(self) -> float:
        """
        Returns distance the child widget is translated to along the x-axis.
        """
        if 'vector' in self._args:
            return self.uc(self._args['vector'].x)

        return self.uc(self._args.get('x', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def y(self) -> float:
        """
        Returns distance the child widget is translated to along the y-axis.
        """
        if 'vector' in self._args:
            return self.uc(self._args['vector'].y)

        return self.uc(self._args.get('y', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        child = self.child

        if self.angle != 0.0:
            child = Rotate2D(angle=self.angle, child=child)

        if self.vector.is_not_origin:
            child = Translate2D(vector=self.vector, child=child)

        return child

# ----------------------------------------------------------------------------------------------------------------------
