"""
visicon

copyright info:
name='visicon',
version='0.1',
description='IP address visualisation',
author='Antisense',
author_email='veracon@gmail.com',
url='http://code.google.com/p/visicon',

=======

An attempt at visualising a user based on their IP address. Visicon
would optimally be a direct port of Visiglyph [1]_ (a variation on
Identicon [2]_), but may not ever be, hence the different name, a
portmanteau of the two implementations.

Prerequisites: ::
- Python Imaging Library (PIL) >= 1.1.6

.. [1] http://digitalconsumption.com/forum/Visiglyphs-for-IP-visualisation
.. [2] http://www.docuverse.com/blog/donpark/2007/01/18/visual-security-9-block-ip-identification

"""

from hashlib import md5
# import os
# import random
# import sys

# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image
    import ImageDraw

T = TRANSPARENT = -1


class Visicon(object):
    """
    Visicon
    =======

    The Visicon class itself. This is versatile in that it isn't
    restricted to IP addresses, but could technically be used with
    any sort of string.

    The class uses md5 (or an md5-like algorithm) to encrypt the
    string, and then generates a unique image from the first four
    bytes of the hash when prompted to (upon calling
    ``Visicon.render``).

    """
    resize = 0
    min_size = 24

    def __init__(self, string, seed, size=24, background=0xffffff):
        """
        Visicon.__init__(self, string, seed, size=24) -> Visicon
        Initialises the Visicon, storing everything that could
        possibly be interpreted from the supplied ``string`` and
        ``seed``.

        """
        self.string = string
        self.seed = seed
        self.hash = md5(self.string + self.seed).hexdigest()
        self.size = size

        dec = lambda hex: int(hex, 16)
        self.block_one = dec(self.hash[0])
        self.block_two = dec(self.hash[1])
        self.block_centre = dec(self.hash[2]) & 7
        self.rotate_one = dec(self.hash[3]) & 3
        self.rotate_two = dec(self.hash[4]) & 3
        self.fg_colour = (dec(self.hash[5:7]) & 239, dec(
            self.hash[7:9]) & 239, dec(self.hash[9:11]) & 239)
        self.fg_colour2 = (dec(self.hash[11:13]) & 239, dec(
            self.hash[13:15]) & 239, dec(self.hash[15:17]) & 239)
        self.background = background

        if self.size < self.min_size:
            self.resize = self.size
            self.size = self.min_size

        self.img_size = self.size * 3
        self.quarter = self.size / 4
        self.quarter3 = self.quarter * 3
        self.half = self.size / 2
        self.third = self.size / 3
        self.double = self.size * 2
        self.centre = self.img_size / 2

        if self.background is not TRANSPARENT:
            self.image = Image.new(
                'RGB', (self.img_size,) * 2, color=self.background)
        else:
            self.image = Image.new('RGBA', (self.img_size,) * 2)

    def draw_image(self):
        """
        draw(self) -> Image.Image
        Draws the Visicon, returning the result as an
        ``Image.Image`` instance.

        """
        self.draw = ImageDraw.Draw(self.image)
        self.draw_corners()
        self.draw_sides()
        self.draw_centre()

        return self.image.resize((self.size,) * 2, Image.ANTIALIAS)

    def draw_corners(self):
        """
        draw_corners(self) -> None
        Draws the corners of the image.

        """
        corners = (
            {'x': 0, 'y': 0},
            {'x': 0, 'y': self.double},
            {'x': self.double, 'y': self.double},
            {'x': self.double, 'y': 0}
        )
        for n, corner in enumerate(corners):
            rotation = self.rotate_one + n
            self.draw_glyph(self.block_one, rotation, corner, self.fg_colour)

    def draw_centre(self):
        """
        draw_centre(self) -> None
        Draws the centre part of the image.

        """
        self.draw_glyph(self.block_centre, 0, {'x': self.size, 'y':
                        self.size}, self.fg_colour, False)

    def draw_sides(self):
        """
        draw_sides(self) -> None
        Draws the sides of the image.

        """
        sides = (
            {'x': self.size, 'y': 0},
            {'x': 0, 'y': self.size},
            {'x': self.size, 'y': self.double},
            {'x': self.double, 'y': self.size}
        )
        for n, side in enumerate(sides):
            rotation = self.rotate_two + n
            self.draw_glyph(self.block_two, rotation, side, self.fg_colour2)

    def draw_glyph(self, block, rotation, modifier, colour, outer=True):
        """
        draw_glyph(self, block, rotation, modifier, colour,\
                   outer=True) -> None
        Draws a glyph on the image, based on the far-too-many
        arguments.

        """
        if outer:
            if block is 1:  # mountains
                points = [
                    0, 0,
                    self.quarter, self.size,
                    self.half, 0
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

                points = [
                    self.half, 0,
                    self.quarter3, self.size,
                    self.size, 0
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 2:  # half triangle
                points = [
                    0, 0,
                    self.size, 0,
                    0, self.size
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 3:  # centre triangle
                points = [
                    0, 0,
                    self.half, self.size,
                    self.size, 0
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 4:  # half block
                points = [
                    0, 0,
                    0, self.size,
                    self.half, self.size,
                    self.half, 0
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 5:  # half diamond
                points = [
                    self.quarter, 0,
                    0, self.half,
                    self.quarter, self.size,
                    self.half, self.half
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 6:  # spike
                points = [
                    0, 0,
                    self.size, self.half,
                    self.size, self.size,
                    self.half, self.size
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 7:  # quarter triangle
                points = [
                    0, 0,
                    self.half, self.size,
                    0, self.size
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 8:  # diag triangle
                points = [
                    0, 0,
                    self.size, self.half,
                    self.half, self.size
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 9:  # centered mini triangle
                points = [
                    self.quarter, self.quarter,
                    self.quarter3, self.quarter,
                    self.quarter, self.quarter3
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 10:  # diag mountains
                points = [
                    0, 0,
                    self.half, 0,
                    self.half, self.half
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

                points = [
                    self.half, self.half,
                    self.size, self.half,
                    self.size, self.size
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 11:  # quarter block
                points = [
                    0, 0,
                    0, self.half,
                    self.half, self.half,
                    self.half, 0
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 12:  # point out triangle
                points = [
                    0, self.half,
                    self.half, self.size,
                    self.size, self.half
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 13:  # point in triangle
                points = [
                    0, 0,
                    self.half, self.half,
                    self.size, 0
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 14:  # diag point in
                points = [
                    self.half, self.half,
                    0, self.half,
                    self.half, self.size
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 15:  # diag point out
                points = [
                    0, 0,
                    self.half, 0,
                    0, self.half
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            else:  # diag side point out
                points = [
                    0, 0,
                    self.half, 0,
                    self.half, self.half
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)
        else:
            if block is 1:  # circle
                self.draw.ellipse((
                    (self.centre - self.quarter3, self.centre - self.quarter3),
                    (self.centre + self.quarter3, self.centre + self.quarter3)
                ), fill=colour)

            elif block is 2:  # quarter square
                points = [
                    self.quarter, self.quarter,
                    self.quarter, self.quarter3,
                    self.quarter3, self.quarter3,
                    self.quarter3, self.quarter
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 3:  # full square
                points = [
                    0, 0,
                    0, self.size,
                    self.size, self.size,
                    self.size, 0
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 4:  # quarter diamond
                points = [
                    self.half, self.quarter,
                    self.quarter3, self.half,
                    self.half, self.quarter3,
                    self.quarter, self.half
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

            elif block is 5:  # diamond
                points = [
                    self.half, 0,
                    0, self.half,
                    self.half, self.size,
                    self.size, self.half
                ]
                points = self.rotate_points(points, rotation, modifier)
                self.draw.polygon(points, fill=colour)

    def rotate_points(self, points, rotation, modifier):
        """
        rotate_points(self, points, rotation, modifier) -> tuple
        Rotate a set of points out from set modifiers.

        """
        rotation = rotation % 4
        if rotation is 1:
            n = 0
            while n < len(points):
                tmp1 = n
                val1 = points[tmp1]
                tmp2 = n + 1
                val2 = points[tmp2]
                points[tmp1] = val2 + modifier['x']
                points[tmp2] = self.size - val1 + modifier['y']
                n += 2
        elif rotation is 2:
            n = 0
            while n < len(points):
                tmp1 = n
                val1 = points[tmp1]
                tmp2 = n + 1
                val2 = points[tmp2]
                points[tmp1] = self.size - val1 + modifier['x']
                points[tmp2] = self.size - val2 + modifier['y']
                n += 2
        elif rotation is 3:
            n = 0
            while n < len(points):
                tmp1 = n
                val1 = points[tmp1]
                tmp2 = n + 1
                val2 = points[tmp2]
                points[tmp1] = self.size - val2 + modifier['x']
                points[tmp2] = val1 + modifier['y']
                n += 2
        else:
            n = 0
            while n < len(points):
                tmp1 = n
                val1 = points[tmp1]
                tmp2 = n + 1
                val2 = points[tmp2]
                points[tmp1] = val1 + modifier['x']
                points[tmp2] = val2 + modifier['y']
                n += 2

        return points
