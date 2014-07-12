#!/bin/bash
#
# This scripts is used to install the application.
# This scripts is required for all projects.
#
SCRIPT_DIR=`dirname $0`

if [ "$1" = "checkdeps" ] ; then
	echo "Checking and installing dependecies..."
    if [ -f "${SCRIPT_DIR}/install_deps.sh" ]; then
        ${SCRIPT_DIR}/install_deps.sh
	else
		echo "Depedency install script not found."
    fi
fi

PROJECT=core

PTH_FILE='blog-core.pth'
if [ "$2" = "lib" ] ; then
    sudo python setup.py -q install
else
    pwd > ${PTH_FILE}
    sudo python scripts/install.py
fi

