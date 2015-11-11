#!/usr/bin/env bash

echo 'MySQL root login'
mysql -u root -p << EOF

DROP DATABASE IF EXISTS django_iportalen;
CREATE DATABASE django_iportalen CHARACTER SET UTF8;

EOF