# Quick Deploy Guide

## Production Deployment

### Prerequisites
- DigitalOcean account
- Domain name
- SSH key pair

### Steps

1. **Create Droplet**
   - Ubuntu 22.04 LTS
   - 2GB RAM minimum (4GB recommended)
   - Add your SSH key

2. **Deploy Application**
   ```bash
   ssh root@YOUR_DROPLET_IP
   curl -sSL https://raw.githubusercontent.com/sirashton/points/main/deploy.sh | bash
   ```

3. **Configure Domain**
   - Point A record to droplet IP
   - Set up SSL with Certbot

4. **Verify Deployment**
   - Visit your domain
   - Test image upload and processing
   - Check both algorithms work

### Production Notes
- Uses system Nginx as reverse proxy
- Docker containers run on ports 3000 (frontend) and 5000 (backend)
- Includes swap space for memory-intensive builds
- Automatic restart on failure
- Gzip compression enabled
- Static asset caching