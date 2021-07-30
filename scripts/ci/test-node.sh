#!/bin/sh

CURRENT=$(pwd)

cd react
yarn prettier:ts:check
formatter_code=$?

yarn lint
lint_code=$?

yarn test
test_code=$?

cd $CURRENT
if [ $formatter_code -ne 0 ] || [ $test_code -ne 0 ] || [ $lint_code -ne 0 ]; then
    exit 1
fi