# -*- coding: utf-8 -*-
# Adapted from libcaca's Python img2txt

import caca
from caca.canvas import Canvas
from caca.dither import Dither
from PIL import Image


def to_ascii(
    img,
    width=60,
    height=None,
    font_width=6,
    font_height=10,
    brightness=1.0,
    contrast=1.0,
    gamma=1.0,
    ditalgo="fstein",
    exformat="ansi",
        charset="ascii"):
    """
    Takes a file-pointer to an image and converts it to ASCII.

        Options:
          -h, --help                      This help
          -v, --version                   Version of the program
          -W, --width=WIDTH               Width of resulting image
          -H, --height=HEIGHT             Height of resulting image
          -x, --font-width=WIDTH          Width of output font
          -y, --font-height=HEIGHT        Height of output font
          -b, --brightness=BRIGHTNESS     Brightness of resulting image
          -c, --contrast=CONTRAST         Contrast of resulting image
          -g, --gamma=GAMMA               Gamma of resulting image
          -d, --dither=DITHER             Dithering algorithm to use
          -f, --format=FORMAT             Format of the resulting image
          -C, --charset=CHARSET           Charset of the resulting image

        DITHER (ditalgo) list:
          - none: no dithering
          - ordered2: 2x2 ordered dithering
          - ordered4: 4x4 ordered dithering
          - ordered8: 8x8 orederd dithering
          - random: random dithering
          - fstein: Floyd-Steinberg dithering

        FORMAT (exformat) list:
          - caca: native libcaca format
          - ansi: ANSI
          - utf8: UTF-8 with ANSI escape codes
          - utf8cr: UTF-8 with ANSI escape codes and MS-DOS \\r
          - html: HTML
          - html3: backwards-compatible HTML
          - bbfr: BBCode (French)
          - irc: IRC with mIRC colours
          - ps: PostScript document
          - svg: SVG vector image
          - tga: TGA image
          - troff: troff source

        CHARSET (charset) list:
          - ascii: use only ascii character
          - shades: use unicode character
          - blocks: use unicode quarter-cell combinations
    """
    img = Image.open(img)

    if "shades" or "blocks" in charset:
        exformat = "utf8"  # Will not work in ascii mode

    # Explicitly encode argument strings as ASCII
    ditalgo = ditalgo.encode('ascii')
    exformat = exformat.encode('ascii')
    charset = charset.encode('ascii')

    # Set height to some proportion
    if height is None:
        height = round(width * img.size[1] * font_width / img.size[0] / font_height)

    # Setup the canvas
    cv = Canvas(width, height)
    cv.set_color_ansi(caca.COLOR_DEFAULT, caca.COLOR_TRANSPARENT)

    #########################
    #### Begin Dithering ####
    #########################
    RMASK = 0x00ff0000
    GMASK = 0x0000ff00
    BMASK = 0x000000ff
    AMASK = 0xff000000
    BPP = 32
    DEPTH = 4

    if img.mode == 'RGB':
        img = img.convert('RGBA')
    #reorder rgba
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        img = Image.merge("RGBA", (b, g, r, a))
    dit = Dither(BPP, img.size[0], img.size[1], DEPTH * img.size[0], RMASK, GMASK, BMASK, AMASK)

    # print(dit.get_algorithm_list());
    # import ipdb; ipdb.set_trace()
    dit.set_algorithm(ditalgo)
    dit.set_brightness(brightness)
    dit.set_gamma(gamma)
    dit.set_contrast(contrast)
    dit.set_charset(charset)
    dit.bitmap(cv, 0, 0, width, height, img.tobytes())

    #########################
    #### End Dithering ######
    #########################

    return cv.export_to_memory(exformat)
