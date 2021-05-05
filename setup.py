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
    version='120',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    packages=["bot"],
    namespace_packages=["bot"],
    scripts=["bin/bot", "bin/botc", "bin/bots"],
    zip_safe=False,
    include_package_data=True,
    data_files=[('share/bot', ['files/bot.service', "files/bot.1.md"]),
                ('mods', mods("mod")),
                ('share/man/man1', ['files/bot.1.gz'])],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
