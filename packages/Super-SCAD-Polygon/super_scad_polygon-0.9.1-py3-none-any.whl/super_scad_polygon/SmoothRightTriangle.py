from typing import List, Set

from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_polygon.RightTriangle import RightTriangle
from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothRightTriangle(SmoothPolygonMixin, RightTriangle):
    """
    A widget for right triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 width: float,
                 depth: float,
                 profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None = None,
                 extend_sides_by_eps: bool | Set[int] | None = None,
                 delta: float | None = None):
        """
        Object constructor.

        :param width: The width of the right triangle.
        :param depth: The depth of the right triangle.
        :param profile_factories: The profile factories to be applied at nodes of the right triangle. When a single
                                  profile factory is given, this profile will be applied at all nodes.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        SmoothPolygonMixin.__init__(self,
                                    profile_factories=profile_factories)
        RightTriangle.__init__(self,
                               width=width,
                               depth=depth,
                               extend_sides_by_eps=extend_sides_by_eps,
                               delta=delta)

# ----------------------------------------------------------------------------------------------------------------------
