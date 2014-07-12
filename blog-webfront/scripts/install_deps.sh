#!/bin/bash
#
# This scripts is used to install dependencies for the application.
#
# python-software-properties depend by add-apt-repository to add nginx ppa
SYS_DEPS=( python-software-properties )

PYTHON_DEPS=( )

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
    if [ `apt-cache  search  $1  | grep -c "^i \+${1} \+"` = 0 ];then
        apt-get -y install  $1
    else
        echo "Package ${1} already installed."
    fi
}

function install_python_dep()
{
    # input args $1 like simplejson==1.0 ,can only extractly match
    if [ `pip freeze | grep -c "${1}"` = 0 ];then
        pip install  $1
    else
        echo "Python package ${1} already installed."
    fi
}

function add_nginx_repository()
{
    add-apt-repository ppa:nginx/stable
    aptitude update
}

function install_nginx()
{
    add_nginx_repository
    install_sys_dep nginx
}

install_dependencies
install_nginx
