#!/bin/bash           
DATABASE_NAME="django_iportalen"

echo -n "Enter the sql filename [ENTER]: "
read sql_file


echo "MySQL root login"
mysql -u root -p $DATABASE_NAME << EOF < $sql_file
