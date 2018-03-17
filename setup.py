#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'Scrapy>=1.5.0', 'scrapy-djangoitem==1.1.1', 'python-decouple==3.1',
                'scrapy-djangoitem>=1.1.1', 'flower>=0.9.2', 'Django>=2.0.1',
                'django-bootstrap-breadcrumbs>=0.9.0', 'django-celery-beat>=1.1.0',
                'django-multiselectfield>=0.1.8', 'celery>=4.1.0']

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
