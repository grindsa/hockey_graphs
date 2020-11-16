#!/bin/bash
# deploy script for hockeygraphs.dynamop.deploy

BUILD_DIR='/tmp/build'
HOCKEYGRAPHS_MASTER='https://github.com/grindsa/hockey_graphs/archive/master.tar.gz'
ARCHIVE_NAME='hockey_graphs-master'
ID_FILE="$HOME/.ssh/id_ed25519"
# create temporary directory
mkdir -p $BUILD_DIR

# download archive and extract
curl -L $HOCKEYGRAPHS_MASTER --output $BUILD_DIR/$ARCHIVE_NAME.tgz
tar xvfz $BUILD_DIR/$ARCHIVE_NAME.tgz -C $BUILD_DIR

# start building image
cd $BUILD_DIR/$ARCHIVE_NAME

# build image
# docker build -f examples/Docker/build_client/Dockerfile -t build_client . --no-cache 

# start container
docker run -v $ID_FILE:/tmp/id_ed25519 --name=build_client build_client



exit 0