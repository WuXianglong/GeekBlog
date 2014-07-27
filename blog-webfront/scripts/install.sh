#!/bin/bash
#
# This scripts is used to install the application.
# This scripts is required for all projects.
#
#python setup.py -q build

SCRIPT_DIR=`dirname $0`

PROJECT=blog-webfront

if [ ! -d "/var/app/log/$PROJECT" ]; then mkdir -p /var/app/log/$PROJECT; fi

if [ "$1" = "checkdeps" ] ; then

    if [ -f "${SCRIPT_DIR}/install_deps.sh" ]; then
        ${SCRIPT_DIR}/install_deps.sh
    fi
    
    shift 
fi 

if [ -f "${SCRIPT_DIR}/setup_conf.sh" ]; then
    ${SCRIPT_DIR}/setup_conf.sh
fi
