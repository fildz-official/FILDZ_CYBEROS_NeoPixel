# The MIT License (MIT)
# Copyright (c) 2023 Edgaras Janušauskas and Inovatorius MB (www.fildz.com)
# Copyright (c) 2021 Jim Mussared
# Copyright (c) 2016 Damien P. George

################################################################################
# FILDZ CYBEROS WS2812 (NeoPixel) LIBRARY
#
# Fully asynchronous WS2812 library for CYBEROS.
#
# Features:
# - Completely asynchronous.
# - 8 pre-defined colors.
# - Adjustable brightness.

from machine import bitstream


class NeoPixel:
    # G R B W
    ORDER = (1, 0, 2, 3)
    # 8 pre-defined colors with default (maximum) brightness.
    C_RED = (255, 0, 0)
    C_ORANGE = (255, 135, 0)
    C_YELLOW = (255, 255, 0)
    C_GREEN = (0, 255, 0)
    C_AQUA = (0, 255, 165)
    C_BLUE = (0, 0, 255)
    C_PURPLE = (165, 0, 255)
    C_WHITE = (255, 255, 255)
    C_BLANK = (0, 0, 0)

    def __init__(self, pin, n, bpp=3, timing=1):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        # Timing arg can either be 1 for 800kHz or 0 for 400kHz,
        # or a user-specified timing ns tuple (high_0, low_0, high_1, low_1).
        self.timing = (
            ((400, 850, 800, 450) if timing else (800, 1700, 1600, 900))
            if isinstance(timing, int)
            else timing
        )
        # Set the brightness.
        self._brightness = 0.02  # From 0.0 to 1.0.
        self._rgb = (0, 0, 0)  # Current pixel color.

    def __len__(self):
        return self.n

    def __setitem__(self, i, v):
        offset = i * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = v[i]

    def __getitem__(self, i):
        offset = i * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]] for i in range(self.bpp))

    ################################################################################
    # Properties
    #
    @property
    def brightness(self):
        return self._brightness

    ################################################################################
    # Tasks
    #
    async def set_color(self, index=0, color=None):
        if color is None:
            r = int(self._rgb[0] * self._brightness)
            g = int(self._rgb[1] * self._brightness)
            b = int(self._rgb[2] * self._brightness)
        else:
            self._rgb = color
            r = int(color[0] * self._brightness)
            g = int(color[1] * self._brightness)
            b = int(color[2] * self._brightness)
        self.__setitem__(index, (r, g, b))
        await self.write()

    async def set_brightness(self, value):
        self._brightness = value
        await self.set_color()

    async def fill(self, v):
        b = self.buf
        l = len(self.buf)
        bpp = self.bpp
        for i in range(bpp):
            c = v[i]
            j = self.ORDER[i]
            while j < l:
                b[j] = c
                j += bpp

    async def write(self):
        # BITSTREAM_TYPE_HIGH_LOW = 0
        bitstream(self.pin, 0, self.timing, self.buf)
