from frame import create_gif
from examples import HypnoticPainter

# Run this test code to see what it looks like!
size = (500, 500)
cellsize = (10, 10)
size_in_cells = (size[0] // cellsize[0], size[1] // cellsize [1])
create_gif('hypno', size=size,
           cellsize=(8, 8), frames=30,
           painter=HypnoticPainter(size_in_cells, colorized=True))
