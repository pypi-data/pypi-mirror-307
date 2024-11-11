import math
from typing import List

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Empty import Empty
from super_scad.boolean.Intersection import Intersection
from super_scad.d2.Circle import Circle
from super_scad.d2.Polygon import Polygon
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type.Angle import Angle
from super_scad.type.Vector2 import Vector2


class CircleSector(ScadWidget):
    """
    Widget for creating circle sectors.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | None = None,
                 start_angle: float | None = None,
                 end_angle: float | None = None,
                 radius: float | None = None,
                 inner_radius: float | None = None,
                 outer_radius: float | None = None,
                 extend_legs_by_eps: bool | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param angle: The angle of the circle sector (implies the starting angle is 0.0).
        :param start_angle: The start angle of the circle sector.
        :param end_angle: The end angle of the circle sector.
        :param radius: The radius of the circle sector (implies inner radius is 0.0).
        :param inner_radius: The inner radius of the circle sector.
        :param outer_radius: The outer radius of the circle sector.
        :param extend_legs_by_eps: Whether to extend the "legs", i.e., the straight sides of the circle sector, by eps
                                   for a clear overlap.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a circle with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'angle'}, {'start_angle', 'end_angle'})
        admission.validate_exclusive({'radius'}, {'inner_radius', 'outer_radius'})
        admission.validate_required({'radius', 'outer_radius'}, {'angle', 'end_angle'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of the circle sector.
        """
        return Angle.normalize(self.end_angle - self.start_angle)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def start_angle(self) -> float:
        """
        Returns the start angle of the circle sector.
        """
        if 'angle' in self._args:
            return Angle.normalize(self._args['angle']) if self._args['angle'] < 0.0 else 0.0

        return Angle.normalize(self._args['start_angle'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def end_angle(self) -> float:
        """
        Returns the end angle of the circle sector.
        """
        if 'angle' in self._args:
            return Angle.normalize(self._args['angle']) if self._args['angle'] > 0.0 else 0.0

        return Angle.normalize(self._args['end_angle'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the outer radius of the circle sector.
        """
        return self.outer_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the inner radius of this circle sector.
        """
        return self.uc(self._args.get('inner_radius', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the outer radius of this circle sector.
        """
        return self.uc(self._args.get('outer_radius', self._args.get('radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_legs_by_eps(self) -> bool:
        """
        Returns whether to extend the "legs", i.e., the straight sides of the circle sector, by eps for a clear overlap.
        """
        return self._args.get('extend_legs_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._args.get('fa')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self.uc(self._args.get('fs'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._args.get('fn4n')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._args.get('fn')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int:
        """
        Returns the convexity of the pie slice.
        """
        return 1 if self.angle < 180.0 else 2

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        angle = self.angle

        if round(self.outer_radius, context.length_digits) <= 0.0 or round(angle, context.angle_digits) == 0.0:
            return Empty()

        if round(self.inner_radius, context.length_digits) == 0.0:
            circles = Circle(radius=self.outer_radius, fa=self.fa, fs=self.fs, fn=self.fn, fn4n=self.fn4n)
        else:
            circles = Difference(children=[Circle(radius=self.outer_radius,
                                                  fa=self.fa,
                                                  fs=self.fs,
                                                  fn=self.fn,
                                                  fn4n=self.fn4n),
                                           Circle(radius=self.inner_radius,
                                                  fa=self.fa,
                                                  fs=self.fs,
                                                  fn=self.fn,
                                                  fn4n=self.fn4n)])

        if round(angle - 360.0, context.angle_digits) == 0.0:
            return circles

        if round(angle - 90.0, context.angle_digits) == 0.0:
            points = self._polygon_is_q1()

        elif round(angle - 180.0, context.angle_digits) == 0.0:
            points = self._polygon_is_q2()

        elif round(angle - 270.0, context.angle_digits) == 0.0:
            points = self._polygon_is_q3()

        elif round(angle - 90.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q1()

        elif round(angle - 180.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q2()

        elif round(angle - 270.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q3()

        elif round(angle - 360.0, context.angle_digits) < 0.0:
            points = self._polygon_in_q4()
        else:
            raise ValueError('Math is broken!')

        extend_sides_by_eps = {index for index in range(len(points))}
        if not self.extend_legs_by_eps:
            extend_sides_by_eps.remove(0)
            extend_sides_by_eps.remove(len(points) - 1)

        return Intersection(children=[circles,
                                      Polygon(points=points,
                                              convexity=self.convexity,
                                              extend_sides_by_eps=extend_sides_by_eps)])

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q1(self) -> List[Vector2]:
        """
        Returns a masking polygon in one quadrant.
        """
        phi = Angle.normalize(self.angle / 2.0, 90.0)
        start_angle = self.start_angle
        end_angle = self.end_angle

        size2 = self.outer_radius / math.cos(math.radians(phi))

        return [Vector2(0.0, 0.0),
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q2(self) -> List[Vector2]:
        """
        Returns a masking polygon in two quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle
        phi = Angle.normalize((start_angle - end_angle) / 2.0, 90.0)

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = size1 / (math.cos(math.radians(phi)) + math.sin(math.radians(phi)))

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 90.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q3(self) -> List[Vector2]:
        """
        Returns a masking polygon in three quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle
        phi = Angle.normalize((start_angle - end_angle) / 2.0, 90.0)

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = size1 / (math.cos(math.radians(phi)) + math.sin(math.radians(phi)))

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 90.0),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 180.0),
                Vector2.from_polar_coordinates(size1, start_angle - phi + 270.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_in_q4(self) -> List[Vector2]:
        """
        Returns a masking polygon in four quadrants.
        """
        return self._polygon_in_q3()

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_is_q1(self) -> List[Vector2]:
        """
        Returns a masking polygon that is exactly one quadrant.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = self.outer_radius

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle + 45.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_is_q2(self) -> List[Vector2]:
        """
        Returns a masking polygon that is exactly two quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = self.outer_radius

        return [Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle + 45.0),
                Vector2.from_polar_coordinates(size1, start_angle + 135.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

    # ----------------------------------------------------------------------------------------------------------------------
    def _polygon_is_q3(self) -> List[Vector2]:
        """
        Returns a masking polygon that is exactly three quadrants.
        """
        start_angle = self.start_angle
        end_angle = self.end_angle

        size1 = math.sqrt(2.0) * self.outer_radius
        size2 = self.outer_radius

        return [Vector2.origin,
                Vector2.from_polar_coordinates(size2, start_angle),
                Vector2.from_polar_coordinates(size1, start_angle + 45.0),
                Vector2.from_polar_coordinates(size1, start_angle + 135.0),
                Vector2.from_polar_coordinates(size1, start_angle + 225.0),
                Vector2.from_polar_coordinates(size2, end_angle)]

# ----------------------------------------------------------------------------------------------------------------------
