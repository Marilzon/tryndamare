#!/bin/sh

docker exec -it tryndamare-target_postgres-1 psql -U postgres -d target_db

# \dt - show tables
