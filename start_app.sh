#!/bin/bash

VALID_ENVS=("dev" "prod" "staging")
VOLUME_FLAG=""
ENV=""

usage() {
  echo "Usage: $0 -e [environment] [-v]"
  echo "Example: $0 -e dev -v"
  exit 1
}

# Check for required commands
command -v docker >/dev/null 2>&1 || { echo >&2 "❌ Docker is not installed."; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo >&2 "❌ 'docker compose' is not available."; exit 1; }

# Parse options
while getopts ":e:v" opt; do
  case ${opt} in
    e )
      ENV=$OPTARG
      ;;
    v )
      VOLUME_FLAG="-v"
      ;;
    \? )
      usage
      ;;
  esac
done

if [[ -z "$ENV" ]]; then
  usage
fi

# Validate environment
if [[ ! " ${VALID_ENVS[@]} " =~ " ${ENV} " ]]; then
  echo "❌ Invalid environment: $ENV"
  echo "Allowed values are: ${VALID_ENVS[*]}"
  exit 1
fi

ENV_FILE=".env.$ENV"

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ File $ENV_FILE not found"
  exit 1
fi

echo "📦 Using environment file: $ENV_FILE"

if [ "$VOLUME_FLAG" == "-v" ]; then
  echo "🧹 Stopping containers and removing volumes..."
else
  echo "📁 Stopping containers (volumes will be preserved)..."
fi

docker compose --env-file "$ENV_FILE" down $VOLUME_FLAG
docker compose --env-file "$ENV_FILE" up -d

# Wait for the database service to become healthy
echo "⏳ Waiting for the database to be ready..."

until [ "$(docker inspect --format='{{.State.Health.Status}}' fastapi-app-db 2>/dev/null)" == "healthy" ]; do
  echo "⏳ DB is not ready yet, waiting..."
  sleep 2
done

echo "✅ Database is ready."


# Wait for Redis to become healthy
echo "⏳ Waiting for Redis to be ready..."
until [ "$(docker inspect --format='{{.State.Health.Status}}' fastapi-app-redis 2>/dev/null)" == "healthy" ]; do
  echo "⏳ Redis is not ready yet, waiting..."
  sleep 2
done

echo "✅ Redis is ready."


# Run Alembic migrations
echo "🚀 Running Alembic migrations..."
if ! docker exec fastapi-app-web alembic upgrade head; then
  echo "❌ Failed to run Alembic migrations"
  exit 1
fi

echo "✅ Deployment completed for environment '$ENV'"
