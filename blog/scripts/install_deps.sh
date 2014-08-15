#!/bin/bash
#
# This scripts is used to install dependencies for the application.
#
# python-software-properties depend by add-apt-repository to add nginx ppa
SYS_DEPS=(mysql-server mysql-client python-pip python-software-properties python2.7-dev libxml2-dev python-mysqldb libjpeg8-dev libmemcached-dev memcached python-memcache)

PYTHON_DEPS=("django==1.6.5" "pymongo==2.4.1" PIL PyJWT django-pipeline)

function install_dependencies()
{
   # update to latest to avoid some packages can not found.
   apt-get update
   echo "Installing required system packages..."
   for sys_dep in ${SYS_DEPS[@]};do
       install_sys_dep $sys_dep
   done
   echo "Installing required system packages finished."

   echo "Installing required python packages..."
   for python_dep in ${PYTHON_DEPS[@]};do
       install_python_dep ${python_dep}
   done
   echo "Installing required python packages finished."
   # install PIL in ubuntu 14.04: pip install PIL --allow-external PIL --allow-unverified PIL
}

function install_sys_dep()
{
    # input args  $1 package name
    if [ `apt-cache  search  $1 | grep -c "^i \+${1} \+"` = 0 ];then
        apt-get -y install $1
    else
        echo "Package ${1} already installed."
    fi
}

function install_python_dep()
{
    # input args $1 like simplejson==1.0 ,can only extractly match
    if [ `pip freeze | grep -c "${1}"` = 0 ];then
        pip install $1
    else
        echo "Python package ${1} already installed."
    fi
}

# http://stackoverflow.com/questions/16263556/installing-java-7-on-ubuntu
function install_java(){
    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    # sudo apt-get install oracle-java6-installer
    # sudo apt-get install oracle-java7-installer
    sudo apt-get install oracle-java8-installer
}

function install_mongodb(){
    sudo sh -c "echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' >> /etc/apt/sources.list"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    sudo apt-get update
    sudo apt-get install mongodb-10gen
}

function install_uwsgi(){
    wget http://projects.unbit.it/downloads/uwsgi-1.0.4.tar.gz
    tar xvf uwsgi-1.0.4.tar.gz
    cd uwsgi-1.0.4
    sudo python setup.py install
}

# install yuglify for using django-pipeline
function install_yuglify(){
    # ln -s /usr/bin/nodejs /usr/bin/node
    sudo apt-get install npm
    sudo npm config set registry http://registry.npmjs.org/
    sudo npm -g install yuglify
}

install_dependencies
install_uwsgi
install_java
install_mongodb
install_yuglify
