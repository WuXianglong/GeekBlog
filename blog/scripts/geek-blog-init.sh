#!/bin/bash
#
# Geek blog init script
# 
### BEGIN INIT INFO
# Provides:          geek-blog
# Required-Start:    $remote_fs $remote_fs $network $syslog
# Required-Stop:     $remote_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start geek blog Web Site Data at boot time
# Description:       geek blog Web Site Data provides web server backend.
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/var/app/enabled/blog
NAME=geek-blog
DESC="geek blog server"
PROJECT=blog
APP_DIR=/var/app/enabled/$PROJECT
LOG_DIR=/var/app/log/$PROJECT
PID_FILE=/var/run/$NAME.pid


if [ -f /etc/default/$NAME ]; then
	. /etc/default/$NAME
fi

set -e

. /lib/lsb/init-functions

function stop_blog()
{
	if [ -f "${PID_FILE}" ]; then
	    uwsgi --stop ${PID_FILE}
	    rm ${PID_FILE}
	else
	    echo "${NAME} stop/waiting."
	fi
}

function start_blog()
{
	if [ -f "$PID_FILE" ]; then
		echo "$NAME is already running."
	else
	    pushd ${APP_DIR} >/dev/null
	    uwsgi --pidfile=${PID_FILE} -x uwsgi.xml --uid blog --gid nogroup
	    popd >/dev/null	
	fi
}

function reload_blog()
{
	if [ ! -f "$PID_FILE" ]; then
        start_blog
	else
	    pushd ${APP_DIR} >/dev/null
	    uwsgi --reload ${PID_FILE}
	    popd >/dev/null	
	fi
}

case "$1" in
	start)
		echo -n "Starting $DESC..."
		start_blog
		echo "Done."				
		;;
	stop)
		echo -n "Stopping $DESC..."
		stop_blog
		echo "Done."
		;;
	restart)
		echo -n "Restarting $DESC..."
		stop_blog
		sleep 3
		start_blog
		echo "Done."
		;;
	reload)
		echo -n "Rereloading $DESC..."
		reload_blog
		echo "Done."
		;;
	status)
		status_of_proc -p $PID_FILE "$DAEMON" uwsgi && exit 0 || exit $?
		;;
	*)
		echo "Usage: $NAME {start|stop|restart|reload|status}" >&2
		exit 1
		;;
esac

exit 0
