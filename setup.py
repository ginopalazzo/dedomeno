#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Gino Palazzo",
    author_email='ginopalazzo@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A Spanish real estate (Idealista) python scraper",
    entry_points={
        'console_scripts': [
            'dedomeno=dedomeno.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dedomeno',
    name='dedomeno',
    packages=find_packages(include=['dedomeno']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ginopalazzo/dedomeno',
    version='0.1.0',
    zip_safe=False,
)

# Config file for automatic testing at travis-ci.org

language: python
python:
  - 3.6
  - 3.5
  - 3.4
  - 2.7

# Command to install dependencies, e.g. pip install -r requirements.txt --use-mirrors
install: pip install -U tox-travis

# Command to run tests, e.g. python setup.py test
script: tox

# Assuming you have installed the travis-ci CLI tool, after you
# create the Github repo and add it to Travis, run the
# following command to finish PyPI deployment setup:
# $ travis encrypt --add deploy.password
deploy:
  provider: pypi
  distributions: sdist bdist_wheel
  user: ginopalazzo
  password:
    secure: PLEASE_REPLACE_ME
  on:
    tags: true
    repo: ginopalazzo/dedomeno
    python: 3.6