#!/bin/sh

if [ "$POSTGRES_DB" = "recursoshidricos" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_SERVER $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"