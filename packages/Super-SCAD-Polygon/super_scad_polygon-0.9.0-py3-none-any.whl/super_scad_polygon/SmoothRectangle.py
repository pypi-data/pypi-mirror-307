from typing import List

from super_scad.d2.Rectangle import Rectangle
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothRectangle(SmoothPolygonMixin, Rectangle):
    """
    A widget for right triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Vector2 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None = None,
                 delta: float | None = None):
        """
        Object constructor.

        :param size: The side_length of the rectangle.
        :param width: The width (the side_length along the x-axis) of the rectangle.
        :param depth: The depth (the side_length along the y-axis) of the rectangle.
        :param center: Whether the rectangle is centered at its position.
        :param profile_factories: The profile factories to be applied at nodes of the right triangle. When a single
                                  profile factory is given, this profile will be applied at all nodes.
        :param delta: The minimum distance between nodes, vertices and line segments for reliable computation of the
                      separation between line segments and nodes.
        """
        SmoothPolygonMixin.__init__(self,
                                    profile_factories=profile_factories,
                                    delta=delta)
        Rectangle.__init__(self,
                           size=size,
                           width=width,
                           depth=depth,
                           center=center)

# ----------------------------------------------------------------------------------------------------------------------
