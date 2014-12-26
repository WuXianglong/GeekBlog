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
    tar -zcf - blog_${TODAY}.sql |openssl des3 -salt -k ${PWD}_${TODAY} | dd of=test.des3
    rm blog_${TODAY}.sql
    # 解密:dd if=test.des3 |openssl des3 -d -k password | tar zxf -
}

function git_push()
{
    git add -A ../..
    git commit -m "backup mysql database of ${TODAY}"
    git push origin master
}

echo "git pull...."
git pull
rm test.des3
backup_mysql
git_push
