#!/bin/sh

SCRIPT_DIR=`dirname $0`
${SCRIPT_DIR}/stop.sh
sleep 3
${SCRIPT_DIR}/start.sh
