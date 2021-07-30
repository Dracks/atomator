from node:12-buster

copy ./react/package.json /home/django/react/package.json
workdir /home/django/react
run yarn install; rm package.json


entrypoint [ "yarn", "build:watch"]