#!/bin/bash
# deploy script for hockeygraphs.dynamop.deploy

BUILD_DIR='/tmp/build'
ID_FILE="$HOME/.ssh/id_ed25519"

# HOCKEYGRAPHS_MASTER='https://github.com/grindsa/hockey_graphs/archive/master.tar.gz'
HOCKEYGRAPHS_MASTER='https://github.com/grindsa/hockey_graphs'
ARCHIVE_NAME='hockey_graphs-master'
CONTAINER_NAME='build_client'


# create temporary directory
mkdir -p $BUILD_DIR

# download archive and extract
# curl -L $HOCKEYGRAPHS_MASTER --output $BUILD_DIR/$ARCHIVE_NAME.tgz
# tar xvfz $BUILD_DIR/$ARCHIVE_NAME.tgz -C $BUILD_DIR
git clone $HOCKEYGRAPHS_MASTER $BUILD_DIR/$ARCHIVE_NAME

# start building image
cd $BUILD_DIR/$ARCHIVE_NAME

# build image
docker build -f examples/Docker/build_client/Dockerfile -t build_client . --no-cache

# start container
docker run -v $ID_FILE:/tmp/id_ed25519 --name=build_client build_client deploy

# cleanup
# stop and remove container
docker container stop build_client
docker container rm build_client
# remove image
docker image rm build_client

# remove build directory
rm -rf $BUILD_DIR


exit 0
