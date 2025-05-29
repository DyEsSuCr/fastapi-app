#!/bin/bash

VALID_ENVS=("dev" "prod" "staging")

if [ -z "$1" ]; then
  echo "Usage: $0 [environment] [-v]"
  echo "Example: $0 dev -v"
  exit 1
fi

ENV="$1"
VOLUME_FLAG=""

if [ "$2" == "-v" ]; then
  VOLUME_FLAG="-v"
fi

if [[ ! " ${VALID_ENVS[@]} " =~ " ${ENV} " ]]; then
  echo "Invalid environment: $ENV"
  echo "Allowed values are: ${VALID_ENVS[*]}"
  exit 1
fi

ENV_FILE=".env.$ENV"

if [ ! -f "$ENV_FILE" ]; then
  echo "File $ENV_FILE not found"
  exit 1
fi

if [ "$VOLUME_FLAG" == "-v" ]; then
  echo "Stopping containers and removing volumes..."
else
  echo "Stopping containers (volumes will be preserved)..."
fi

docker compose --env-file "$ENV_FILE" down $VOLUME_FLAG

docker compose --env-file "$ENV_FILE" up -d

echo "Waiting for services to be ready..."
sleep 2

docker exec fastapi-app-web alembic upgrade head
