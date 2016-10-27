#!/usr/bin/env python
from setuptools import setup

setup(name='I-Portalen',
      version='1.0',
      description='I-sektionens anslagstavla tillika hemsida',
      author='Webgroup',
      author_email='webmaster@isektionen.se',
      url='http://www.i-portalen.se',
      install_requires=['django>=1.8.5,<1.8.99',
                        'PyMySQL',
                        'dj-static==0.0.6',
                        'markdown==2.6.6',
                        'django-storages==1.5.1',
                        'boto==2.42.0',
                        'urllib3==1.16',
                        'django_extensions==1.7.2',
                        'pytz==2016.6.1',
                        'pillow>=2.0.0',
                        'requests==2.6.0',
                        'requests-toolbelt==0.7.0',
                        'django-nose==1.4.4',
                        'coverage=4.2',
                        'django-filter==0.14.0',
                        'django-debug-toolbar=1.5',
                        'djangorestframework==3.3.2',
                        'django-cors-headers==1.1.0',
                        'reversion==0.2'],  # This should match requirements.txt!
      )
