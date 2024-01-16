#!/bin/bash

# Define the path to the Docker Compose file
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Check if the Docker Compose file exists
if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
    echo "Error: Docker Compose file '$DOCKER_COMPOSE_FILE' not found."
    exit 1
fi

# Load environment variables from a file (e.g., .env)
ENV_FILE=".env"

# Check if the environment file exists
if [ -f "$ENV_FILE" ]; then
    echo "Loading environment variables from $ENV_FILE"
    export $(grep -v '^#' $ENV_FILE | xargs)
fi

# Run Docker Compose with the specified file
docker-compose -f "$DOCKER_COMPOSE_FILE" up -d