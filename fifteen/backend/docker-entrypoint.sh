#!/bin/bash -x
echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done
echo "PostgreSQL started"
python3 manage.py db upgrade || exit 1
exec "$@"