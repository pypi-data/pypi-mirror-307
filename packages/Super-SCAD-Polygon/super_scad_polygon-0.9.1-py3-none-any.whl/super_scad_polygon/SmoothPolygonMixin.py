from abc import ABC
from typing import List

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.RoughFactory import RoughFactory
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory


class SmoothPolygonMixin(PolygonMixin, ABC):
    """
    A widget for polygons with smooth corners.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None):
        """
        Object constructor.

        :param profile_factories: The profile factories to be applied at nodes of the polygon. When a single profile
                                  factory is given, this profile will be applied at all nodes.
        """
        # PolygonMixin.__init__(self)

        self._profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None = profile_factories
        """
        The profile factories to be applied at nodes of the polygon.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def profile_factories(self) -> List[SmoothProfileFactory]:
        """
        Returns the list of smooth profile factories.
        """
        profile_factories = self._profile_factories
        if isinstance(profile_factories, SmoothProfileFactory):
            return [profile_factories for _ in range(self.sides)]

        if isinstance(profile_factories, List):
            return profile_factories + [RoughFactory() for _ in range(len(profile_factories), self.sides)]

        return [RoughFactory() for _ in range(self.sides)]

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if self.extend_sides_by_eps():
            polygon = self._build_polygon_extended(context=context)
        else:
            polygon = self._build_polygon(context=context)

        nodes = self.nodes
        inner_angles = self.inner_angles(context)
        normal_angles = self.normal_angles(context)
        profile_factories = self.profile_factories
        for index in range(len(nodes)):
            profile = profile_factories[index]
            polygon = profile.create_smooth_profile(inner_angle=inner_angles[index],
                                                    normal_angle=normal_angles[index],
                                                    position=nodes[index],
                                                    child=polygon)

        return polygon

# ----------------------------------------------------------------------------------------------------------------------
