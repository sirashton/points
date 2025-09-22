# ⚡ Quick Deployment Reference

## 🚀 One-Command Deployment

```bash
# On your DigitalOcean droplet
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/deploy.sh | bash
```

## 📋 Pre-Deployment Checklist

- [ ] DigitalOcean droplet created (Ubuntu 22.04, $6/month plan)
- [ ] Domain A record pointing to droplet IP
- [ ] SSH access to droplet working
- [ ] Repository is public or you have SSH keys set up

## 🔧 Essential Commands

```bash
# Deploy
./deploy.sh

# Update
git pull && sudo docker-compose -f docker-compose.prod.yml up -d --build

# View logs
sudo docker-compose -f docker-compose.prod.yml logs -f

# Check status
sudo docker-compose -f docker-compose.prod.yml ps

# Setup domain
./setup-domain.sh
```

## 🌐 Domain Setup

1. **DNS**: Add A record `pointillism.yourdomain.com` → `YOUR_DROPLET_IP`
2. **Configure**: Run `./setup-domain.sh`
3. **SSL**: Run `sudo certbot --nginx -d pointillism.yourdomain.com`

## 🆘 Quick Fixes

**App not loading?**
```bash
sudo docker-compose -f docker-compose.prod.yml logs
sudo ufw status
```

**Domain not working?**
```bash
nslookup pointillism.yourdomain.com
```

**SSL issues?**
```bash
sudo certbot certificates
sudo nginx -t
```

## 📊 Monitoring

```bash
# System resources
htop

# Docker resources
sudo docker stats

# Application health
curl -I https://pointillism.yourdomain.com
```

## 💰 Estimated Costs

- **Droplet**: $6/month (1GB RAM, 1 CPU, 25GB SSD)
- **Domain**: $10-15/year (if you don't have one)
- **SSL**: Free (Let's Encrypt)
- **Total**: ~$7-8/month
