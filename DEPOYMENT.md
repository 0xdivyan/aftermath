# Deployment Guide

## Prerequisites

1. **Python 3.11+**
2. **API Keys:**
   - Polygon.io API key (get from https://polygon.io)
   - Polymarket API credentials
   - Ethereum wallet with private key

## Local Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/aftermath.git
cd aftermath

# Run deployment script
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 2. Configure Environment

Edit `.env` file with your credentials:

```bash
nano .env
```

Required fields:
- `POLYGON_API_KEY`
- `POLYMARKET_API_KEY`
- `POLYMARKET_PRIVATE_KEY`
- `WALLET_ADDRESS`

### 3. Test Configuration

```bash
source venv/bin/activate
pytest tests/ -v
```

### 4. Start Bot

```bash
# Foreground (for testing)
python -m src.main

# Background (for production)
nohup python -m src.main > logs/bot.log 2>&1 &
```

## Production Deployment

### Option 1: Docker (Recommended)

```bash
cd docker
docker-compose up -d
```

Monitor logs:
```bash
docker-compose logs -f
```

Stop bot:
```bash
docker-compose down
```

### Option 2: Systemd Service (Linux)

Create service file `/etc/systemd/system/aftermath.service`:

```ini
[Unit]
Description=Aftermath Earnings Arbitrage Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/aftermath
Environment="PATH=/path/to/aftermath/venv/bin"
ExecStart=/path/to/aftermath/venv/bin/python -m src.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable aftermath
sudo systemctl start aftermath
sudo systemctl status aftermath
```

View logs:
```bash
journalctl -u aftermath -f
```

### Option 3: Cloud Deployment (AWS)

#### EC2 Setup

1. Launch EC2 instance (t3.small or larger)
2. Install dependencies:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv git -y
```

3. Clone and setup:

```bash
git clone https://github.com/yourusername/aftermath.git
cd aftermath
./scripts/deploy.sh
```

4. Setup systemd service (see Option 2)

#### Using AWS Lambda (for event-driven)

Note: Lambda has cold start delays, not ideal for ultra-fast execution.

```bash
# Package for Lambda
pip install -r requirements.txt -t package/
cd package
zip -r ../aftermath-lambda.zip .
cd ..
zip -g aftermath-lambda.zip -r src/ config/
```

Deploy via AWS CLI or Console.

## Monitoring

### Metrics Dashboard

Access Prometheus metrics:
```
http://localhost:8080/metrics
```

### Grafana Setup (Optional)

```bash
docker run -d -p 3000:3000 grafana/grafana
```

Add Prometheus data source: `http://localhost:8080`

### Log Monitoring

```bash
# Real-time logs
./scripts/monitor.sh

# Search logs
grep "ERROR" logs/aftermath_*.log
```

## Performance Optimization

### 1. Network Latency

Deploy close to exchanges:
- **AWS**: us-east-1 (Virginia)
- **Google Cloud**: us-east1
- **Azure**: East US

### 2. System Optimization

```bash
# Increase file descriptors
ulimit -n 65535

# Disable swap for consistent performance
sudo swapoff -a
```

### 3. Python Optimization

```bash
# Use PyPy for faster execution (optional)
pypy3 -m venv venv-pypy
source venv-pypy/bin/activate
pip install -r requirements.txt
```

## Security Best Practices

### 1. Secure Private Keys

```bash
# Use environment variables, never commit .env
echo ".env" >> .gitignore

# Or use AWS Secrets Manager
aws secretsmanager create-secret \
  --name aftermath/private-key \
  --secret-string "your_private_key"
```

### 2. API Key Rotation

Rotate keys every 90 days:
```bash
# Update .env
nano .env

# Restart bot
sudo systemctl restart aftermath
```

### 3. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp
sudo ufw allow 8080/tcp
sudo ufw enable
```

## Troubleshooting

### Bot Not Starting

```bash
# Check logs
tail -100 logs/errors_*.log

# Verify configuration
python -c "from config.settings import settings; print(settings)"

# Test API connections
python -c "import asyncio; from src.api.polygon_client import PolygonAPIClient; \
           client = PolygonAPIClient('YOUR_KEY'); \
           asyncio.run(client.get_earnings_calendar())"
```

### Slow Execution

```bash
# Check network latency
ping api.polygon.io
ping clob.polymarket.com

# Monitor system resources
htop
```

### Trade Failures

```bash
# Check wallet balance
# Check gas prices
# Verify API keys
# Review error logs
```

## Backup & Recovery

### Backup Configuration

```bash
# Backup .env and data
tar -czf aftermath-backup-$(date +%Y%m%d).tar.gz .env data/ logs/

# Upload to S3
aws s3 cp aftermath-backup-*.tar.gz s3://your-bucket/backups/
```

### Disaster Recovery

```bash
# Restore from backup
aws s3 cp s3://your-bucket/backups/latest.tar.gz .
tar -xzf latest.tar.gz

# Restart bot
./scripts/start.sh
```

## Scaling

### Multiple Instances

For redundancy (not recommended for arbitrage):

```bash
# Instance 1: Primary
python -m src.main

# Instance 2: Backup (different wallet)
WALLET_ADDRESS=backup_wallet python -m src.main
```

### Load Balancing

Not applicable for arbitrage (speed is critical, no load balancing needed).

## Maintenance

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart
sudo systemctl restart aftermath
```

### Health Checks

```bash
# Create health check script
cat > scripts/health_check.sh << 'EOF'
#!/bin/bash
if pgrep -f "python -m src.main" > /dev/null; then
    echo "✅ Bot is running"
    exit 0
else
    echo "❌ Bot is not running"
    exit 1
fi
EOF

chmod +x scripts/health_check.sh
```

### Automated Restarts

Add to crontab:
```bash
*/5 * * * * /path/to/aftermath/scripts/health_check.sh || /path/to/aftermath/scripts/start.sh
```

## Cost Estimation

### API Costs
- **Polygon.io**: $29-199/month (depending on plan)
- **Polymarket**: Free (gas fees apply)

### Infrastructure
- **AWS EC2 t3.small**: ~$15/month
- **DigitalOcean Droplet**: ~$12/month
- **Google Cloud e2-small**: ~$13/month

### Total Monthly Cost
- **Minimum**: ~$50/month
- **Recommended**: ~$100/month (includes higher-tier API access)

## Support

For issues:
1. Check logs in `logs/` directory
2. Review documentation
3. Open GitHub issue
4. Check Polygon.io/Polymarket status pages