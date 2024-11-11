#!/usr/bin/env python3

'''Setup script for the package.'''

# import os
from setuptools import setup

setup(
    # Name of the package
    name='testpypibiomedxtest',
    # read the version from the file release-version.txt (do not change this line)
    version=2,
    # Folders where the packages are located
    packages=['app'],
    # Author information
    author='BMX',
    author_email='gsingh@bio.mx',
    long_description_content_type='text/markdown',
    # Description of the package
    description='Test',
    license='MIT'
)
