import inspect
import math

import pysomo as csg

export_enabled = False


def arguments_to_attributes(args):
    arguments = []
    for a in args:
        value = args[a]
        arguments.append(f'{a}="{value}"')
    return ' '.join(arguments)


def assert_and_export(expected_str, actual_root, name=''):
    if expected_str not in actual_root.dump_xcsg():
        print('expected_str:')
        print(expected_str)
        print('actual str:')
        print(actual_root.dump_xcsg())
    assert expected_str in actual_root.dump_xcsg()

    if export_enabled:
        test_name = inspect.stack()[1][3]
        file_name = f'{test_name}.obj' if not name else f'{test_name}_{name}.obj'

        # 2d shapes need a third dimension
        if isinstance(actual_root.children[0], csg.figures.Shape):
            actual_root.children[0] = actual_root.children[0].linear_extrude(1)

        csg.Exporter(file_name).export_obj(actual_root)


def test_operations2d():
    s = csg.Square(60)
    c = csg.Circle(30)
    operations = [
        (lambda a, b: a + b, 'union2d'),
        (lambda a, b: a - b, 'difference2d'),
        (lambda a, b: a & b, 'intersection2d')
    ]

    for operation in operations:
        op, name = operation
        actual = csg.Root(op(s, c))
        expected = f'<xcsg version="1.0"><{name}><square size="60" center="true" /><circle r="30" /></{name}></xcsg>'
        assert_and_export(expected, actual, name)


def test_operations3d():
    c = csg.Cube(40)
    s = csg.Sphere(30)
    operations = [
        (lambda a, b: a + b, 'union3d'),
        (lambda a, b: a - b, 'difference3d'),
        (lambda a, b: a & b, 'intersection3d')
    ]

    for operation in operations:
        op, name = operation
        actual = csg.Root(op(c, s))
        expected = f'<xcsg version="1.0"><{name}><cube size="40" center="true" /><sphere r="30" /></{name}></xcsg>'
        assert_and_export(expected, actual, name)


def test_simple_shapes():
    shapes = [
        (lambda: csg.Circle(30), 'circle', {'r': '30'}),
        (lambda: csg.Square(30), 'square', {'size': '30', 'center': 'true'}),
        (lambda: csg.Rectangle(30, 20, center='false'), 'rectangle', {'dx': '30', 'dy': '20', 'center': 'false'})
    ]

    for shape in shapes:
        sh, name, args = shape
        actual = csg.Root(sh())
        expected = f'<xcsg version="1.0"><{name} {arguments_to_attributes(args)} /></xcsg>'
        assert_and_export(expected, actual, name)


def test_simple_solids():
    shapes = [
        (lambda: csg.Cone(30, 20, 10, center='true'), 'cone', {'r1': '30', 'r2': '20', 'h': '10', 'center': 'true'}),
        (lambda: csg.Sphere(30), 'sphere', {'r': '30'}),
        (lambda: csg.Cube(30, center='false'), 'cube', {'size': '30', 'center': 'false'}),
        (lambda: csg.Cuboid(30, 20, 10), 'cuboid', {'dx': '30', 'dy': '20', 'dz': '10', 'center': 'true'}),
        (lambda: csg.Cylinder(30, 20), 'cylinder', {'r': '30', 'h': '20', 'center': 'true'}),
    ]

    for shape in shapes:
        sh, name, args = shape
        actual = csg.Root(sh())
        expected = f'<xcsg version="1.0"><{name} {arguments_to_attributes(args)} /></xcsg>'
        assert_and_export(expected, actual, name)


def test_simple_extrude():
    c = csg.Circle(30)
    extrusions = [
        (lambda x: x.linear_extrude(10.5), 'linear_extrude', {'dz': '10.5'}),
        (lambda x: x.rotate_extrude(1, 0), 'rotate_extrude', {'angle': '1', 'pitch': '0'})
    ]

    for extrusion in extrusions:
        extr, name, args = extrusion
        actual = csg.Root(extr(c))
        expected = f'<xcsg version="1.0"><{name} {arguments_to_attributes(args)}><circle r="30" /></{name}></xcsg>'
        assert_and_export(expected, actual, name)


def test_polygon():
    vertices = [
        (0, 0),
        (4, 0),
        (4, 3),
        (2, 5),
        (0, 3)
    ]
    p = csg.Polygon(vertices)
    actual = csg.Root(p)

    expected_vertices = ''.join([f'<vertex x="{x}" y="{y}" />' for x, y in vertices])
    expected = f'<xcsg version="1.0"><polygon><vertices>{expected_vertices}</vertices></polygon></xcsg>'

    assert_and_export(expected, actual)


def test_translated_polygon():
    vertices = [
        (0, 0),
        (4, 0),
        (4, 3),
        (2, 5),
        (0, 3)
    ]
    p = csg.Polygon(vertices).translate(-1, -1)
    actual = csg.Root(p)

    expected_vertices = ''.join([f'<vertex x="{x}" y="{y}" />' for x, y in vertices])
    expected_tmatrix = '<trow c0="1" c1="0" c2="0" c3="-1" /><trow c0="0" c1="1" c2="0" c3="-1" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" />'
    expected = f'<xcsg version="1.0"><polygon><vertices>{expected_vertices}</vertices><tmatrix>{expected_tmatrix}</tmatrix></polygon></xcsg>'

    assert_and_export(expected, actual)


def test_scaled_circle():
    c = csg.Circle(10).scale(x=2)
    actual = csg.Root(c)

    expected_tmatrix = '<trow c0="2" c1="0" c2="0" c3="0" /><trow c0="0" c1="1" c2="0" c3="0" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" />'
    expected = f'<xcsg version="1.0"><circle r="10"><tmatrix>{expected_tmatrix}</tmatrix></circle></xcsg>'
    assert_and_export(expected, actual)


def test_scaled_sphere():
    s = csg.Sphere(10).scale(x=2)
    actual = csg.Root(s)

    expected_tmatrix = '<trow c0="2" c1="0" c2="0" c3="0" /><trow c0="0" c1="1" c2="0" c3="0" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" />'
    expected = f'<xcsg version="1.0"><sphere r="10"><tmatrix>{expected_tmatrix}</tmatrix></sphere></xcsg>'
    assert_and_export(expected, actual)


def test_rotated_cuboid():
    angle = math.pi / 4
    c = csg.Cuboid(10, 1, 1).rotate(z=angle)
    actual = csg.Root(c)

    cos_ = math.cos(angle)
    sin_ = math.sin(angle)

    expected_tmatrix = f'<trow c0="{cos_}" c1="-{sin_}" c2="0" c3="0" /><trow c0="{sin_}" c1="{cos_}" c2="0" c3="0" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" />'
    expected = f'<xcsg version="1.0"><cuboid dx="10" dy="1" dz="1" center="true"><tmatrix>{expected_tmatrix}</tmatrix></cuboid></xcsg>'
    assert_and_export(expected, actual)


def test_simple_polyhedron():
    vertices = [
        (0, 0, 0),
        (0, 4, 0),
        (2, 5, 0),
        (4, 4, 0),
        (4, 0, 0),
        (0, 0, 4),
        (0, 4, 4),
        (2, 5, 4),
        (4, 4, 4),
        (4, 0, 4)
    ]
    p = csg.Polyhedron(vertices).translate(-1, -1, -1)
    actual = csg.Root(p)

    expected_vertices = ''.join([f'<vertex x="{x}" y="{y}" z="{z}" />' for x, y, z in vertices])
    expected_tmatrix = '<trow c0="1" c1="0" c2="0" c3="-1" /><trow c0="0" c1="1" c2="0" c3="-1" /><trow c0="0" c1="0" c2="1" c3="-1" /><trow c0="0" c1="0" c2="0" c3="1" />'
    expected = f'<xcsg version="1.0"><polyhedron><vertices>{expected_vertices}</vertices><tmatrix>{expected_tmatrix}</tmatrix></polyhedron></xcsg>'

    assert_and_export(expected, actual)


def test_minkowski2d():
    s = csg.Square(10)
    c = csg.Circle(5)
    actual = csg.Root(s.minkowski(c))

    expected = '<xcsg version="1.0"><minkowski2d><square size="10" center="true" /><circle r="5" /></minkowski2d></xcsg>'

    assert_and_export(expected, actual)


def test_minkowski3d():
    c = csg.Cube(10)
    s = csg.Sphere(5)
    actual = csg.Root(c.minkowski(s))

    expected = '<xcsg version="1.0"><minkowski3d><cube size="10" center="true" /><sphere r="5" /></minkowski3d></xcsg>'

    assert_and_export(expected, actual)


def test_project2d():
    c = csg.Cube(10)
    s = csg.Sphere(5).translate(0, 100, 0)
    actual = csg.Root((c + s).project())

    expected_tmatrix = '<tmatrix><trow c0="1" c1="0" c2="0" c3="0" /><trow c0="0" c1="1" c2="0" c3="100" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" /></tmatrix>'
    expected = f'<xcsg version="1.0"><projection2d><union3d><cube size="10" center="true" /><sphere r="5">{expected_tmatrix}</sphere></union3d></projection2d></xcsg>'

    assert_and_export(expected, actual)


def test_hull2d():
    s = csg.Square(10)
    c = csg.Circle(5).translate(15, 0)
    actual = csg.Root(s.hull(c))

    expected_tmatrix = '<tmatrix><trow c0="1" c1="0" c2="0" c3="15" /><trow c0="0" c1="1" c2="0" c3="0" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" /></tmatrix>'
    expected = f'<xcsg version="1.0"><hull2d><square size="10" center="true" /><circle r="5">{expected_tmatrix}</circle></hull2d></xcsg>'

    assert_and_export(expected, actual)


def test_hull3d():
    c = csg.Cube(10)
    s = csg.Sphere(5).translate(15, 0, 0)
    actual = csg.Root(c.hull(s))

    expected_tmatrix = '<tmatrix><trow c0="1" c1="0" c2="0" c3="15" /><trow c0="0" c1="1" c2="0" c3="0" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" /></tmatrix>'
    expected = f'<xcsg version="1.0"><hull3d><cube size="10" center="true" /><sphere r="5">{expected_tmatrix}</sphere></hull3d></xcsg>'

    assert_and_export(expected, actual)
