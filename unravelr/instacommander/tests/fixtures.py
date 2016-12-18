# -*- coding: utf-8 -*-

import os

MODULE_PATH = os.path.split(os.path.realpath(__file__))[0]


def typical_fixtures():
    # models.User.add_system_users()
    # typical_users()
    pass


def typical_picture():
    return open(os.path.join(MODULE_PATH, "data/led-hallway.jpg"), 'rb')

# def typical_users():
#     models.User.register(
#         email='joe',
#         name='Joe MacMillan',
#         password='aaa',
#         confirmed=True,
#         roles=["User"],
#     )
#     models.User.register(
#         email='cameron',
#         name='Cameron Howe',
#         password='aaa',
#         confirmed=True,
#         roles=["User"],
#     )

# # 