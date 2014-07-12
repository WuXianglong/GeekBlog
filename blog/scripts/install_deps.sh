#!/bin/bash
#
# This scripts is used to install dependencies for the application.
#
# python-software-properties depend by add-apt-repository to add nginx ppa
SYS_DEPS=(python-pip python-software-properties python2.7-dev libxml2-dev python-mysqldb libjpeg8-dev)

PYTHON_DEPS=("django==1.5.2" "uwsgi==1.0.4" PIL "pymongo==2.4.1" PyJWT)

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

function install_java(){
    sudo add-apt-repository ppa:sun-java-community-team/sun-java6
    sudo apt-get update
    sudo apt-get install sun-java6-jdk
}

# http://stackoverflow.com/questions/16263556/installing-java-7-on-ubuntu
function install_java7(){
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java7-installer
    sudo apt-get install oracle-java7-set-default
}

function install_mongodb(){
    sudo sh -c "echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' >> /etc/apt/sources.list"
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    sudo apt-get update
    sudo apt-get install mongodb-10gen
}

install_dependencies
install_java
install_mongodb
