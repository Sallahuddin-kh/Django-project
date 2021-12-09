#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py makemigrations
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=123456
export DJANGO_SUPERUSER_PASSWORD
python manage.py createsuperuser --no-input --username sallahuddin --email sallahuddin@gmail.com
python manage.py test
python manage.py runserver 0.0.0.0:8000
exec "$@"
