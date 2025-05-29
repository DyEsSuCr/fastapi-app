# start_app.sh - Deployment Script

Script to deploy the application in different environments using Docker Compose.

## Prerequisites

- Docker and Docker Compose installed
- Environment configuration files (`.env.dev`, `.env.prod`, `.env.staging`)
- Script must have execution permissions

## Usage

```bash
./start_app.sh [environment] [-v]
```

### Parameters

- **environment**: Deployment environment (required)
  - `dev` - Development environment
  - `prod` - Production environment  
  - `staging` - Staging environment
- **-v**: Optional flag to remove volumes (optional)

### Examples

```bash
# Deploy to development (preserving volumes)
./start_app.sh dev

# Deploy to production with complete volume cleanup
./start_app.sh prod -v

# Deploy to staging
./start_app.sh staging
```

## What does the script do?

1. **Validation**: Verifies that the environment is valid and the corresponding `.env` file exists
2. **Stop containers**: Runs `docker compose down` (with or without `-v` as specified)
3. **Start containers**: Runs `docker compose up -d` with the corresponding environment file
4. **Wait**: Pauses for 2 seconds to let services get ready
5. **Migrations**: Executes database migrations with Alembic

## Required Environment Files

The script automatically looks for these files based on the environment:

- `.env.dev` - For development environment
- `.env.prod` - For production environment
- `.env.staging` - For staging environment

## Initial Setup

1. Give execution permissions to the script:
```bash
chmod +x start_app.sh
```

2. Make sure the necessary environment files exist in the project root directory.

## Application Container

The script assumes there's a container named `fastapi-app-web` where it executes Alembic migrations. If your container has a different name, modify the last line of the script.

## Troubleshooting

- **Error "File .env.X not found"**: Create the corresponding environment file
- **Error "Invalid environment"**: Use only `dev`, `prod` or `staging`
- **Migration errors**: Verify that the `fastapi-app-web` container is running and Alembic is properly configured