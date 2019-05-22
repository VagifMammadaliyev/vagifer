from random import randint

class BasePainter:
    """\
    Base class for painters. Custom painter classes must inherit from
    this one.

    Painters ares used to get the pixel (more specificly - to provide
    a way of creating new color for pixel and then return that pixel
    in `get_pixel(...)'). Painters' `get_pixel(...)' method called
    each time when particular pixel needs its color, so it's good
    to keep in mind performance problems when implementing.

    `get_pixel(...)' must return pixel as a sequence containing values
    appropriate for seleceted `brush' mode (default RGB, so sequence returned
    is in (r, g, b) format). Make your painter create pretty frames by
    implementing logic in `get_pixel(...)'.
    For example you can return black pixels for even columns of
    frame and default (random-color) pixel for odd ones:

        class MyPainter(BasePainter):

            def __init__(self):
                super().__init__()

            def get_pixel(self, pos):
                if pos[0] % 2 == 0:
                    return (0, 0, 0)
                else:
                    return super().get_pixel(pos)

    """

    def __init__(self, brush='RGB'):
        self.brush = brush

    def get_pixel(self, pos):
        """\
        pos - position of pixel that requires color

            *Note*: pos == (0, 0) is upper-left pixel

            *Note 2*: it is not an actual pixel's position, but cell's.
            Cell is a group of pixel that are of same color. They are used to
            simulate big pixels but in HD image. For example if your
            image's size is (100, 100) (pixels) and you set your
            cell's size to (10, 10) then your image will look like it
            contains only 100^2/10^2 pixels instead of 100^2 but actual size
            would be 100^2.
        """
        random_pixel = (randint(1, 255), randint(1, 255), randint(1, 255))
        return random_pixel

    def __str__(self):
        return '<{}: brush={!r}>'.format(self.__class__.__name__, self.brush)

    def __repr__(self):
        return self.__str__()
