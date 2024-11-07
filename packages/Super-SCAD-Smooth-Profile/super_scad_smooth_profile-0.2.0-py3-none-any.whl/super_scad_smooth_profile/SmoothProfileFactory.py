from abc import ABC, abstractmethod

from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Vector2 import Vector2

from super_scad_smooth_profile.SmoothProfile import SmoothProfile


class SmoothProfileFactory(ABC):
    """
    A smooth profile factory is an abstract base class for smooth profile factories. A smooth profile factory is an
    object that creates a smooth profile SuperSCAD widget given an inner angle, a normal angle, and a position of a
    node and its two vertices, a.k.a., a corner or edge.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def create_smooth_profile(self,
                              *,
                              inner_angle: float,
                              normal_angle: float,
                              position: Vector2,
                              child: ScadWidget) -> SmoothProfile:
        """
        Returns a smooth profile widget.

        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param position: The position of the node.
        :param child: The child object on which the smoothing must be applied.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
