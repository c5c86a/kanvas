[![Travis build status](https://travis-ci.org/nickmeet/kanvas.png?branch=master)](https://travis-ci.org/nickmeet/kanvas)

#### Manual actions

1. To rename the site, go to /admin at Sites section ("superuser with verified email" / password: maria/maria)
2. Sending email is enabled with the following instructions at the gmail of the admin:
https://support.google.com/accounts/answer/6010255

#### Getting started

git checkout db.sqlite3

git pull

pip install -r requirements.txt # at cloud9 run it with sudo

export COLLECT=True

python manage.py collectstatic --noinput

unset COLLECT

export EMAIL=True # makes emails mandatory and email verification also mandatory

python manage.py runserver 0.0.0.0:8080 # at cloud9 do not export EMAIL due to https://cloud.google.com/compute/docs/tutorials/sending-mail/

visit: https://kanvas-mariapalai.c9users.io

As the email has to be unique, for testing you can use mailinator.

cloud9 hibernates its VM after 1-2 days of inactivity

#### When modifying the models

1. python manage.py makemigrations
2. python manage.py migrate
