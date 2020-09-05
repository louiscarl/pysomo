# pysomo

_pysomo_ (for **so**lid **mo**deling) is a small solid modeling library. This library allows you to create 3D models in Python and export them to various 3D file formats.

## Requirements
_pysomo_ creates an _xcsg_ file, an XML file that can be parsed by the _xcsg_ application to create export your models in various file formats. _pysomo_ does not include _xcsg_, it can be downloaded separately: [download xcsg](https://github.com/arnholm/xcsg).

## Installation
1. To install, simply run `pip install pysomo`
2. To export from xcsg format to a 3D model file, the _xcsg_ application must be in the same directory as your application.

## Examples

### Extrusion
![Extrusion solid](/img/solid.png)
The following code creates the solid above.
```
import pysomo as csg

# Create a circle and subtract a square from it.
circle = csg.Circle(30)
square = csg.Square(50)
shape = circle - square

# Make the shape a solid via extrusion.
solid = shape.linear_extrude(10) # Creates a volume by extrusion

# Export
root = csg.Root(solid) # Root of the xml document
csg.Exporter(r"solid.xcsg").export_obj(root) # Exports as obj
```

### Stairs
![Stairs](/img/stairs.png)
The following code builds the stairs above up to the maximum height allowed by a building code, using the maximum step height allowed.
```
# Let's say these are the building code requirements for stairs, in inches.
to_meters = lambda inches: 0.0254 * inches
min_clear_width = to_meters(3 * 12)
max_stair_height = to_meters(163)
max_riser_height = to_meters(7 + 1 / 2)
min_tread_depth = to_meters(11)

# Build the staircase steps by union of every step.
step = somo.Cuboid(min_clear_width, max_riser_height, min_tread_depth, center='false')
steps = step # Initially, the stairs are a single step
step_count = 1 # Number of steps in the stairs
# Let's keep adding steps until it's illegal!
while (step_count + 1) * max_riser_height < max_stair_height:
    steps = steps + step.translate(0, max_riser_height * step_count, min_tread_depth * step_count)
    step_count += 1

# Build the stringers
vertices = [ # The vertices are calculated from the steps we built above
    (min_clear_width, 0, 0),
    (min_clear_width, 0, min_tread_depth),
    (min_clear_width, max_riser_height * step_count, min_tread_depth * step_count),
    (min_clear_width, max_riser_height * (step_count - 1), min_tread_depth * step_count),
    (0, 0, 0),
    (0, 0, min_tread_depth),
    (0, max_riser_height * step_count, min_tread_depth * step_count),
    (0, max_riser_height * (step_count - 1), min_tread_depth * step_count),
]
stringers = somo.Polyhedron(vertices)

# The union of steps and stringers creates the stairwell.
root = somo.Root(steps + stringers)

# Export to obj format.
somo.Exporter(r"stairs.xcsg").export_obj(root)
```
