# This file is place in the Public Domain.

import os

from setuptools import setup

def mods(name):
    res = []
    if os.path.exists(name):
        for p in os.listdir(name):
            if p.startswith("__"):
                continue
            if p.endswith("%.py"):
                res.append(name + os.sep + p)
    return res

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='121',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthategmail.com', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    packages=["bot"],
    zip_safe=True,
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
