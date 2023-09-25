#!/bin/sh

set -e

python manage.py wait_for_db
# Collect all the static files and \
# put into configured static files directory.
python manage.py collectstatic --noinput
python manage.py migrate

# Running uWSGI service passing in "socket :9000" (which runs \
# ont tcp socket on port 9000; this port will be used from \
# nginx server to connect to our app(??))
# "workers 4" sets 4 diferent WSGI workers
# "enable-threads" enables multitreading for application.
# "module app.wsgi" - specifying module. It will run \
# app/wsgi.py file. It is telling to uWSGI service that \
# this is the entry point to the our project. We will be \
# running from 'app' directory from Docker container.
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi