import src.pysomo as somo


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