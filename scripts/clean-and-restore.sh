#!/bin/sh

rm db.sqlite3
./manage.py migrate
./manage.py demo_users