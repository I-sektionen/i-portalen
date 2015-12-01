#!/usr/bin/env python
from setuptools import setup

setup(name='I-Portalen',
      version='0.1',
      description='I-sektionens anslagstavla tillika hemsida',
      author='Webgroup',
      author_email='webmaster@isektionen.se',
      url='http://www.i-portalen.se',
      install_requires=['Django>=1.8.5,<1.8.99',
                        'PyMySQL',
                        'dj-static',
                        'django-reversion',
                        'markdown',
                        'django-storages-redux',
                        'boto',
                        'urllib3',
                        'django_extensions',
                        'pytz'],  # This should match requirements.txt!
      )
