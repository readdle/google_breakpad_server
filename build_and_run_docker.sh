#!/bin/bash
PORT=4000


echo "Building docker..."
docker build ./docker -t crashserver


echo "Starting server on port ${PORT}"
docker run --restart=always -d -p ${PORT}:8003 crashserver

