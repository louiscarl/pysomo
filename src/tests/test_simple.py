import pysomo as csg


def arguments_to_attributes(args):
    arguments = []
    for a in args:
        value = args[a]
        arguments.append(f'{a}="{value}"')
    return ' '.join(arguments)


def test_operations2d():
    s = csg.Square(40)
    c = csg.Circle(30)
    operations = [
        (lambda a, b: a + b, 'union2d'),
        (lambda a, b: a - b, 'difference2d'),
        (lambda a, b: a & b, 'intersection2d')
    ]

    for operation in operations:
        op, name = operation
        actual = csg.Root(op(s, c)).dump_xcsg()
        expected = f'<xcsg version="1.0"><{name}><square size="40" center="true" /><circle r="30" /></{name}></xcsg>'
        assert expected in actual


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
        actual = csg.Root(op(c, s)).dump_xcsg()
        expected = f'<xcsg version="1.0"><{name}><cube size="40" center="true" /><sphere r="30" /></{name}></xcsg>'
        assert expected in actual


def test_simple_shapes():
    shapes = [
        (lambda: csg.Circle(30), 'circle', {'r': '30'}),
        (lambda: csg.Square(30), 'square', {'size': '30', 'center': 'true'}),
        (lambda: csg.Rectangle(30, 20, center='false'), 'rectangle', {'dx': '30', 'dy': '20', 'center': 'false'})
    ]

    for shape in shapes:
        sh, name, args = shape
        actual = csg.Root(sh()).dump_xcsg()
        expected = f'<xcsg version="1.0"><{name} {arguments_to_attributes(args)} /></xcsg>'
        assert expected in actual


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
        actual = csg.Root(sh()).dump_xcsg()
        expected = f'<xcsg version="1.0"><{name} {arguments_to_attributes(args)} /></xcsg>'
        assert expected in actual


def test_simple_extrude():
    c = csg.Circle(30)
    extrusions = [
        (lambda x: x.linear_extrude(10.5), 'linear_extrude', {'dz': '10.5'}),
        (lambda x: x.rotate_extrude(10, 20), 'rotate_extrude', {'angle': '10', 'pitch': '20'})
    ]

    for extrusion in extrusions:
        extr, name, args = extrusion
        actual = csg.Root(extr(c)).dump_xcsg()
        expected = f'<xcsg version="1.0"><{name} {arguments_to_attributes(args)}><circle r="30" /></{name}></xcsg>'
        assert expected in actual


def test_polygon():
    vertices = [
        (0, 0),
        (0, 4),
        (2, 5),
        (4, 4),
        (4, 0)
    ]
    p = csg.Polygon(vertices)
    r = csg.Root(p)

    actual = r.dump_xcsg()
    expected_vertices = ''.join([f'<vertex x="{x}" y="{y}" />' for x, y in vertices])
    expected = f'<xcsg version="1.0"><polygon><vertices>{expected_vertices}</vertices></polygon></xcsg>'

    assert expected in actual


def test_translated_polygon():
    vertices = [
        (0, 0),
        (0, 4),
        (2, 5),
        (4, 4),
        (4, 0)
    ]
    p = csg.Polygon(vertices).translate(-1, -1)
    r = csg.Root(p)

    actual = r.dump_xcsg()
    expected_vertices = ''.join([f'<vertex x="{x}" y="{y}" />' for x, y in vertices])
    expected_tmatrix = '<trow c0="1" c1="0" c2="0" c3="-1" /><trow c0="0" c1="1" c2="0" c3="-1" /><trow c0="0" c1="0" c2="1" c3="0" /><trow c0="0" c1="0" c2="0" c3="1" />'
    expected = f'<xcsg version="1.0"><polygon><vertices>{expected_vertices}</vertices><tmatrix>{expected_tmatrix}</tmatrix></polygon></xcsg>'

    assert expected in actual


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
    r = csg.Root(p)

    actual = r.dump_xcsg()
    expected_vertices = ''.join([f'<vertex x="{x}" y="{y}" z="{z}" />' for x, y, z in vertices])
    expected_tmatrix = '<trow c0="1" c1="0" c2="0" c3="-1" /><trow c0="0" c1="1" c2="0" c3="-1" /><trow c0="0" c1="0" c2="1" c3="-1" /><trow c0="0" c1="0" c2="0" c3="1" />'
    expected = f'<xcsg version="1.0"><polyhedron><vertices>{expected_vertices}</vertices><tmatrix>{expected_tmatrix}</tmatrix></polyhedron></xcsg>'

    assert expected in actual
