#!/bin/sh
cd /app/server
nginx -g 'daemon off;' &
uwsgi --ini uwsgi.ini --thunder-lock --plugin python3