import math
from typing import List, Set

from super_scad.d2.Polygon import Polygon
from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.scad.Unit import Unit
from super_scad.type.Angle import Angle
from super_scad.type.Vector2 import Vector2


class RegularPolygon(ScadWidget, PolygonMixin):
    """
    Widget for creating regular polygons.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 sides: int,
                 outer_radius: float | None = None,
                 outer_diameter: float | None = None,
                 inner_radius: float | None = None,
                 inner_diameter: float | None = None,
                 side_length: float | None = None,
                 extend_sides_by_eps: bool | Set[int] | None = None,
                 delta: float | None = None):
        """
        Object constructor.

        :param sides: The number of sides of the regular polygon.
        :param outer_radius: The outer radius (a.k.a. circumradius) of the regular polygon.
        :param inner_radius: The inner radius (a.k.a. apothem) of the regular polygon.
        :param side_length: The length of a side of the regular polygon.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        ScadWidget.__init__(self, args=locals())
        PolygonMixin.__init__(self, extend_sides_by_eps=extend_sides_by_eps, delta=delta)

        self._angles: List[float] = []
        """
        The angles of the nodes regular polygon.
        """

        self._nodes: List[Vector2] = []
        """
        The nodes of the regular polygon.
        """

        self._unit: Unit | None = None
        """
        The unit in which self.__points are calculated.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'side_length'},
                                     {'outer_radius'},
                                     {'outer_diameter'},
                                     {'inner_radius'},
                                     {'inner_diameter'})
        admission.validate_required({'sides'},
                                    {'side_length', 'outer_radius', 'outer_diameter', 'inner_radius', 'inner_diameter'})

    # ------------------------------------------------------------------------------------------------------------------
    def _nodes_and_angles(self) -> None:
        """
        Computes the nodes and the angles of the nodes of the regular polygon.
        """
        if len(self._angles) > 0 and self._unit == Context.get_unit_length_current():
            return

        self._unit = Context.get_unit_length_current()
        self._nodes.clear()
        self._angles.clear()

        step = 2.0 * math.pi / self.sides
        radius = self.outer_radius
        if self.sides % 2 == 0:
            # Even number of sides.
            angle = step / 2.0
        else:
            # Odd number of sides.
            angle = math.pi / 2.0

        for i in range(self.sides):
            self._nodes.append(Vector2(x=radius * math.cos(angle), y=radius * math.sin(angle)))
            self._angles.append(Angle.normalize(math.degrees(angle)))
            angle -= step

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sides(self) -> int:
        """
        Returns the number of sides of the polygon.
        """
        return self._args['sides']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the outer radius of the regular polygon.
        """
        if 'outer_radius' in self._args:
            return self.uc(self._args['outer_radius'])

        if 'outer_diameter' in self._args:
            return self.uc(0.5 * self._args['outer_diameter'])

        if 'inner_radius' in self._args:
            return self.uc(self._args['inner_radius'] / math.cos(math.pi / self.sides))

        if 'inner_diameter' in self._args:
            return self.uc(0.5 * self._args['inner_diameter'] / math.cos(math.pi / self.sides))

        if 'side_length' in self._args:
            return self.uc(self._args['side_length'] / (2.0 * math.sin(math.pi / self.sides)))

        raise AssertionError('Should not be reached')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_diameter(self) -> float:
        """
        Returns the outer diameter of the regular polygon.
        """
        if 'outer_radius' in self._args:
            return self.uc(2.0 * self._args['outer_radius'])

        if 'outer_diameter' in self._args:
            return self.uc(self._args['outer_diameter'])

        if 'inner_radius' in self._args:
            return self.uc(2.0 * self._args['inner_radius'] / math.cos(math.pi / self.sides))

        if 'inner_diameter' in self._args:
            return self.uc(self._args['inner_diameter'] / math.cos(math.pi / self.sides))

        if 'side_length' in self._args:
            return self.uc(self._args['side_length'] / (math.sin(math.pi / self.sides)))

        raise AssertionError('Should not be reached')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the inner radius of the regular polygon.
        """
        if 'inner_radius' in self._args:
            return self.uc(self._args['inner_radius'])

        if 'inner_diameter' in self._args:
            return self.uc(self._args['inner_diameter'] / 2.0)

        if 'outer_radius' in self._args:
            return self.uc(self._args['outer_radius'] * math.cos(math.pi / self.sides))

        if 'outer_diameter' in self._args:
            return self.uc(0.5 * self._args['outer_diameter'] * math.cos(math.pi / self.sides))

        if 'side_length' in self._args:
            return self.uc(self._args['side_length'] / (2.0 * math.tan(math.pi / self.sides)))

        raise AssertionError('Should not be reached')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_diameter(self) -> float:
        """
        Returns the inner diameter of the regular polygon.
        """
        if 'inner_radius' in self._args:
            return self.uc(2.0 * self._args['inner_radius'])

        if 'inner_diameter' in self._args:
            return self.uc(self._args['inner_diameter'])

        if 'outer_radius' in self._args:
            return self.uc(2.0 * self._args['outer_radius'] * math.cos(math.pi / self.sides))

        if 'outer_diameter' in self._args:
            return self.uc(self._args['outer_diameter'] * math.cos(math.pi / self.sides))

        if 'side_length' in self._args:
            return self.uc(self._args['side_length'] / (math.tan(math.pi / self.sides)))

        raise AssertionError('Should not be reached')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def side_length(self) -> float:
        """
        Returns the inner radius of the regular polygon.
        """
        if 'inner_radius' in self._args:
            return self.uc(2.0 * self._args['inner_radius'] * math.tan(math.pi / self.sides))

        if 'inner_diameter' in self._args:
            return self.uc(self._args['inner_diameter'] * math.tan(math.pi / self.sides))

        if 'outer_radius' in self._args:
            return self.uc(2.0 * self._args['outer_radius'] * math.sin(math.pi / self.sides))

        if 'outer_diameter' in self._args:
            return self.uc(self._args['outer_diameter'] * math.sin(math.pi / self.sides))

        if 'side_length' in self._args:
            return self.uc(self._args['side_length'])

        raise AssertionError('Should not be reached')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_angle(self) -> float:
        """
        Returns the inner angle in degrees between the edges of the regular polygon.
        """
        return 180.0 - 360.0 / self.sides

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def exterior_angle(self) -> float:
        """
        Returns the exterior angle in degrees between the edges of the regular polygon.
        """
        return 360.0 / self.sides

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angles(self) -> List[float]:
        """
        Returns the angles in degrees of the position of the nodes of the regular polygon in polar coordinates.
        """
        self._nodes_and_angles()

        return self._angles

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the coordinates of the nodes of the regular polygon.
        """
        self._nodes_and_angles()

        return self._nodes

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the convexity of this polygon.
        """
        return self._args.get('convexity')

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return self._build_polygon(context)

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return Polygon(primary=self.nodes, convexity=self.convexity)

# ----------------------------------------------------------------------------------------------------------------------
