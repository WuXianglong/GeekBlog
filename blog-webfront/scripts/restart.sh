#!/bin/sh

if [ -f "/var/run/nginx.pid" ]; then
    # remove nginx  cache
    sudo rm -fr /var/lib/nginx/cache
	sudo service nginx reload
else
    # remove nginx  cache
    sudo rm -fr /var/lib/nginx/cache
	sudo service nginx start
fi
