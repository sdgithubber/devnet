#!/bin/bash

COMMIT=$1

date=$(date +%s)
MY_TMP=~/tmp/$date/
IMAGES_DIR=~/images
mkdir -p $MY_TMP

tmpd=`mktemp -d`
pushd $tmpd
git clone git@github.com:spacemeshos/go-spacemesh.git
cd go-spacemesh
git checkout $COMMIT
go build
cp $IMAGES_DIR/Dockerfile $MY_TMP
cp go-spacemesh $MY_TMP
ls -l $MY_TMP
BUILD_CMD="sudo docker build -t node:$COMMIT $MY_TMP"
$BUILD_CMD

# cleanup
popd
rm -rf $tmpd
rm -rf $MY_TMP
