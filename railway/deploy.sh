#!/bin/bash

# Railway deployment script for CAI-CERBERUS

# Set Railway token
export RAILWAY_TOKEN=1f934b38-b539-44e6-82c4-9dcb14f23364

# Install Railway CLI if not present
if ! command -v railway &> /dev/null; then
    npm install -g @railway/cli
fi

# Login with token (browserless)
railway login --browserless

# Link to existing project
railway link

# Add new service for CERBERUS
railway add

# Set environment variables
railway variables set CERBERUS_MODEL=gpt-4o
railway variables set DB_TYPE=postgresdb
railway variables set DB_POSTGRESDB_HOST=postgres.railway.internal
railway variables set DB_POSTGRESDB_DATABASE=railway
railway variables set DB_POSTGRESDB_USER=railway
railway variables set DB_POSTGRESDB_PASSWORD=uqX3OX48RgaiIsaXEr4jQHoNqU0inbmT
railway variables set DB_POSTGRESDB_PORT=5432
railway variables set PORT=8000

# Deploy
railway up

echo "Deployment complete!"
echo "N8N: https://primary-production-7050.up.railway.app"
echo "CERBERUS API: https://cerberus-api-production.up.railway.app"