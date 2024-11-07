from abc import ABC, abstractmethod
from typing import Any, Dict

from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Angle import Angle
from super_scad.type.Vector2 import Vector2


class SmoothProfile(ScadSingleChildParent, ABC):
    """
    Abstract parent class for smooth profiles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 args: Dict[str, Any],
                 child: ScadWidget):
        """
        Object constructor.

        :param args: The arguments of the smooth profile. Must include the following keys: inner_angle,
                     normal_angle, and position.
        :param child: The child object on which the profile is applied.
        """
        ScadSingleChildParent.__init__(self, args=args, child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_angle(self) -> float:
        """
        Returns the inner angle between the vertices at the node.
        """
        return Angle.normalize(self._args['inner_angle'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def normal_angle(self) -> float:
        """
        Returns the normal angle of the vertices at the node.
        """
        return Angle.normalize(self._args['normal_angle'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def position(self) -> Vector2:
        """
        Returns the position of the node.
        """
        return self.uc(self._args['position'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def size1(self) -> float:
        """
        Returns the size of the profile on the first vertex at the node.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def size2(self) -> float:
        """
        Returns the size of the profile on the second vertex at the node.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
