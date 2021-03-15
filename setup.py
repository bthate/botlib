# BOTLIB - pure python3 bot library
#
# this file is place in the public domain

"library to program bots"

import os

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='117',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="pure python3 bot library",
    long_description=read(),
    license='Public Domain',
    packages=["bot", "bot.cmd"],
    zip_safe=True,
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
