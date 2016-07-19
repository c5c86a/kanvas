#!/bin/sh
#

python2.7 manage.py makemigrations
python2.7 manage.py migrate
python2.7 manage.py runserver 0.0.0.0:8085         # accessible to network, not only to localhost:8085
