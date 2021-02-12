#!/bin/sh
docker pull 'aduvermy/groupm:0.0.1'
docker build src/.docker_modules/groupm/0.0.1 -t 'aduvermy/groupm:0.0.1'
docker push aduvermy/groupm:0.0.1
