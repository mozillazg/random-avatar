#!/bin/sh

cd ../random-avatar/

git pull

pip install -r requirements.txt

cd ../random-avatar-conf/


chown www-data:www-data /home/www -R



./stop.sh
./start.sh
