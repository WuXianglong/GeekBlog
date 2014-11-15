#!/bin/bash
#
# This scripts is used to backup mysql database. 
#

TODAY=`date +%Y%m%d`
USER_NAME=$1
PWD=$2

function backup_mysql()
{
    echo "dump mysql database..."
    mysqldump -u$USER_NAME -p$PWD --add-drop-table --routines geekblog > blog_${TODAY}.sql
    echo "mysqldump -u$USER_NAME -p$PWD --add-drop-table --routines geekblog > blog_${TODAY}.sql"
    sleep 3 

    echo "gzip sql file to git dir..."
    gzip blog_${TODAY}.sql
}

function git_push()
{
    git add -A ../..
    git commit -m "backup mysql database of ${TODAY}"
    git push origin master
}

echo "git pull...."
git pull
backup_mysql
git_push
