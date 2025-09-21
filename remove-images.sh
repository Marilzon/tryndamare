#!/bin/sh

docker compose down -v;
docker rm -vf $(docker ps -aq);
docker rmi -f $(docker images -aq);

