from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.SmoothProfile import SmoothProfile


class Rough(SmoothProfile):
    """
    Applies no finish to the vertices at a node (a.k.a. edge).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, child: ScadWidget):
        """
        Object constructor.

        :param child: The child object which will be left rough.
        """
        SmoothProfile.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size1(self) -> float:
        """
        Returns the size of the profile on the first vertex at the node.
        """
        return 0.0

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size2(self) -> float:
        """
        Returns the size of the profile on the second vertex at the node.
        """
        return 0.0

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return self.child

# ----------------------------------------------------------------------------------------------------------------------
