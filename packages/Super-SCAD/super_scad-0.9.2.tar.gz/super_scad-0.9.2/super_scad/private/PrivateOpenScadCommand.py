import re
from typing import Any, Dict, List, Set, Tuple

from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Color import Color
from super_scad.type.Vector2 import Vector2
from super_scad.type.Vector3 import Vector3


class PrivateOpenScadCommand(ScadWidget):
    """
    Widget for creating OpenSCAD commands.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, command: str, args: Dict[str, Any]):
        """
        Object constructor.

        :param command: The name of the OpenSCAD command.
        :param args: The arguments of the OpenSCAD command.
        """
        ScadWidget.__init__(self, args=args)

        self._command: str = command
        """
        The name of the OpenSCAD command.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return self

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def command(self) -> str:
        """
        Returns the name of the OpenSCAD command.
        """
        return self._command

    # ------------------------------------------------------------------------------------------------------------------
    def generate_args(self, context: Context) -> str:
        """
        Returns the arguments of the OpenSCAD command.
        """
        argument_map = self._argument_map()
        argument_angles = self._argument_angles()
        argument_lengths = self._argument_lengths()
        argument_scales = self._argument_scales()

        args_as_str = '('
        first = True
        for key, value in self._args.items():
            if not first:
                args_as_str += ', '
            else:
                first = False

            real_name = argument_map.get(key, key)
            if real_name in argument_angles:
                real_value = self.__format_argument(context, value, True, False, False)
            elif real_name in argument_lengths:
                real_value = self.__format_argument(context, self.uc(value), False, True, False)
            elif real_name in argument_scales:
                real_value = self.__format_argument(context, value, False, False, True)
            else:
                real_value = self.__format_argument(context, value, False, False, False)

            if real_name is None:
                args_as_str += '{}'.format(real_value)
            else:
                args_as_str += '{} = {}'.format(real_name, real_value)
        args_as_str += ')'

        return args_as_str

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_map(self) -> Dict[str, str | None]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {}

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_angles(self) -> Set[str]:
        """
        Returns the set with arguments that are angles.
        """
        return set()

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return set()

    # ------------------------------------------------------------------------------------------------------------------
    def _argument_scales(self) -> Set[str]:
        """
        Returns the set with arguments that are scales and factors.
        """
        return set()

    # ------------------------------------------------------------------------------------------------------------------
    def __format_argument(self,
                          context: Context,
                          argument: Any,
                          is_angle: bool,
                          is_length: bool,
                          is_scale: bool) -> str:
        """
        Returns an argument of the OpenSCAD command.

        :param context: The build context.
        :param argument: The argument of OpenSCAD command.
        """
        if isinstance(argument, float):
            if is_length:
                argument = context.round_length(argument)
            elif is_angle:
                argument = context.round_angle(argument)
            elif is_scale:
                argument = context.round_scale(argument)
            if argument == '-0.0':
                argument = '0.0'

            return argument

        if isinstance(argument, Vector2):
            return "[{}, {}]".format(self.__format_argument(context, float(argument.x), is_angle, is_length, is_scale),
                                     self.__format_argument(context, float(argument.y), is_angle, is_length, is_scale))

        if isinstance(argument, Vector3):
            return "[{}, {}, {}]".format(
                    self.__format_argument(context, float(argument.x), is_angle, is_length, is_scale),
                    self.__format_argument(context, float(argument.y), is_angle, is_length, is_scale),
                    self.__format_argument(context, float(argument.z), is_angle, is_length, is_scale))

        if isinstance(argument, bool):
            return str(argument).lower()

        if isinstance(argument, str):
            return '"{}"'.format(re.sub(r'([\\\"])', r'\\\1', argument))

        if isinstance(argument, int):
            return str(argument)

        if isinstance(argument, List) or isinstance(argument, Tuple):
            parts = [self.__format_argument(context, element, is_angle, is_length, is_scale) for element in argument]

            return '[{}]'.format(', '.join(parts))

        if isinstance(argument, Color):
            return str(argument)

        raise ValueError(f'Can not format argument of type {argument.__class__}.')

# ----------------------------------------------------------------------------------------------------------------------
