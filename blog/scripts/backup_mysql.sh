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
    sleep 5 

    gzip blog_${TODAY}.sql
    mv blog_${TODAY}.sql.gz ~/GeekBlog/backup/blog_${TODAY}.sql.gz
    echo "move sql file to git dir..."
}

function git_pull()
{
    echo "git pull...."
    cd ~/GeekBlog
    git pull
}

function git_push()
{
    git add -A
    git commit -m "backup mysql database of ${TODAY}"
    git push origin master
}

#git_pull
#backup_mysql
git_push
