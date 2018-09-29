#!/usr/bin/env bash

PROJECTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )
echo $PROJECTDIR

if [[ $1 == "build" ]]; then
    docker build -t lut_tests -f tests.Dockerfile $PROJECTDIR
fi

echo "Running unit tests..."
docker run -l lut_tests_container -v $PROJECTDIR:/app lut_tests
echo "...done"

if [[ $? == 0 ]]; then
    echo "Deleting container:"
    docker rm `docker ps -qaf label=lut_tests_container`
fi