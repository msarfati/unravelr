#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Prototype for InstaCommander
import sys
import os
sys.path.insert(0, '.')
MODULE_PATH = os.path.split(os.path.realpath(__file__))[0]

from instagram.client import InstagramAPI
import requests
from io import BytesIO
from instacommander.images import ANSIImage

from tempfile import NamedTemporaryFile

view = """\
--------
{img}
{media.user}
{media.created_time}
{media.link}
Likes: {media.like_count}
Comments: {media.comment_count}
{media.tags}\
"""

# Unauthorized Client
client = InstagramAPI(
    client_id='b8fd789f28cc4db8801fcda9a733e3ae',
    client_secret='b7f009145f604e6190f420ef1d3ec350',
)

get_tty_width = lambda: int(os.popen('stty size').read().split()[1])
# output_size = round(get_tty_width() / 1.15)  # Leaves a margin
output_size = get_tty_width()


def old_poll_feed():
    feed = [i for i in client.media_popular() if i.type == 'image']  # Filter for only images
    for post in feed:
        img = BytesIO(requests.get(post.images['standard_resolution'].url).content)
        img = ANSIImage(img, output_size)
        # img = A(img, output_size)
        print(view.format(media=post, img=img.stream))


def new_poll_feed():
    feed = [i for i in client.media_popular() if i.type == 'image']  # Filter for only images
    for post in feed:
        tmp = NamedTemporaryFile()
        tmp.write(requests.get(post.images['standard_resolution'].url).content)
        img = os.popen('img2txt -W {output_size} -d fstein {fp}'.format(output_size=output_size, fp=tmp.name)).read()
        print(view.format(media=post, img=img))
        # print(os.popen('img2txt ' + tmp.name).read())


def main():
    # old_poll_feed()
    new_poll_feed()


if __name__ == '__main__':
    main()
