#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    #os.chdir('..')  #this will make the python interpreter see iportalen_django.iportalen_django when running tests.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iportalen_django.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
