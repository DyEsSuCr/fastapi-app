# start_app.sh - Deployment Script

Script to deploy the application in different environments using Docker Compose with proper health checks and dependency management.

## Prerequisites

- Docker and Docker Compose installed (automatically checked by the script)
- Environment configuration files (`.env.dev`, `.env.prod`, `.env.staging`)
- Script must have execution permissions
- Docker containers with health checks configured:
  - `fastapi-app-db` (database container)
  - `fastapi-app-redis` (Redis container)
  - `fastapi-app-web` (web application container)

## Usage

```bash
./start_app.sh -e [environment] [-v]
```

### Parameters

- **-e environment**: Deployment environment (required)
  - `dev` - Development environment
  - `prod` - Production environment  
  - `staging` - Staging environment
- **-v**: Optional flag to remove volumes during shutdown

### Examples

```bash
# Deploy to development (preserving volumes)
./start_app.sh -e dev

# Deploy to production with complete volume cleanup
./start_app.sh -e prod -v

# Deploy to staging
./start_app.sh -e staging
```

## What does the script do?

1. **Prerequisites Check**: Automatically verifies Docker and Docker Compose are installed
2. **Parameter Parsing**: Uses proper getopt parsing for command-line arguments
3. **Environment Validation**: Verifies that the environment is valid and the corresponding `.env` file exists
4. **Container Management**: Stops existing containers (with or without volume removal)
5. **Service Startup**: Starts all services using Docker Compose
6. **Health Checks**: Waits for database and Redis services to become healthy before proceeding
7. **Database Migrations**: Executes Alembic migrations once all dependencies are ready
8. **Completion**: Provides clear status messages with emojis for better visibility

## Required Environment Files

The script automatically looks for these files based on the environment:

- `.env.dev` - For development environment
- `.env.prod` - For production environment
- `.env.staging` - For staging environment

## Container Dependencies

The script expects these containers with health checks:

- **fastapi-app-db**: Database container (must have health check configured)
- **fastapi-app-redis**: Redis container (must have health check configured)  
- **fastapi-app-web**: Web application container (for running migrations)

## Initial Setup

1. Give execution permissions to the script:
```bash
chmod +x start_app.sh
```

2. Make sure the necessary environment files exist in the project root directory.

3. Ensure your `docker-compose.yml` includes health checks for database and Redis services.

## Health Check Configuration

Your `docker-compose.yml` should include health checks like:

```yaml
services:
  db:
    container_name: fastapi-app-db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U your_user"]
      interval: 10s
      timeout: 5s
      retries: 5
      
  redis:
    container_name: fastapi-app-redis
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## Script Features

- **Robust Error Handling**: Fails fast with clear error messages
- **Visual Feedback**: Uses emojis and clear status messages
- **Smart Waiting**: Waits for actual health checks instead of arbitrary timeouts
- **Dependency Management**: Ensures database and Redis are ready before migrations
- **Flexible Options**: Supports volume cleanup and multiple environments

## Troubleshooting

- **❌ Docker is not installed**: Install Docker and Docker Compose
- **❌ File .env.X not found**: Create the corresponding environment file
- **❌ Invalid environment**: Use only `dev`, `prod` or `staging`
- **❌ Failed to run Alembic migrations**: 
  - Check that `fastapi-app-web` container is running
  - Verify Alembic configuration
  - Ensure database connection is properly configured
- **Health check timeouts**: 
  - Verify health check configuration in docker-compose.yml
  - Check container logs for startup issues
  - Ensure database/Redis services are properly configured