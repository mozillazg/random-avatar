#!/bin/sh

gunicorn_conf="`pwd`/gunicorn.py"

cd /home/www/random-avatar/


pwd

gunicorn deploy:app_wsgi -c $gunicorn_conf -D
