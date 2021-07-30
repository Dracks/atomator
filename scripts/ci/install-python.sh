#!/bin/sh

apt-get update
apt-get install -y virtualenv
virtualenv -p python3 venv

venv/bin/pip install -r requirements.txt
venv/bin/pip install -r requirements_lint.txt