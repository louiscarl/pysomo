# pysomo

_pysomo_ (for **so**lid **mo**deling) is a small solid modeling library. This library allows you to create 3D models in Python and export them to various 3D file formats.

## Requirements
_pysomo_ creates an _xcsg_ file, an XML file that can be parsed by the _xcsg_ application to create export your models in various file formats. _pysomo_ does not include _xcsg_, it can be downloaded separately: [download xcsg](https://github.com/arnholm/xcsg/releases).

## Installation
1. To install, simply run `pip install pysomo`
2. To export from xcsg format to a 3D model file, the [_xcsg_ application](https://github.com/arnholm/xcsg) must be in the same directory as your application.

## Examples

### Extrusion
The following code creates a coin with a square hole in the middle.
```python
import pysomo as somo


# First let's create the round part of the coin.
coin_circle = somo.Circle(30)
# This creates the base solid of the coin.
coin = coin_circle.linear_extrude(2)
# Create the solid to use as the extrusion. Note that we use the offset method
# to create a smaller circle from the base. This will give us the rim.
coin_extr = coin_circle.offset(-5, True).linear_extrude(1)


# Now we use the subtraction operator to extrude our shapes from the coin.
coin = coin - coin_extr.translate(0, 0, 1.5) - coin_extr.translate(0, 0, -0.5)


# Let's now create the square hole in the coin.
square = somo.Square(20)
square_rim = square.linear_extrude(2)
square_hole = square.offset(-2, False).linear_extrude(2)


# Our final coin is the base coin with a square removed.
coin = coin + square_rim - square_hole


# Now we export to a file. The Root is responsible for building the xcsg file.
root = somo.Root(coin)
# The Exporter reads the root file and uses the xcsg application.
somo.Exporter(r"coin.obj").export_obj(root)

```
This creates the coin below.

![Extrusion solid](https://github.com/louiscarl/pysomo/raw/master/img/coin.png "Extrusion of a square from a larger circle.")

### Stairs
The following code builds a staircase up to the maximum height allowed by a building code, if we were to use the maximum step height allowed. It demonstrates modelisation via code. It also demonstrates that figures do not mutate when an operation is applied. Instead, every operation returns a new figure.
```python
import pysomo as somo


def to_meters(inches):
    return 0.0254 * inches


# Let's say these are the building code requirements for stairs, in inches.
min_clear_width = to_meters(3 * 12)
max_stair_height = to_meters(163)
max_riser_height = to_meters(7 + 1 / 2)
min_tread_depth = to_meters(11)


# Build the staircase steps by union of every step.
step = somo.Cuboid(
    min_clear_width,
    max_riser_height,
    min_tread_depth,
    center='false')
steps = step  # Initially, the stairs are a single step
step_count = 1  # Number of steps in the stairs


# Let's keep adding steps while the height is code compliant.
while (step_count + 1) * max_riser_height < max_stair_height:
    # Note that every operation in fact returns a new solid and does not
    # modify the original step, so you can reuse solids for every translation.
    steps += step.translate(
        0,
        max_riser_height * step_count,
        min_tread_depth * step_count)
    step_count += 1


# Build the stringers. Vertices are calculated from the steps we built above.
stairs_height = max_riser_height * step_count
stairs_depth = min_tread_depth * step_count
vertices = [
    (min_clear_width, 0, 0),
    (min_clear_width, 0, min_tread_depth),
    (min_clear_width, stairs_height, stairs_depth),
    (min_clear_width, stairs_height - max_riser_height, stairs_depth),
    (0, 0, 0),
    (0, 0, min_tread_depth),
    (0, stairs_height, stairs_depth),
    (0, stairs_height - max_riser_height, stairs_depth),
]
stringers = somo.Polyhedron(vertices)


# The union of steps and stringers creates the stairwell.
root = somo.Root(steps + stringers)


# Export to obj format.
somo.Exporter(r"stairs.obj").export_obj(root)
```
This creates the staircase below.

![Stairs](https://github.com/louiscarl/pysomo/raw/master/img/stairs.png "Generated stairs at a compliant height.")

An advantage in this style of 3d modeling is the simplicity of changing your models through variables. Let's say we added a zero to the maximum height allowed:

![Stairs](https://github.com/louiscarl/pysomo/raw/master/img/superstairs.png "Generated staircase that is way too high.")
