#!/bin/sh

if [ "$DATABASE" = "recursoshidricos" ]
then
    echo "Waiting for recursoshidricos..."

    while ! nc -z $POSTGRES_SERVER $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
# python manage.py migrate

exec "$@"