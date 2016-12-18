# -*- coding: utf-8 -*-

from setuptools import setup
import os

version = '0.1'


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


setup(version=version,
    name='InstaCommander',
    description="Prototype Terminal client for Instagram.",
    author='Michael Sarfati',
    author_email="michael.sarfati@utoronto.ca",
    packages=[
        "instacommander",
        "instacommander.tests",
        "instacommander.utils",
    ],
    scripts=[
    ],
    long_description="""""",
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    include_package_data=True,
    keywords='',
    install_requires=read('requirements.txt'),

    zip_safe=False,
)
