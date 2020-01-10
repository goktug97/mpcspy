#!/usr/bin/env python

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='mpcspy',
      version='0.0.4',
      description='My Personal Configuration System for Python',
      author='Göktuğ Karakaşlı',
      author_email='karakasligk@gmail.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/goktug97/mpcspy',
      download_url=('https://github.com/goktug97/mpcspy/archive/v0.0.4.tar.gz'),
      packages=['mpcspy'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License"
      ],
      install_requires=[],
      python_requires='>=3.6',
      include_package_data=True)
