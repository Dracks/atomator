from python:3.8-buster

copy ./requirements.txt /tmp
run mkdir /home/django
run pip3 install -r /tmp/requirements.txt
run pip3 install psycopg2-binary
run apt update && apt install gettext -y

# run apt-get update && apt-get install -y mariadb-client && apt-get clean --dry-run

EXPOSE 8000

WORKDIR /home/django
ENTRYPOINT [ "docker/start.sh" ]