#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Prototype for InstaCommander
import sys
import os
sys.path.insert(0, '.')
MODULE_PATH = os.path.split(os.path.realpath(__file__))[0]

import requests
from io import BytesIO
from instacommander.images import ANSIImage
from instacommander import renderers
import time

username = "instagram" if len(sys.argv) < 2 else sys.argv[1]

# TODO: Comments, rendering user profile pictures
view = """\
--------
{full_name} ( {username} )
{img}
{created_time}
{caption}
{link}
Likes: {like_count}
\n
"""

get_tty_width = lambda: int(os.popen('stty size').read().split()[1])
# output_size = round(get_tty_width() / 1.15)  # Leaves a margin
width = get_tty_width()

client = requests.get("https://www.instagram.com/{username}/media".format(username=username))
feed = [i for i in client.json()['items'] if i['type'] == 'image']
# import ipdb; ipdb.sset_trace()


def ansi_feed():
    feed = [i for i in client.media_popular() if i.type == 'image']  # Filter for only images
    for post in feed:
        img = BytesIO(requests.get(post.images['standard_resolution'].url).content)
        img = ANSIImage(img, width)
        # img = A(img, output_size)
        print(view.format(media=post, img=img.stream))


def make_payload(post):
    """
    Creates a payload for the view function.

    :returns: A dict
    """
    payload = {
        "created_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(post['created_time']))),

        "caption": post['caption']['text'],

        "full_name": post['user']['full_name'],

        # Post's link
        "link": post['link'],

        "like_count": post['likes']['count'],

        "username": post['user']['username'],
    }
    return payload


def ascii_feed():
    for post in feed:
        # import ipdb; ipdb.sset_trace()
        img = BytesIO(requests.get(post['images']['standard_resolution']['url']).content)
        img = renderers.to_ascii(img, width)
        payload = make_payload(post)
        print(view.format(img=img, **payload))


def main():
    # pass
    # ansi_feed()
    ascii_feed()


if __name__ == '__main__':
    main()
