#!/bin/bash

# Pointillism Generator Deployment Script
# Run this on your DigitalOcean Droplet

set -e

echo "🎨 Deploying Pointillism Generator..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
    echo "🔧 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Add swap space if not exists (helps with memory issues during build)
if [ ! -f /swapfile ]; then
    echo " Adding swap space..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/pointillism
cd /opt/pointillism

# Clone your repository
echo "📥 Cloning repository..."
if [ ! -d ".git" ]; then
    git clone https://github.com/sirashton/points.git .
fi

# Build and start services
echo "🔨 Building and starting services..."
sudo docker-compose -f docker-compose.prod.yml down || true
sudo docker-compose -f docker-compose.prod.yml build --no-cache
sudo docker-compose -f docker-compose.prod.yml up -d

# Show status
echo "✅ Deployment complete!"
echo "📊 Service status:"
sudo docker-compose -f docker-compose.prod.yml ps

echo ""
echo " Your Pointillism Generator should now be available at:"
echo "   http://your-domain.com"
echo ""
echo "📝 To view logs:"
echo "   sudo docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🔄 To update:"
echo "   git pull && sudo docker-compose -f docker-compose.prod.yml up -d --build"