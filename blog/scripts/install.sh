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

PROJECT=blog
USER=blog

PTH_FILE='geek-blog.pth'
if [ "$2" = "lib" ] ; then
    sudo python setup.py -q install
else
    pwd > ${PTH_FILE}
    sudo python scripts/install.py
fi

echo "Collect Static to Webfront"
pushd geekblog
python manage.py collectstatic
popd

echo Configuring ${PROJECT}...

echo Installing blog...
[ -z `grep "^$USER:" /etc/passwd` ] && sudo useradd -r $USER -M -N

chmod -R 775 /var/app/enabled/$PROJECT
chmod -R a+rw /var/app/data/$PROJECT
chmod -R a+rw /var/app/log/$PROJECT
chown $USER:nogroup /var/app/data/$PROJECT
chown $USER:nogroup /var/app/log/$PROJECT

ln -sf /var/app/enabled/$PROJECT/scripts/geek-blog-init.sh /etc/init.d/geek-blog
update-rc.d geek-blog defaults
cp /var/app/enabled/$PROJECT/scripts/geekblog.cron /etc/cron.d/geekblog
cp /var/app/enabled/$PROJECT/scripts/geekblog.logrotate /etc/logrotate.d/geekblog
