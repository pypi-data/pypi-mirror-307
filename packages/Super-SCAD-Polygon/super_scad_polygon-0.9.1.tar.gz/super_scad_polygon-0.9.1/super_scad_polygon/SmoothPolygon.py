from typing import List, Set

from super_scad.d2.Polygon import Polygon
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothPolygon(SmoothPolygonMixin, Polygon):
    """
    A widget for polygons with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 primary: List[Vector2] | None = None,
                 points: List[Vector2] | None = None,
                 secondary: List[Vector2] | None = None,
                 secondaries: List[List[Vector2]] | None = None,
                 convexity: int | None = None,
                 profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None = None,
                 extend_sides_by_eps: bool | Set[int] | None = None,
                 delta: float | None = None):
        """
        Object constructor.

        :param primary: The list of 2D points of the polygon.
        :param points: Alias for primary.
        :param secondary: The secondary path that will be subtracted from the polygon.
        :param secondaries: The secondary paths that will be subtracted form the polygon.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param profile_factories: The profile factories to be applied at nodes of the right triangle. When a single
                                  profile factory is given, this profile will be applied at all nodes.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        Polygon.__init__(self,
                         primary=primary,
                         points=points,
                         secondary=secondary,
                         secondaries=secondaries,
                         convexity=convexity,
                         extend_sides_by_eps=extend_sides_by_eps,
                         delta=delta)
        SmoothPolygonMixin.__init__(self, profile_factories=profile_factories)

# ----------------------------------------------------------------------------------------------------------------------
