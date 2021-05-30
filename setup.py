# This file is place in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='123',
    url='https://github.com/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="python3 bot library",
    long_description=read(),
    license='Public Domain',
    packages=["bot"],
    zip_safe=True,
    include_package_data=False,
    data_files=[('share/botd/', ['files/bot.1.md',
                                    'files/botctl.8.md',
                                    'files/botd.8.md',
                                    'files/botd.service',
                                    'files/botd'])],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
