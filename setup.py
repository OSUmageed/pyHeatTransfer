
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import subprocess as sp
import shlex

here = path.abspath(path.dirname(__file__))

setup(
    name = 'pyHeatTransfer',
    version = '0.1.11',

    description = 'Heat Transfer Library v0.1 includes GUI and nacent materials database.',
    long_description = 'The GUI launches a simulation that computes temperature of 3D solid in environment with finite difference scheme returns contour plot on plane.',

    author = 'Daniel J Magee',
    url = 'https://github.com/OSUmageed/pyHeatTransfer',
    author_email = 'mageed@oregonstate.edu',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        "Natural Language :: English",
        'Operating System :: Unix',


        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords = 'heat transfer engineering education',
    packages = find_packages(),

    install_requires = [
        'nose', 
        'numpy', 
        'kivy', 
        'CoolProp', 
        'matplotlib', 
        'deco',
        'pygame'],

    package_data = {
        'pyHeatTransfer': ['*.kv'],
        'SolidProp': ["PropData/*.json"],},

    entry_points = {
        'console_scripts': [
            'heatRun=pyHeatTransfer:main',
        ],
    },
)

strs = "garden install graph"
execs = shlex.split(strs)
proc = sp.Popen(execs)
sp.Popen.wait(proc)
