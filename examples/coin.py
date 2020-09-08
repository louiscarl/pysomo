import src.pysomo as somo


# First let's create the round part of the coin.
coin_circle = somo.Circle(30)
# This creates the base solid of the coin.
coin = coin_circle.linear_extrude(2)
# Create the solid to use as the extrusion. Note that we use the offset method
# to create a smaller circle from the base. This will give us the rim.
coin_extr = coin_circle.offset(-5, True).linear_extrude(1)


# Now we use the subtraction operator to exclude our shapes from the coin.
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
