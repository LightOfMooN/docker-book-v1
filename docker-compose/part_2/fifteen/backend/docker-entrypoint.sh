#!/bin/bash
if [ ! -z  "$DB_HOST" ]
then
  echo "Waiting for database"
  DB_PORT="${DB_PORT:-5432}"
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.5
  done
  echo "Database started"
  flask db upgrade || exit 1
fi
exec "$@"
