#!/bin/bash

# Run the initial migrations, creating the database
docker-compose run --rm app /bin/sh -c "cd /app; ./manage.py migrate"
docker-compose run --rm app /bin/sh -c "cd /app; ./manage.py loaddata orbit_class"

# Run the pipeline
docker-compose run --rm app /bin/bash -c "cd /app; ./data/run_pipeline.sh"

# Create an admin login
docker-compose run --rm app /bin/sh -c "cd /app; ./manage.py createsuperuser"
