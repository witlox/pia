#!/usr/bin/env python
# -*- coding: utf-8 -*-#

# Copyright (c) 2021 Pim Witlox
#
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from setuptools import setup

version = "0.1.1"

requirements = ['aiofiles',
                '']

test_requirements = ['pytest', 'tox']

if sys.argv[-1] == "tag":
    os.system("git tag -a {0} -m 'version {1}'".format(version, version))
    os.system("git push origin master --tags")
    sys.exit()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "test":
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        raise ImportError("{0} is not installed. Install your test requirements.".format(
            str(e).replace("No module named ", ""))
        )
    os.system('py.test')
    sys.exit()

setup(name="pia",
      version=version,
      description="Personal Information Assesor",
      long_description=open("README.md").read(),
      author="Pim Witlox",
      author_email="pim@witlox.io",
      url="https://github.com/witlox/pia",
      license="MIT",
      entry_points={
          "console_scripts": [
              "pia = pia.application:main",
          ]
      },
      packages=[
          "pia"
      ],
      include_package_data=True,
      install_requires=requirements,
      python_requires=">=3.7",
      keywords="Python, Python3",
      project_urls={
          "Documentation": "https://pia.readthedocs.io/en/latest/",
          "Source": "https://github.com/witlox/pia",
          "Tracker": "https://github.com/witlox/pia/issues",
      },
      test_suite="tests",
      tests_require=test_requirements,
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: System Administrators",
                   "Natural Language :: English",
                   "Environment :: Console",
                   "License :: OSI Approved :: GPLv3 License",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.7",
                   "Topic :: Software Development :: Libraries",
                   "Topic :: Utilities"],
      )
