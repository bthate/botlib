# This file is place in the Public Domain.

import os

from setuptools import setup

def mods(name):
    res = []
    if os.path.exists(name):
        for p in os.listdir(name):
            if p.startswith("__"):
                continue
            if p.endswith(".py"):
                res.append(p[:-3])
    return res

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='120',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    package_dir={"": "bot"},
    py_modules=mods("bot"),
    scripts=["bin/bot", "bin/botc", "bin/bots"],
    data_files=[('share/bot', ['files/bot.service', "files/bot.1.md"]),
                ('share/man/man1', ['files/bot.1.gz'])],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
