#!/bin/bash

# Domain setup script for Pointillism Generator
# Run this after deploying to configure your domain

set -e

echo "🌐 Setting up domain configuration..."

# Get domain from user
read -p "Enter your domain (e.g., pointillism.yourdomain.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "❌ Domain is required!"
    exit 1
fi

echo "📝 Configuring nginx for domain: $DOMAIN"

# Update nginx configuration
sed -i "s/your-domain.com/$DOMAIN/g" frontend/nginx.prod.conf

echo "✅ Nginx configuration updated!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure your domain's A record points to this server's IP"
echo "2. Run: sudo docker-compose -f docker-compose.prod.yml up -d"
echo "3. Set up SSL with: sudo certbot --nginx -d $DOMAIN"
echo ""
echo "🔍 To check if your domain is pointing correctly:"
echo "   nslookup $DOMAIN"
