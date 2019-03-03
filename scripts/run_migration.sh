#!/bin/bash

# Run new migrations
docker-compose run --rm app /bin/sh -c "cd /app && ./manage.py migrate && ./manage.py loaddata orbit_class"
