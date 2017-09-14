#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('warlok')


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'gitpython==2.1.5',
    'click==6.7',
    'colorama==0.3.9',
]

test_requirements = []

setup(
    name='warlok',
    version=version,
    description="An evil cousin of Arcanist",
    long_description=readme + '\n\n' + history,
    author="Julius Seporaitis",
    author_email='julius@seporaitis.net',
    url='https://github.com/seporaitis/warlok',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_dir={
        'warlok': 'warlok',
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='python',
    entry_points={
        'console_scripts': [
            'wlk=warlok.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
