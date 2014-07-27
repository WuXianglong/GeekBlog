#!/bin/bash
#
# This scripts is used to stop the application.
#

sudo service nginx stop
# remove nginx  cache
sudo rm -rf /var/lib/nginx/cache
