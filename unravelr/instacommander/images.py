# -*- coding: utf-8 -*-
# Hacked from https://github.com/hit9/img2txt
from PIL import Image


class ANSIImage(object):
    def __init__(self, original, output_size=80.0):
        '''
        :param original: Raw image bytes
        :type original: io.BytesIO

        :param output_size: Size of ANSI stream output. Default to 80.0
        :type output_size: float
        '''
        self.original = Image.open(original).convert('RGBA')
        self.output_size = output_size
        self.img = self.resize(self.original, maxLen=output_size)
        self.stream = self.generate_ANSI(
            pixels=self.img.load(),
            width=self.img.size[0],
            height=self.img.size[1],
            bgcolor_rgba=None,
        )

    def resize(self, img, antialias=True, maxLen=80.0):
        """
        Resizes image prior to processing.

        Application will handle dynamic detection of maxLen, based on terminal size

        :param img: A PIL.Image object
        :type img: PIL.Image

        :param antialias:
        :type antialias: bool

        :param maxLen: Size of the image
        :type maxLen: float
        """
        if maxLen is not None:
            native_width, native_height = img.size
            rate = float(maxLen) / max(native_width, native_height)
            width = int(rate * native_width)
            height = int(rate * native_height)

            if native_width != width or native_height != height:
                img = img.resize((width, height), Image.ANTIALIAS
                                 if antialias else Image.NEAREST)

        return img

    def getANSIcolor_for_rgb(self, rgb):
        """
        Convert to web-safe color since that's what terminals can handle in
        "256 color mode"
          https://en.wikipedia.org/wiki/ANSI_escape_code
        http://misc.flogisoft.com/bash/tip_colors_and_formatting#bash_tipscolors_and_formatting_ansivt100_control_sequences # noqa
        http://superuser.com/questions/270214/how-can-i-change-the-colors-of-my-xterm-using-ansi-escape-sequences # noqa
        """
        websafe_r = int(round((rgb[0] / 255.0) * 5))
        websafe_g = int(round((rgb[1] / 255.0) * 5))
        websafe_b = int(round((rgb[2] / 255.0) * 5))

        # Return ANSI coolor
        # https://en.wikipedia.org/wiki/ANSI_escape_code (see 256 color mode
        # section)
        return int(((websafe_r * 36) + (websafe_g * 6) + websafe_b) + 16)

    def generate_ANSI_to_set_fg_bg_colors(self, cur_fg_color, cur_bg_color, new_fg_color, new_bg_color):
        # This code assumes that ESC[49m and ESC[39m work for resetting bg and fg
        # This may not work on all terminals in which case we would have to use
        # ESC[0m
        # to reset both at once, and then put back fg or bg that we actually want

        # We don't change colors that are already the way we want them - saves
        # lots of file size

        # use array mechanism to avoid multiple escape sequences if we need to
        # change fg and bg
        color_array = []

        if new_bg_color != cur_bg_color:
            if new_bg_color is None:
                color_array.append('49')        # reset to default
            else:
                color_array += self.getANSIbgarray_for_ANSIcolor(new_bg_color)

        if new_fg_color != cur_fg_color:
            if new_fg_color is None:
                color_array.append('39')        # reset to default
            else:
                color_array += self.getANSIfgarray_for_ANSIcolor(new_fg_color)

        if len(color_array) > 0:
            return "\x1b[" + ";".join(color_array) + "m"
        else:
            return ""

    def getANSIbgarray_for_ANSIcolor(self, ANSIcolor):
        """Return array of color codes to be used in composing an SGR escape
        sequence. Using array form lets us compose multiple color updates without
        putting out additional escapes"""
        # We are using "256 color mode" which is available in xterm but not
        # necessarily all terminals
        # To set BG in 256 color you use a code like ESC[48;5;###m
        return ['48', '5', str(ANSIcolor)]

    def getANSIbgstring_for_ANSIcolor(self, ANSIcolor):
        # Get the array of color code info, prefix it with ESCAPE code and
        # terminate it with "m"
        return "\x1b[" + ";".join(self.getANSIbgarray_for_ANSIcolor(ANSIcolor)) + "m"

    def alpha_blend(src, dst):
        # Does not assume that dst is fully opaque
        # See https://en.wikipedia.org/wiki/Alpha_compositing - section on "Alpha
        # Blending"
        src_multiplier = (src[3] / 255.0)
        dst_multiplier = (dst[3] / 255.0) * (1 - src_multiplier)
        result_alpha = src_multiplier + dst_multiplier
        if result_alpha == 0:       # special case to prevent div by zero below
            return (0, 0, 0, 0)
        else:
            return (
                int(((src[0] * src_multiplier) +
                    (dst[0] * dst_multiplier)) / result_alpha),
                int(((src[1] * src_multiplier) +
                    (dst[1] * dst_multiplier)) / result_alpha),
                int(((src[2] * src_multiplier) +
                    (dst[2] * dst_multiplier)) / result_alpha),
                int(result_alpha * 255)
            )

    def generate_ANSI(self, pixels, width, height, bgcolor_rgba, get_pixel_func=None, is_overdraw=False):
        if get_pixel_func is None:
            # just treat pixels as 2D array
            get_pixel_func = lambda pixels, x, y: (" ", pixels[x, y])

        # Compute ANSI bg color and strings we'll use to reset colors when moving
        # to next line
        if bgcolor_rgba is not None:
            bgcolor_ANSI = self.getANSIcolor_for_rgb(bgcolor_rgba)
            # Reset cur bg color to bgcolor because \n will fill the new line with
            # this color
            bgcolor_ANSI_string = self.getANSIbgstring_for_ANSIcolor(bgcolor_ANSI)
        else:
            bgcolor_ANSI = None
            # Reset cur bg color default because \n will fill the new line with
            # this color
            # reset bg to default (if we want to support terminals that can't
            # handle this will need to instead use 0m which clears fg too and then
            # when using this reset prior_fg_color to None too
            bgcolor_ANSI_string = "\x1b[49m"

        # removes all attributes (formatting and colors) to start in a known state
        string = "\x1b[0m"

        prior_fg_color = None       # this is an ANSI color not rgba
        prior_bg_color = None       # this is an ANSI color not rgba
        cursor_x = 0

        for h in range(height):
            for w in range(width):

                draw_char, rgba = get_pixel_func(pixels, w, h)

                # Handle fully or partially transparent pixels - but not if it is
                # the special "erase" character (None)
                skip_pixel = False
                if draw_char is not None:
                    alpha = rgba[3]
                    if alpha == 0:
                        skip_pixel = True       # skip any full transparent pixel
                    elif alpha != 255 and bgcolor_rgba is not None:
                        # non-opaque so blend with specified bgcolor
                        rgba = self.alpha_blend(rgba, bgcolor_rgba)

                if not skip_pixel:
                    # Throw away alpha channel - can still have non-fully-opaque
                    # alpha value here if bgcolor was partially transparent or if
                    # no bgcolor and not fully transparent. Could make argument to
                    # use threshold to decide if throw away (e.g. >50% transparent)
                    # vs. consider opaque (e.g. <50% transparent) but at least for
                    # now we just throw it away
                    rgb = rgba[:3]
                    # If we've got the special "erase" character turn it into
                    # outputting a space using the bgcolor which if None will
                    # just be a reset to default bg which is what we want
                    if draw_char is None:
                        draw_char = " "
                        color = bgcolor_ANSI
                    else:
                        # Convert from RGB to ansi color, using closest color
                        color = self.getANSIcolor_for_rgb(rgb)
                        # Optimization - if we're drawing a space and the color is
                        # the same as a specified bg color then just skip this. We
                        # need to make this check here because the conversion to
                        # ANSI can cause colors that didn't match to now match
                        # We cannot do this optimization in overdraw mode because
                        # we cannot assume that the bg color is already drawn at
                        # this location
                        if not is_overdraw and (draw_char == " ") and \
                                (color == bgcolor_ANSI):
                            skip_pixel = True

                    if not skip_pixel:

                        if len(draw_char) > 1:
                            raise ValueError(
                                "Not allowing multicharacter draw strings")

                        # If we are not at the cursor x location (happens if we
                        # skip pixels) output sequence to get there
                        # This is how we implement transparency - we don't draw
                        # spaces, we skip via cursor moves
                        if cursor_x < w:
                            # **SIZE - Note that when the bgcolor is specified
                            # (not None) and not overdrawing another drawing
                            # (as in an animation case) an optimization could be
                            # performed to draw spaces rather than output cursor
                            # advances. This would use less
                            # size when advancing less than 3 columns since the min
                            # escape sequence here is len 4. Not implementing this
                            # now
                            # code to advance N columns ahead
                            string += "\x1b[{0}C".format(w - cursor_x)
                            cursor_x = w

                        # Generate the ANSI sequences to set the colors the way we
                        # want them
                        if draw_char == " ":

                            # **SIZE - If we are willing to assume terminals that
                            # support ECH (Erase Character) as specified in here
                            # http://vt100.net/docs/vt220-rm/chapter4.html we could
                            # replace long runs of same-color spaces with single
                            # ECH codes. Seems like it is only correct to do this
                            # if BCE is supported though (
                            # http://superuser.com/questions/249898/how-can-i-prevent-os-x-terminal-app-from-overriding-vim-colours-on-a-remote-syst) # noqa
                            # else "erase" would draw the _default_ background
                            # color not the currently set background color

                            # We are supposed to output a space, so we're going to
                            # need to change the background color. No, we can't
                            # output an "upper ascii" character that fills the
                            # entire foreground - terminals don't display these the
                            # same way, if at all.
                            # Since we're outputting a space we can leave the prior
                            # fg color intact as it won't be used
                            string += self.generate_ANSI_to_set_fg_bg_colors(
                                prior_fg_color, prior_bg_color, prior_fg_color,
                                color)
                            prior_bg_color = color

                        else:
                            # We're supposed to output a non-space character, so
                            # we're going to need to change the foreground color
                            # and make sure the bg is set appropriately
                            string += self.generate_ANSI_to_set_fg_bg_colors(
                                prior_fg_color, prior_bg_color, color,
                                bgcolor_ANSI)
                            prior_fg_color = color
                            prior_bg_color = bgcolor_ANSI

                        # Actually output the character
                        string += draw_char

                        cursor_x = cursor_x + 1

            # Handle end of line - unless last line which is NOP because we don't
            # want to do anything to the _line after_ our drawing
            if (h + 1) != height:

                # Reset bg color so \n fills with it
                string += bgcolor_ANSI_string
                prior_bg_color = bgcolor_ANSI       # because it has been reset

                # Move to next line. If this establishes a new line in the terminal
                # then it fills the _newly established line_
                # to EOL with current bg color. However, if cursor had been moved
                # up and this just goes back down to an existing
                # line, no filling occurs
                string += "\n"
                cursor_x = 0
        string += "\x1b[0m\n"
        return string
