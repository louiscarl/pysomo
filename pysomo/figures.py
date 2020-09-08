from __future__ import annotations

from math import cos, sin

import xml.etree.ElementTree as ET


class Figure(object):
    def __init__(self, type_, attributes=None):
        self.type_ = type_
        self.attributes = attributes if attributes else dict()
        self.children = []

    def __sub_element__(self, parent):
        attr = dict()
        for a in self.attributes.keys():
            attr[a] = str(self.attributes[a])
        e = ET.SubElement(parent, self.type_, attr)

        for c in self.children:
            c.__sub_element__(e)


class Shape(Figure):
    def __init__(self, type_, attributes=None):
        super().__init__(type_, attributes=attributes)

    def __add__(self, other: Shape) -> Shape:
        return Union2d(self, other)

    def __sub__(self, other: Shape) -> Shape:
        return Difference2d(self, other)

    def __and__(self, other: Shape) -> Shape:
        return Intersection2d(self, other)

    def linear_extrude(self, dz: float) -> Solid:
        """Extrudes linearly into a solid by dz.

        Arguments:
            dz: the height of the extrusion
        """
        return LinearExtrude(self, dz)

    def rotate_extrude(self, angle, pitch) -> Solid:
        """Extrudes by rotating along the y axis to create a solid.
        Arguments:
            angle:
            pitch:
        """
        return RotateExtrude(self, angle, pitch)

    def transform_extrude(self, other: Shape) -> Solid:
        """Extrudes between two shapes to create a solid.
        Arguments:
            other:
        """
        return TransformExtrude(self, other)

    def sweep(self, spline_path) -> Solid:
        """Extrudes along a spline curve.
        Arguments:
            spline_path:
        """
        return Sweep(self, spline_path)

    def fill(self) -> Shape:
        """Fills any holes in the shape."""
        return Fill2d(self)

    def hull(self, other: Shape) -> Shape:
        """Hull of two figures.
        Arguments:
            other:
        """
        return Hull2d(self, other)

    def offset(self, delta, round_, chamfer=False) -> Shape:
        """Adds a offset (margin).
        Arguments:
            delta:
            round_:
            chamfer:
        """
        return Offset2d(self, delta, round_, chamfer)

    def minkowski(self, other: Shape) -> Shape:
        """Minkowski sum of two figures.
        Arguments:
            other:
        """
        return Minkowski2d(self, other)

    def translate(self, x, y) -> Shape:
        """Translates a shape in 2d"""
        shape = Shape(self.type_, self.attributes)
        shape.children += self.children
        shape.children.append(Translation3d(x, y, 0, 1))
        return shape

    def scale(self, x=1, y=1) -> Shape:
        """Scales a shape in 2d"""
        shape = Shape(self.type_, self.attributes)
        shape.children += self.children
        shape.children.append(Scale3d(x, y, 1, 1))
        return shape


class Solid(Figure):
    '''
    The base shape for any solid, including the results of operations. This
    shouldn't have to be used directly.
    '''

    def __init__(self, type_, attributes=None):
        super().__init__(type_, attributes=attributes)

    def __add__(self, other: Solid) -> Solid:
        return Union3d(self, other)

    def __sub__(self, other: Solid) -> Solid:
        return Difference3d(self, other)

    def __and__(self, other: Solid) -> Solid:
        return Intersection3d(self, other)

    def hull(self, other: Solid) -> Solid:
        """Hull of two figures.
        Arguments:
            other:
        """
        return Hull3d(self, other)

    def minkowski(self, other: Solid) -> Solid:
        """Minkowski sum of two figures.
        Arguments:
            other:
        """
        return Minkowski3d(self, other)

    def project(self) -> Shape:
        """Projects onto the XY plane."""
        return Projection2d(self)

    def translate(self, x, y, z) -> Solid:
        """Translates a solid in 3d"""
        solid = Solid(self.type_, self.attributes)
        solid.children += self.children
        solid.children.append(Translation3d(x, y, z, 1))
        return solid

    def scale(self, x=1, y=1, z=1) -> Solid:
        """Scales a solid in 3d"""
        solid = Solid(self.type_, self.attributes)
        solid.children += self.children
        solid.children.append(Scale3d(x, y, z, 1))
        return solid

    def rotate(self, x=0, y=0, z=0) -> Solid:
        """Rotates a shape in 2d"""
        if (x != 0 and (y != 0 or z != 0)) or (y != 0 and z != 0):
            raise Exception("Only one axis should be set at a time.")

        solid = Solid(self.type_, self.attributes)
        solid.children += self.children
        if x != 0:
            solid.children.append(RotateX3d(x))
        elif y != 0:
            solid.children.append(RotateY3d(y))
        else:
            solid.children.append(RotateZ3d(z))
        return solid


class LinearExtrude(Solid):
    def __init__(self, a: Shape, dz):
        super().__init__('linear_extrude')
        self.children.append(a)
        self.attributes['dz'] = dz


class RotateExtrude(Solid):
    def __init__(self, a: Shape, angle, pitch):
        super().__init__('rotate_extrude')
        self.children.append(a)
        self.attributes['angle'] = angle
        self.attributes['pitch'] = pitch


class TransformExtrude(Solid):
    def __init__(self, a: Shape, b: Shape):
        super().__init__('transform_extrude')
        self.children.append(a)
        self.children.append(b)


class Sweep(Solid):
    def __init__(self, a: Shape, spline_path):
        super().__init__('sweep')
        self.children.append(a)
        self.children.append(spline_path)


class Fill2d(Shape):
    def __init__(self, a: Shape):
        super().__init__('fill2d')
        self.children.append(a)


class Offset2d(Shape):
    def __init__(self, a: Shape, delta, round_, chamfer):
        super().__init__('offset2d')
        self.children.append(a)
        self.attributes['delta'] = delta
        self.attributes['round'] = round_
        self.attributes['chamfer'] = chamfer


class Hull2d(Shape):
    def __init__(self, a: Shape, b: Shape):
        super().__init__('hull2d')
        self.children.append(a)
        self.children.append(b)


class Minkowski2d(Shape):
    def __init__(self, a: Shape, b: Shape):
        super().__init__('minkowski2d')
        self.children.append(a)
        self.children.append(b)


class Projection2d(Shape):
    def __init__(self, a: Shape):
        super().__init__('projection2d')
        self.children.append(a)


class Operation2d(Shape):
    def __init__(self, shape_type, a: Shape, b: Shape):
        super().__init__(shape_type)
        self.children.append(a)
        self.children.append(b)


class Intersection2d(Operation2d):
    def __init__(self, a: Shape, b: Shape):
        super().__init__('intersection2d', a, b)


class Difference2d(Operation2d):
    def __init__(self, a: Shape, b: Shape):
        super().__init__('difference2d', a, b)


class Union2d(Operation2d):
    def __init__(self, a: Shape, b: Shape):
        super().__init__('union2d', a, b)


class Circle(Shape):
    def __init__(self, radius):
        super().__init__('circle')
        self.attributes['r'] = radius


class Square(Shape):
    def __init__(self, size, center='true'):
        super().__init__('square')
        self.attributes['size'] = size
        self.attributes['center'] = center


class Rectangle(Shape):
    def __init__(self, dx: float, dy: float, center='true'):
        super().__init__('rectangle')
        self.attributes['dx'] = dx
        self.attributes['dy'] = dy
        self.attributes['center'] = center


class Polygon(Shape):
    def __init__(self, vertices):
        super().__init__('polygon')
        self.children.append(Vertices2d(vertices))


class Vertices2d(Shape):
    def __init__(self, vertices):
        super().__init__('vertices')
        self.children += [Vertex2d.from_tuple(v) for v in vertices]


class Vertex2d(Figure):
    def __init__(self, x: float, y: float):
        super().__init__('vertex')
        self.attributes['x'] = x
        self.attributes['y'] = y

    @staticmethod
    def from_tuple(vertex):
        x, y = vertex
        return Vertex2d(x, y)


class Operation3d(Solid):
    def __init__(self, solid_type, a: Solid, b: Solid):
        super().__init__(solid_type)
        self.children.append(a)
        self.children.append(b)


class Intersection3d(Operation3d):
    def __init__(self, a: Solid, b: Solid):
        super().__init__('intersection3d', a, b)


class Difference3d(Operation3d):
    def __init__(self, a: Solid, b: Solid):
        super().__init__('difference3d', a, b)


class Union3d(Operation3d):
    def __init__(self, a: Solid, b: Solid):
        super().__init__('union3d', a, b)


class Hull3d(Solid):
    def __init__(self, a: Solid, b: Solid):
        super().__init__('hull3d')
        self.children.append(a)
        self.children.append(b)


class Minkowski3d(Solid):
    def __init__(self, a: Solid, b: Solid):
        super().__init__('minkowski3d')
        self.children.append(a)
        self.children.append(b)


class Cone(Solid):
    def __init__(self, r1: float,  r2: float,  h: float,  center='true'):
        super().__init__('cone')
        self.attributes['r1'] = r1
        self.attributes['r2'] = r2
        self.attributes['h'] = h
        self.attributes['center'] = center


class Sphere(Solid):
    def __init__(self, radius):
        super().__init__('sphere')
        self.attributes['r'] = radius


class Cube(Solid):
    def __init__(self, size, center='true'):
        super().__init__('cube')
        self.attributes['size'] = size
        self.attributes['center'] = center


class Cuboid(Solid):
    def __init__(self, dx: float, dy: float, dz: float, center='true'):
        super().__init__('cuboid')
        self.attributes['dx'] = dx
        self.attributes['dy'] = dy
        self.attributes['dz'] = dz
        self.attributes['center'] = center


class Cylinder(Solid):
    def __init__(self, r: float,  h: float,  center='true'):
        super().__init__('cylinder')
        self.attributes['r'] = r
        self.attributes['h'] = h
        self.attributes['center'] = center


class Polyhedron(Solid):
    def __init__(self, vertices):
        super().__init__('polyhedron')
        self.children.append(Vertices3d(vertices))


class Vertices3d(Figure):
    def __init__(self, vertices):
        super().__init__('vertices')
        self.children += [Vertex3d.from_tuple(v) for v in vertices]


class Vertex3d(Figure):
    def __init__(self, x, y, z):
        super().__init__('vertex')
        self.attributes['x'] = x
        self.attributes['y'] = y
        self.attributes['z'] = z

    @staticmethod
    def from_tuple(vertex):
        x, y, z = vertex
        return Vertex3d(x, y, z)


class Face(Figure):
    def __init__(self, indexes):
        super().__init__()
        for i in indexes:
            self.children.append(Fv(i))


class Fv(Figure):
    def __init__(self, index):
        super().__init__()
        self.attributes['index'] = index


class TMatrix(Figure):
    def __init__(self, rows):
        super().__init__('tmatrix')
        self.children += rows


class TRow(Figure):
    def __init__(self, c0, c1, c2, c3):
        super().__init__('trow')
        self.attributes['c0'] = c0
        self.attributes['c1'] = c1
        self.attributes['c2'] = c2
        self.attributes['c3'] = c3


class Translation3d(TMatrix):
    def __init__(self, x, y, z, w):
        rows = (
            TRow(1, 0, 0, x),
            TRow(0, 1, 0, y),
            TRow(0, 0, 1, z),
            TRow(0, 0, 0, w)
        )
        super().__init__(rows)


class Scale3d(TMatrix):
    def __init__(self, x, y, z, w):
        rows = (
            TRow(x, 0, 0, 0),
            TRow(0, y, 0, 0),
            TRow(0, 0, z, 0),
            TRow(0, 0, 0, w)
        )
        super().__init__(rows)


class RotateX3d(TMatrix):
    def __init__(self, angle):
        rows = (
            TRow(0, cos(angle), -sin(angle), 0),
            TRow(0, sin(angle),  cos(angle), 0),
            TRow(1,          0,           0, 0),
            TRow(0,          0,           0, 1)
        )
        super().__init__(rows)


class RotateY3d(TMatrix):
    def __init__(self, angle):
        rows = (
            TRow(-sin(angle), 0, cos(angle), 0),
            TRow( cos(angle), 0, sin(angle), 0),  # noqa: E201
            TRow(          0, 1,          0, 0),  # noqa: E201
            TRow(          0, 0,          0, 1)   # noqa: E201
        )
        super().__init__(rows)


class RotateZ3d(TMatrix):
    def __init__(self, angle):
        rows = (
            TRow(cos(angle), -sin(angle), 0, 0),
            TRow(sin(angle),  cos(angle), 0, 0),
            TRow(         0,          0,  1, 0),  # noqa: E201
            TRow(         0,          0,  0, 1)   # noqa: E201
        )
        super().__init__(rows)
