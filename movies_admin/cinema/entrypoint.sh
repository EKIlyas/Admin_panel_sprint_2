#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "waiting for postgres..."

  while  ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
  done

  echo "postgres started"
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear
django-admin compilemessages

exec "$@"
