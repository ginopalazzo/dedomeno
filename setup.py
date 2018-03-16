from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys
import re

import dedomeno

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


LONG_DESCRIPTION = read('README.md')

setup(
    setup_requires=['pytest-runner'],
    name='dedomeno',
    version='0.1',
    url='http://github.com/ginopalazzo/dedomeno/',
    license='GNU General Public License v3.0',
    author='Gino Palazzo',
    tests_require=['pytest'],
    install_requires=['Django>=2.0.1',
                      'Scrapy==1.5.0',
                      'celery>=4.1.0',
                      'django-bootstrap-breadcrumbs>=0.9.0',
                      'django-celery-beat>=1.1.<0',
                      'django-multiselectfield>=0.1.8',
                      'fake-useragent>=0.1.8',
                      'flower>=0.9.2',
                      'python-decouple>=3.1',
                      'scrapy-djangoitem>=1.1.1',
                      ],

    author_email='ginopalazzo@gmail.com',
    description='A Spanish real estate (Idealista) python scraper',
    long_description=LONG_DESCRIPTION,
    packages=['dedomeno'],
    include_package_data=True,
    platforms='any',
    test_suite='dedomeno.test',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Alfa',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)