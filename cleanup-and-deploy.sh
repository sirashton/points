#!/bin/bash

# Cleanup and deploy script for Pointillism Generator
# Run this when SSH'd into your server to fix disk space issues

echo "🧹 Cleaning up disk space and redeploying..."

# Navigate to the application directory
cd /opt/pointillism/

# Stop all containers first
echo "🛑 Stopping containers..."
sudo docker-compose -f docker-compose.prod.yml down --remove-orphans || true

# Kill any remaining containers that might be using ports
echo "🧹 Cleaning up any remaining containers..."
sudo docker kill $(sudo docker ps -q) 2>/dev/null || true

# Wait a moment for ports to be released
sleep 2

# Clean up Docker to free space
echo "🗑️ Cleaning up Docker..."
sudo docker system prune -af
sudo docker volume prune -f
sudo docker image prune -af

# Remove any dangling images
sudo docker rmi $(sudo docker images -f "dangling=true" -q) 2>/dev/null || true

# Check disk space
echo "💾 Current disk usage:"
df -h

# Pull latest changes from GitHub
echo "📥 Pulling latest changes..."
git pull origin main

# Force stop all containers and clean up
echo "🛑 Stopping existing containers..."
sudo docker-compose -f docker-compose.prod.yml down --remove-orphans || true

# Kill any remaining containers that might be using ports
echo "🧹 Cleaning up any remaining containers..."
sudo docker kill $(sudo docker ps -q) 2>/dev/null || true

# Wait a moment for ports to be released
sleep 2

# Clean up Docker to free space
echo "🗑️ Cleaning up Docker..."
sudo docker system prune -af
sudo docker volume prune -f
sudo docker image prune -af

# Remove any dangling images
sudo docker rmi $(sudo docker images -f "dangling=true" -q) 2>/dev/null || true

# Check disk space
echo "💾 Current disk usage:"
df -h

# Build with no cache to ensure latest changes
echo "🔨 Building services with latest changes (no cache)..."
sudo docker-compose -f docker-compose.prod.yml build --no-cache --pull

# Start services
echo "🚀 Starting services..."
sudo docker-compose -f docker-compose.prod.yml up -d

# Show status
echo "✅ Cleanup and deployment complete!"
echo "📊 Service status:"
sudo docker-compose -f docker-compose.prod.yml ps

echo "🌐 Your application should now be updated at your domain"
