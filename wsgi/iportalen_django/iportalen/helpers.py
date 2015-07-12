__author__ = 'isac'

import os
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'mysql_credentials')

def get_mysql_credentials():
    with open(file_path, 'r') as f:
        mysql_credentials = {}
        for line in f:
            fields = line.strip().split()
            mysql_credentials[fields[0]] = fields[1]
        return mysql_credentials