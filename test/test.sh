#!/usr/bin/env bash

set -ev

SCRIPT_DIR=$(dirname "$0")
CODE_DIR=$(cd $SCRIPT_DIR/..; pwd)

# Ensure docker socket is accessible
if [[ "$(uname)" == "Darwin" ]]; then
    DOCKER_CMD=docker
else
    DOCKER_CMD="sudo docker"
fi

# Build test container if needed
if [[ -z $($DOCKER_CMD images | grep test-container) ]] ; then
    echo "Building test container"
    $DOCKER_CMD build -t test-container $SCRIPT_DIR
fi

echo "Testing $1"
$DOCKER_CMD run \
    --rm \
    --name test \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $CODE_DIR:$CODE_DIR \
    -w $CODE_DIR \
    -e TAG=${TAG:-latest} \
    -e GOPATH=${GOPATH:-/go} \
    --network host \
    test-container \
    sh -c "export PYTHONPATH=\$PYTHONPATH:\$PWD/test ; python test/$@"