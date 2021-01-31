#!/usr/bin/env python
from setuptools import setup

setup(name='I-Portalen',
      version='1.1.2',
      description='I-sektionens anslagstavla tillika hemsida',
      author='Webgroup',
      author_email='webmaster@isektionen.se',
      url='http://www.i-portalen.se',
      install_requires=[
          'Django==1.11.29',
          'PyMySQL',
          'boto==2.42.0',
          'coverage==4.2',
          'dj-static==0.0.6',
          'django-cors-headers==1.1.0',
          'django-debug-toolbar==1.5',
          'django-extensions==1.7.4',
          'django-filter==0.15.0',
          'django-nose==1.4.4',
          'django-storages-redux==1.3.2',
          'djangorestframework==3.3.2',
          'Markdown==2.6.6',
          'pillow',
          'pytz==2016.6.1',
          'requests==2.6.0',
          'requests-toolbelt==0.7.0',
          'django-reversion==2.0.0',
          'sqlparse==0.2.1',
          'urllib3',
          'django-autocomplete-light'],  # This should match requirements.txt!
      )
