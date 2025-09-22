# 🚀 DigitalOcean Deployment Guide

This guide will walk you through deploying your Pointillism Generator to DigitalOcean.

## 📋 Prerequisites

- DigitalOcean account
- Domain name (e.g., `pointillism.yourdomain.com`)
- Git repository with your code (GitHub, GitLab, etc.)

## 🎯 Step-by-Step Deployment

### Step 1: Create a DigitalOcean Droplet

1. **Log into DigitalOcean** and go to the Droplets section
2. **Click "Create Droplet"**
3. **Choose configuration:**
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($6/month - 1GB RAM, 1 CPU, 25GB SSD)
   - **Datacenter**: Choose closest to your users
   - **Authentication**: SSH Key (recommended) or Password
4. **Name your droplet**: `pointillism-generator`
5. **Click "Create Droplet"**

### Step 2: Connect to Your Droplet

```bash
# Replace with your droplet's IP address
ssh root@YOUR_DROPLET_IP

# Or if using a non-root user
ssh username@YOUR_DROPLET_IP
```

### Step 3: Set Up Your Domain

1. **In your domain registrar's DNS settings**, add an A record:
   - **Type**: A
   - **Name**: `pointillism` (or whatever subdomain you want)
   - **Value**: Your droplet's IP address
   - **TTL**: 300 (5 minutes)

2. **Wait for DNS propagation** (can take up to 24 hours, usually much faster)

### Step 4: Deploy the Application

1. **Clone your repository:**
```bash
cd /opt
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git pointillism
cd pointillism
```

2. **Update the nginx configuration:**
```bash
# Edit the nginx config file
nano frontend/nginx.prod.conf

# Replace 'your-domain.com' with your actual domain
# Replace the SSL certificate paths with your actual certificate paths
```

3. **Run the deployment script:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Step 5: Set Up SSL (Optional but Recommended)

For production, you should set up SSL certificates. Here are two options:

#### Option A: Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d pointillism.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

#### Option B: Custom SSL Certificate

1. Upload your certificate files to the droplet
2. Update `frontend/nginx.prod.conf` with the correct paths:
```nginx
ssl_certificate /path/to/your/certificate.crt;
ssl_certificate_key /path/to/your/private.key;
```

### Step 6: Configure Firewall

```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 🔧 Management Commands

### View Logs
```bash
# All services
sudo docker-compose -f docker-compose.prod.yml logs -f

# Specific service
sudo docker-compose -f docker-compose.prod.yml logs -f backend
sudo docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Update Application
```bash
cd /opt/pointillism
git pull
sudo docker-compose -f docker-compose.prod.yml up -d --build
```

### Restart Services
```bash
sudo docker-compose -f docker-compose.prod.yml restart
```

### Stop Services
```bash
sudo docker-compose -f docker-compose.prod.yml down
```

### Check Status
```bash
sudo docker-compose -f docker-compose.prod.yml ps
```

## 🛠️ Troubleshooting

### Application Not Loading
1. Check if services are running: `sudo docker-compose -f docker-compose.prod.yml ps`
2. Check logs: `sudo docker-compose -f docker-compose.prod.yml logs`
3. Check if port 80 is open: `sudo ufw status`

### Domain Not Resolving
1. Check DNS propagation: https://www.whatsmydns.net/
2. Verify A record is correct in your domain registrar
3. Wait longer for DNS propagation

### SSL Issues
1. Check certificate paths in nginx config
2. Verify certificate is valid: `openssl x509 -in /path/to/cert.crt -text -noout`
3. Check nginx error logs: `sudo docker-compose -f docker-compose.prod.yml logs frontend`

## 📊 Monitoring

### Resource Usage
```bash
# Check system resources
htop
df -h
free -h

# Check Docker resource usage
sudo docker stats
```

### Application Health
```bash
# Check if application is responding
curl -I http://your-domain.com
curl -I https://your-domain.com
```

## 🔒 Security Considerations

1. **Keep system updated**: `sudo apt update && sudo apt upgrade -y`
2. **Use SSH keys** instead of passwords
3. **Configure fail2ban** for additional security
4. **Regular backups** of your application data
5. **Monitor logs** for suspicious activity

## 💰 Cost Optimization

- **Start with the $6/month plan** - it's sufficient for most use cases
- **Monitor usage** and upgrade only if needed
- **Use DigitalOcean's monitoring** to track resource usage
- **Consider DigitalOcean Spaces** for file storage if needed

## 🎉 You're Done!

Your Pointillism Generator should now be live at `https://pointillism.yourdomain.com`!

### Next Steps:
1. Test all functionality
2. Set up monitoring alerts
3. Configure regular backups
4. Consider setting up a CDN for better performance
5. Monitor resource usage and scale as needed

## 📞 Support

If you run into issues:
1. Check the logs first
2. Verify all configuration files
3. Test locally before deploying
4. Check DigitalOcean's status page
5. Review this guide for common solutions
