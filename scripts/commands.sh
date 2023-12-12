#!/bin/sh

set -e

wait_postgresql.sh
collectstatic.sh
makemigrations.sh
migrate.sh
runserver.sh
