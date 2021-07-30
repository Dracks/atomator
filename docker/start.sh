#!/bin/sh

# WAIT_HOSTS="$DB_HOST:3306" wait

# until mysql -h $DB_HOST -u $DB_USER -p$DB_PASS -e "show databases"; do
#    echo sleeping;
#    sleep 1;
#done;

./manage.py migrate
./manage.py runserver 0.0.0.0:8010