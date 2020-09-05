# pysomo

_pysomo_ (for **so**lid **mo**deling) is a small solid modeling library. This library allows you to create 3D models in Python and export them to various 3D file formats.

## Requirements
_pysomo_ creates an _xcsg_ file, an XML file that can be parsed by the _xcsg_ application to create export your models in various file formats. _pysomo_ does not include _xcsg_, it can be downloaded separately: [download xcsg](https://github.com/arnholm/xcsg).

## Installation
1. To install, simply run `pip install pysomo`
2. To export from xcsg format to a 3D model file, the _xcsg_ application must be in the same directory as your application.

## Examples
The following code creates the solid above.
```
import pysomo as csg

# Create a circle and subtract a square from it.
circle = csg.Circle(30)
square = csg.Square(50)
shape = circle - square

# Make the shape a solid via extrusion.
solid = shape.linear_extrude(1) # Creates a volume by extrusion

# Export
root = csg.Root(solid) # Root of the xml document
csg.Exporter(r"solid.xcsg").export_obj(root) # Exports as obj
```

The following code creates the shape above.
```
import pysomo as csg

# Draw a house.
vertices = [
    (0, 0),
    (0, 4),
    (2, 5),
    (4, 4),
    (4, 0)
]
polygon = csg.Polygon(vertices)

# Export
root = csg.Root(polygon)
csg.Exporter(r"solid.xcsg").export_obj(root) # Exports as obj
```

The following code creates the shape above.
```
import pysomo as csg

vertices = [(math.sin(i / 100), i) for i in range(0, 100)]
vertices += [(math.sin((100 - i) / 100) + 1, i) for i in range(0, 100)]
polygon = csg.Polygon(vertices)

# Export
root = csg.Root(polygon)
csg.Exporter(r"solid.xcsg").export_obj(root) # Exports as obj
```

