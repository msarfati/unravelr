#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urwid


def scroll_up():
    txt.set_text("Scrolling up")


def scroll_down():
    txt.set_text("Scrolling down")


palette = [
    ('body','black','light gray', 'standout'),
    ('reverse','light gray','black'),
    ('header','white','dark red', 'bold'),
    ('important','dark blue','light gray',('standout','underline')),
    ('editfc','white', 'dark blue', 'bold'),
    ('editbx','light gray', 'dark blue'),
    ('editcp','black','light gray', 'standout'),
    ('bright','dark gray','light gray', ('bold','standout')),
    ('buttn','black','dark cyan'),
    ('buttnf','white','dark blue','bold'),
]


def show_key_or_exit(key):
    if key in ('f8'):
        raise urwid.ExitMainLoop()
    frame.footer = urwid.AttrWrap(urwid.Text(
        [u"Pressed: ", key.__repr__()]), 'header')

text_header = (u"Ƹ̵̡❀ Ｔｅｒｍｂｌｒ ❀̵̨̄Ʒ\n(up and down arrows to scroll, F8 to quit)")

# [urwid.Text(post.format(**i), align='center') for i in tree.execute("$.posts")]
listbox_content = [[urwid.Text(post.format(**i), align='center'), urwid.Divider()] for i in tree.execute("$.posts")]
listbox_content = [i for s in listbox_content for i in s]


header = urwid.AttrWrap(urwid.Text(text_header, align='center'), 'header')
listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)

loop = urwid.MainLoop(
    widget=frame,
    palette=palette,
    screen=urwid.raw_display.Screen(),
    unhandled_input=show_key_or_exit,
    handle_mouse=False,
)
loop.run()
