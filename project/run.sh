#!/bin/bash

echo "Removing xpra container"
docker rm -f xpra
echo "Rebuilding xpra container"
docker build -t xpra-container -f Dockerfile-xpra .
docker run -d -p 14500:14500 --name xpra xpra-container
