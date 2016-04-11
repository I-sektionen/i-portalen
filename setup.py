#!/usr/bin/env python
from setuptools import setup

setup(name='I-Portalen',
      version='0.1',
      description='I-sektionens anslagstavla tillika hemsida',
      author='Webgroup',
      author_email='webmaster@isektionen.se',
      url='http://www.i-portalen.se',
      install_requires=['django>=1.8.5,<1.8.99',
                        'PyMySQL',
                        'dj-static',
                        'markdown',
                        'django-storages-redux',
                        'boto',
                        'urllib3',
                        'django_extensions',
                        'pytz',
                        'pillow>=2.0.0',
                        'requests==2.6.0',
                        'requests-toolbelt'
                        ], # This should match requirements.txt!
      )
