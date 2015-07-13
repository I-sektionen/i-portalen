#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    """
    This part here imports pymysql and uses it instead of MySQLdb which is not proted to python3 yet.

    It might cause problems with advanced mysql-operations.

    The same trick is done in the application.py.

    //Isac
    """
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
    #os.chdir('iportalen_django/')  #this will make the python interpreter see iportalen_django.iportalen_django when running tests.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iportalen.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
