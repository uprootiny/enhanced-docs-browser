# 🌙 Silver Lining Production Deployment Guide

## Prerequisites
- All services running on high ports (44500, 45503, 47777, 44777)
- DNS pointing semantic.uprootiny.dev to server IP
- sudo access for SSL certificate generation

## Automated Deployment

### 1. Generate SSL Certificate
```bash
sudo python3 generate_ssl_cert.py
```

### 2. Manual SSL Setup (if automated fails)
```bash
# Stop nginx temporarily
sudo systemctl stop nginx

# Generate SSL certificate
sudo certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email admin@uprootiny.dev \
    --domains semantic.uprootiny.dev \
    --expand

# Install nginx configuration
sudo cp /tmp/semantic.uprootiny.dev.conf /etc/nginx/sites-available/semantic.uprootiny.dev
sudo ln -sf /etc/nginx/sites-available/semantic.uprootiny.dev /etc/nginx/sites-enabled/semantic.uprootiny.dev

# Test and reload nginx
sudo nginx -t
sudo systemctl start nginx
sudo systemctl reload nginx
```

## Service Architecture

### Running Services
```bash
# Main essays server (port 44500)
python3 enhanced_docs_server.py &

# Silver Lining ClojureScript UI (port 45503)  
python3 silver-cljs/serve.py &

# Randomness service (port 47777)
python3 randomness_service.py &

# Shrine contemplative service (port 44777)
python3 shrine_service.py &
```

### Production URLs
- **Main Server**: http://localhost:44500 → https://essays.uprootiny.dev (via nginx)
- **Silver Lining**: http://localhost:45503 → https://semantic.uprootiny.dev (via nginx)
- **Randomness API**: http://localhost:47777 → https://randomness.uprootiny.dev (via nginx)
- **Shrine**: http://localhost:44777 → https://shrine.uprootiny.dev (via nginx)

## Verification

### Test All Services
```bash
# Run comprehensive test suite
python3 test_production_readiness.py
```

### Check SSL Configuration
```bash
# Test SSL endpoint
curl -I https://semantic.uprootiny.dev

# Verify certificate
openssl s_client -connect semantic.uprootiny.dev:443 -servername semantic.uprootiny.dev
```

### Monitor Services
```bash
# Check service status
curl http://localhost:44500/api/files
curl http://localhost:45503/health  
curl http://localhost:47777/health
curl http://localhost:44777/health
```

## Features Deployed

### ✅ Core System
- Enhanced documentation server with ripgrep search
- Sophisticated ClojureScript semantic exploration UI
- Multi-tier randomness service with 7 entropy sources  
- Calm contemplative Shrine service

### ✅ Advanced Features
- Entropy-weighted clustering algorithms
- Stochastic jitter for dynamic exploration
- Temporal variance multipliers
- Statistical entropy quality validation

### ✅ Production Ready
- Comprehensive test coverage (40 tests)
- SSL certificate configuration ready
- nginx subdomain-to-port mapping
- Security headers and input sanitization

## System Philosophy

**Dynamic ↔ Static Balance**
- **Randomness Service**: Multi-source entropy, continuous refresh
- **Shrine Service**: Stable daily wisdom, contemplative consistency  
- **Main Server**: Reliable document serving with fast search
- **Silver Lining**: Sophisticated clustering with randomness integration

The system provides both sophisticated semantic exploration through multi-tier randomness and calm contemplative balance, creating a complete ecosystem for document discovery and reflection.