#!/bin/sh

CURRENT=$(pwd)

cd react
yarn install && yarn build
code=$?

cd $CURRENT
exit $code