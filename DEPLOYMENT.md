# Deployment Guide

## Quick Deploy to DigitalOcean

1. **Create a Droplet**
   - Ubuntu 22.04 LTS
   - At least 2GB RAM (4GB recommended)
   - Add your SSH key

2. **Connect and Deploy**
   ```bash
   ssh root@YOUR_DROPLET_IP
   curl -sSL https://raw.githubusercontent.com/sirashton/points/main/deploy.sh | bash
   ```

3. **Set up Domain and SSL**
   ```bash
   # Point your domain to the droplet IP
   # Then run:
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Troubleshooting

### Frontend Container Keeps Restarting
- **Issue**: Nginx configuration errors
- **Fix**: Check `frontend/nginx.prod.conf` syntax
- **Command**: `sudo docker logs pointillism-frontend-1`

### Backend Container Fails to Start
- **Issue**: Missing gunicorn or other dependencies
- **Fix**: Add missing packages to `backend/requirements.txt`
- **Command**: `sudo docker logs pointillism-backend-1`

### Memory Issues During Build
- **Issue**: Build process killed due to low memory
- **Fix**: Add swap space (included in deploy.sh)
- **Command**: `sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`

### Port Conflicts
- **Issue**: Docker containers can't bind to ports
- **Fix**: Use different host ports (3000, 5000) and let system Nginx proxy
- **Check**: `sudo lsof -i :80` and `sudo docker ps`

### 502 Bad Gateway
- **Issue**: System Nginx can't reach Docker containers
- **Fix**: Ensure containers are running on correct ports and Nginx proxies to localhost:3000 and localhost:5000
- **Check**: `curl http://localhost:3000` and `curl http://localhost:5000/api/algorithms`