# -*- coding: utf-8 -*-
# ===========================
# Setup file
# ===========================

import re
from setuptools import setup, find_packages


version = re.search(r'__version__\s*=\s*"(.+)"', open('activeiq/__init__.py', 'rt').read()).group(1)

with open('README.md') as f:
    long_description = f.read()
    
setuptools.setup(
    name="activeiq",
    version=version,
    author="Wouter Coppens",
    author_email="wouter.coppens@gmail.com",
    description="This package allows to consume the ActiveIQ API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woutercoppens/activeiq-sdk",
    packages=find_packages(exclude=['samples']),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'requests',
        'six'
    ],
    python_requires='>=3.5',
)
