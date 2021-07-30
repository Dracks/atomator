#!/bin/sh

COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_SUB=$(git log -1 --pretty=%s)
COMMIT_HASH=$(git log -1 --pretty=%H)

BRANCH="$CI_COMMIT_REF_NAME"

if [ "$BRANCH" == "" ]; then
    BRANCH=$(git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')
fi

if [ "$BRANCH" == "" ]; then
    echo "WARNING: Branch not detected"
fi


tar -czvf /tmp/package.tgz $FILES
if [  $? != 0 ]; then
    echo "Error packaging it"
    exit -1
fi

curl -F message="$COMMIT_MSG" -F hash=$COMMIT_HASH -F branch="$BRANCH" -F file=@/tmp/package.tgz $SERVER/upload_version/$TOKEN > "out.html"
if [  $? != 0 ]; then
    echo "Error pushing the package"
    exit -1
fi

out_content=$(cat out.html)
if [ "$out_content" != "Upload" ]; then
    echo "$out_content"
    exit -1
fi