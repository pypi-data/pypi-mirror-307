import math

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Union import Union
from super_scad.d2.Circle import Circle
from super_scad.d2.Polygon import Polygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Position2D import Position2D
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type import Vector2
from super_scad_circle_sector.CircleSector import CircleSector
from super_scad_smooth_profile.SmoothProfile import SmoothProfile


class Fillet(SmoothProfile):
    """
    Applies a fillet to vertices at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float,
                 inner_angle: float,
                 normal_angle: float,
                 position: Vector2,
                 child: ScadWidget):
        """
        Object constructor.

        :param radius: The radius of the fillet.
        :param inner_angle: Inner angle of the corner.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param child: The child object on which the fillet is applied.
        """
        SmoothProfile.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Return the radius of the fillet.
        """
        return self.uc(self._args['radius'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size1(self) -> float:
        """
        Returns the size of the profile on the first vertex at the node.
        """
        return self.radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size2(self) -> float:
        """
        Returns the size of the profile on the second vertex at the node.
        """
        return self.radius

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        inner_angle = self.inner_angle
        radius = self.radius

        if radius > 0.0 and inner_angle < 180.0:
            # The corner is convex.
            alpha = math.radians(inner_angle) / 2.0
            fillet = self._build_fillet_pos(context, alpha, 90.0)

            return Difference(children=[self.child, fillet])

        if radius > 0.0 and inner_angle > 180.0:
            # The corner is concave.
            alpha = math.radians(360.0 - inner_angle) / 2.0
            fillet = self._build_fillet_pos(context, alpha, -90.0)

            return Union(children=[self.child, fillet])

        if radius < 0.0:
            # Negative radius.
            fillet = self._build_fillet_neg()

            return Union(children=[self.child, fillet])

        return self.child

    # ------------------------------------------------------------------------------------------------------------------
    def _build_fillet_pos(self, context: Context, alpha: float, rotation: float) -> ScadWidget:
        """
        Builds a fillet.

        :param context: The build context.
        :param alpha: The angle of the fillet.
        """
        radius = self.radius

        x = radius * math.cos(alpha) + context.eps
        y = radius * math.cos(alpha) ** 2 / math.sin(alpha)
        polygon = Polygon(points=[Vector2(0.0, context.eps), Vector2(x, -y), Vector2(-x, -y)], convexity=2)
        circle = Circle(radius=radius, fn4n=True)
        fillet = Difference(children=[polygon,
                                      Translate2D(vector=Vector2(0.0, -radius / math.sin(alpha)),
                                                  child=circle)])

        return Position2D(angle=self.normal_angle + rotation,
                          vector=self.position,
                          child=fillet)

    # ------------------------------------------------------------------------------------------------------------------
    def _build_fillet_neg(self) -> ScadWidget:
        """
        Builds a fillet.
        """
        inner_angle = self.inner_angle

        return Translate2D(vector=self.position,
                           child=CircleSector(start_angle=self.normal_angle + 0.5 * inner_angle,
                                              end_angle=self.normal_angle - 0.5 * inner_angle,
                                              radius=-self.radius,
                                              extend_legs_by_eps=True,
                                              fn4n=True))

# ----------------------------------------------------------------------------------------------------------------------
