# This file is place in the Public Domain.

import os

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='118',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    packages=["bot"],
    namespace_packages=["bot"],
    zip_safe=False,
    scripts=["bin/bot", "bin/botctl", "bin/botd"],
    include_package_data=False,
    data_files=[('share/bot', ['botd.service']),
                ('share/man/man1', ['man/bot.1.gz']),
                ('share/man/man8', ['man/botctl.8.gz', 'man/botd.8.gz'])],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
