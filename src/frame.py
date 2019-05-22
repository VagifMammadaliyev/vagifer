import os, sys
from random import randint

import imageio
from PIL import Image

from painter import BasePainter


class Frames:
    """\
    Each frame in `frames' list is given particular index (`no') even if
    you have already set each frame's index before passing them
    in a list to initializer. Index of passed frames are used only for
    sorting frames inside initializer. If passed frame has no explicitly set
    index (which means that it is set to 0) then those frames added
    to sequence after indexed frames added.

    You can pass frames and 'fill(...)' them. For full information
    check help(Frame.fill). `painter' is used to decide
    which pixels are used to fill each frame. If you want specific
    `painter' for each frame, then fill frames manually by calling
    their own `fill(...)' method.
    """

    def __init__(self, frames=[]):
        self.frames = []
        self.last = 0  # no. of last frame

        if frames:
            indexed = [frame for frame in frames if frame.no > 0]
            not_indexed = [frame for frame in frames if frame.no <= 0]

            if indexed:
                self.frames += sorted(indexed)
                self.last = self.frames[-1].no

            for frame in not_indexed:
                self.add(frame)

            # normalize indices
            n = 0
            for frame in self.frames:
                n += 1
                frame.no = n

            self.last = n


    def add(self, frame):
        """Add frame with correct index (a.k.a `no')"""
        self.last += 1
        frame.no = self.last
        self.frames.append(frame)

        if frame.no != 1:
            self.frames.sort()

    def fill(self, cellwidth=1, cellheight=1, painter=None, ignore=[]):
        """Same as `fill(...)' method for individual `Frame' object
        but you must not fill each frame manually.

        ignore - is a list of frame indices that are ignored (not filled
            by this method)"""

        if painter is None:
            painter = BasePainter()

        l = len(self.frames)
        for i, frame in enumerate(self.frames, start=1):
            if i not in ignore:
                print('Filling {}/{}'.format(i, l))
                frame.fill(cellwidth, cellheight, painter)
            else:
                print('Igored {}/{}'.format(i, l))


    def save(self, name):
        """Creates folder to place frames. If folder already exists
        then creates new one under another name. Then calls `_makegif()'
        to create '.gif' out of frames"""

        folder = name + '-gif'

        foldercreated = False
        num = 0
        suffix = ''
        while not foldercreated:
            try:
                os.makedirs(folder + suffix, exist_ok=False)
            except OSError:
                num += 1
                suffix = str(num)
                print('\rDirectory already exists. ', end='')
                print('Creating under another name: {}'.format(folder + suffix), end='')
            else:
                foldercreated = True
        print()

        self.dir = folder + suffix  # final folder name

        print('Saving:')
        for i, frame in enumerate(self.frames, start=1):
            frame.name = name + str(i) + '.png'
            frame.image.save('./{}/{}'.format(self.dir, frame.name))
            print('\r\t{} frames saved to ./{}/ so far...'.format(i, self.dir), end='')
            sys.stdout.flush()
        print('\n\tSaved all!')

        self._makegif()


    def _makegif(self):
        """Make gif out of frames and places it in the same folder as frames
        images. Name of '.gif' file is name of folder where frames are without
        '-gif{#}' suffix"""

        print('Making gif...')
        images = []
        l = len(self.frames)
        i = 1
        for frame in self.frames:
            images.append(imageio.imread(os.path.join(self.dir, frame.name)))
            print('\r\tCollecting images: {}/{}'.format(i, l), end='')
            i += 1

        print('\n\tSaving to {}...'.format(self.dir))
        # also get rid of -gif suffix in self.dir (folder.name)
        gifname = self.dir[:self.dir.find('-gif')] + '.gif'
        imageio.mimsave(os.path.join(self.dir, gifname), images)
        print('\tSaved as {}'.format(gifname))


    def __getitem__(self, item):
        try:
            item = int(item)
            return self.frames[item]
        except ValueError:
            raise TypeError('Expected int as index not ' + type(item).__name__)

    def __str__(self):
        return '<{}: total={}>'.format(self.__class__.__name__, self.last)

    def __repr__(self):
        return self.__str__()


class Frame:
    """\
    If `image' is None, then new `PIL.Image.Image' object is created with
    given `size' and `mode'. Pass `PIL.Image.Image' object as `image' if you
    don't want to `fill_frame(...)' by hand. By the way, if you don't ever use
    `fill_frame(...)' then there is not point of using this code.

    no - index of frame (position in possible sequence of frames)
    """

    def __init__(self, size, mode='RGB', no=0, image=None):
        self.no = no if no > 0 else 0
        self.size = tuple(size)

        if image is None:
            self.image = Image.new(size=self.size, mode=mode)
            self.mode = mode
        else:
            self.image = image
            self.size = size
            self.mode = image.mode


    def fill(self, cellwidth=1, cellheight=1, painter=BasePainter()):
        """Fill frame with colored pixels. Color of each pixel decided by `painter'.

        (cellwidth, cellheight) - size (in pixels) of one 'big pixel'
            used to fill frame.
        """

        width = self.size[0] // cellwidth
        heigth = self.size[1] // cellheight

        for i in range(width + 1):
            for j in range(heigth + 1):
                pixel = tuple(painter.get_pixel((i, j)))
                for i_ in range(cellwidth):
                    for j_ in range(cellheight):
                        place = (i_ + cellwidth * i, j_ + cellheight * j)
                        # try/catch used to simulate hiding parts of
                        # overflowed cells when self.size
                        # cannot be divided completely by cell{width/heigth}
                        try:
                            self.image.putpixel(place, pixel)
                        except IndexError:
                            continue
                filling = i * (heigth + 1) + j
                perc = filling / ((width + 1) * (heigth + 1))
                print('\rFilled {:.2f}%'.format(perc * 100), end='')
        print('\rFilling complete')

        pixelsfilled = self.size[0] * self.size[1]

        return pixelsfilled


    def __eq__(self, other):
        return self.no == other.no

    def __lt__(self, other):
        return self.no < other.no

    def __le__(self, other):
        return self.no <= other.no

    def __gt__(self, other):
        return self.no > other.no

    def __ge__(self, other):
        return self.no >= other.no

    def __str__(self):
        no = self.no if self.no > 0 else '?'
        return '<{}: size={} mode={!r} #{}>'.format(
            self.__class__.__name__, self.size, self.mode, no)

    def __repr__(self):
        return self.__str__()


# helper function
def create_gif(name, size: tuple, cellsize: tuple, frames: int, painter):
    """Just creates gif. You don't need to call this function
    for more special gifs but sometimes everything you need is this function.

    name - name of '.gif' file
    size - size of frame (image) in pixels
    cellsize - size of cell in pixels. Refer to `painter.BasePainter'
    frames - amount of frames in gif
    painter - `painter.BasePainter' instance
    """

    amount = frames
    frames = []
    for i in range(amount):
        frames.append(Frame(size))

    frames = Frames(frames)
    frames.fill(cellsize[0], cellsize[1], painter)
    frames.save(name)
