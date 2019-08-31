#!/bin/bash

# Run the pipeline
time docker-compose run --rm app /bin/bash -c "cd /app; ./data/run_pipeline.sh"
