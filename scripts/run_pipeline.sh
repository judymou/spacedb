#!/bin/bash

# Run the pipeline
docker-compose run --rm app /bin/bash -c "cd /app; ./data/run_pipeline.sh"
