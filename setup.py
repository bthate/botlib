from setuptools import setup

def readme():
    with open('README') as file:
        return file.read()

setup(
    name='botlib',
    version='72',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots (a botlib).",
    long_description=readme(),
    license='Public Domain',
    zip_safe=True,
    packages=["botlib"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
