#!/bin/sh
chmod 777 -R /app/_file
cd /app/server
nginx -g 'daemon off;' &
uwsgi --ini uwsgi.ini --thunder-lock --plugin python3