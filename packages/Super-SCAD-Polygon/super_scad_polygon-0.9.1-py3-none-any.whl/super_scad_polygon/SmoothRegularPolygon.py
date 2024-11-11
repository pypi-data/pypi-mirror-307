from typing import List, Set

from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_polygon.RegularPolygon import RegularPolygon
from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothRegularPolygon(SmoothPolygonMixin, RegularPolygon):
    """
    Class for regular polygons.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 sides: int,
                 outer_radius: float | None = None,
                 outer_diameter: float | None = None,
                 inner_radius: float | None = None,
                 inner_diameter: float | None = None,
                 size: float | None = None,
                 profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None = None,
                 extend_sides_by_eps: bool | Set[int] | None = None,
                 delta: float | None = None):
        """
        Object constructor.

        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        RegularPolygon.__init__(self,
                                sides=sides,
                                outer_radius=outer_radius,
                                outer_diameter=outer_diameter,
                                inner_radius=inner_radius,
                                inner_diameter=inner_diameter,
                                side_length=size,
                                extend_sides_by_eps=extend_sides_by_eps,
                                delta=delta)
        SmoothPolygonMixin.__init__(self, profile_factories=profile_factories)

# ----------------------------------------------------------------------------------------------------------------------
