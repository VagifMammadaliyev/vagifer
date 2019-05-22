"""Examples

This file contain example painters. They are not very complex
but you may get an idea of how painters are implemented.

You don't have to follow these implementation styles!

Writing a painter is actually a good time killer and it is
very addicting :)
"""

from random import randint
from painter import BasePainter

#
# Implementation of HypnoticPainter.
# You can do anything you want! define how many methods you need and so on...
# But at the end you should return pixel's color
# in appropriate format
#

class HypnoticPainter(BasePainter):
    """Draws 'hypnotic' squares. Will make your friends
    give you all their money :D
    """
    def __init__(self, size, colorized=False):
        """/
        size - size of canvas painter paints. Maku sure it is the same
            as size of actual frame in 'cells' (refer to `BasePainter').
            For more information about what cell actually is.
        """
        super().__init__()

        self.frame = 0  # keep track of frames
                        # actually it is a very nice tactic

        # for some painters it is necessary to keep track
        # of canvas size, like this one
        # although you may implement it some other way w/out size (may be)
        self.size = size
        self.lastcol, self.lastrow = size[0] - 1, size[1] - 1

        self.colorized = colorized

        if colorized:
            self.colorized = True
            self.randomcolor = [randint(1, 255), randint(1, 255), randint(1, 255)]


    def get_pixel(self, pos):
        if tuple(pos) == (self.size[0] - 1, self.size[1]):
            self.frame += 1  # next frame

            if self.colorized:
                self._cycle_color() # change color of squares

        if self._is_in_square(pos):
            if self.colorized:
                return self.randomcolor
            else:
                return (0, 0, 0)
        else:
            white_pixel = (255, 255, 255)
            return white_pixel

    def _is_in_square(self, pos):
        # checks whether particular pixel is part of square
        offset = 1 if self.frame % 2 == 0 else 0

        for i in range(offset, self.size[0] // 2 + offset, 2):
            if pos[0] == i or pos[0] == self.lastcol - i:
                return pos[1] >= i and pos[1] <= self.lastrow - i

            if pos[1] == i or pos[1] == self.lastrow - i:
                return pos[0] >= i and pos[0] <= self.lastrow - i

    def _cycle_color(self):
        for i in range(len(self.randomcolor)):
            self.randomcolor[i] += 20
            if self.randomcolor[i] > 255:
                self.randomcolor[i] -= 255
