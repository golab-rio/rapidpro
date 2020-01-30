#!/bin/bash
set -e

case $1 in
    start)
        python3.6 manage.py compress --extension=.haml --force
        python3.6 clear-compressor-cache.py
        python3.6 manage.py migrate --noinput
        cat nginx.conf > /etc/nginx/sites-enabled/nginx.conf
        /usr/local/bin/supervisord -n -c supervisor-app.conf
    ;;

esac

exec "$@"
