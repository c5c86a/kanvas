#!/bin/sh
#

cp -R parent_unversioned_folder/media ../data/
cp parent_unversioned_folder/db.sqlite3 ../data/db

export COLLECT=True
python manage.py collectstatic --noinput
unset COLLECT

python2.7 manage.py makemigrations
python2.7 manage.py migrate
python2.7 manage.py runserver 0.0.0.0:9000         # accessible to network, not only to localhost:8085
