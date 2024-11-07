#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Hstong, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import dirname, join

from setuptools import (
    find_packages,
    setup,
)

with open(join(dirname(__file__), 'hs/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

install_requires = ["protobuf==3.13.0",
                    "PyCryptodome==3.10.1",
                    "netifaces==0.11.0",
                    "psutil==5.9.0",
                    "python-snappy==0.6.1"]

setup(
    name='py-sahm-openapi',
    version=version,
    description='Sham Quantitative Trading/Quote API',
    classifiers=[],
    keywords='Sham SA/US Stock Quant Trading/Quote API',
    author='Sham, Inc.',
    author_email='',
    url='',
    license='Apache License 2.0',
    packages=find_packages(exclude=[]),
    package_data={'': ['*.*']},
    include_package_data=True,
    install_requires=install_requires
)
