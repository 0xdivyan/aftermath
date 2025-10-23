# 🚀 Aftermath - Ultra-Fast Post-Earnings Arbitrage Bot

An automated trading bot that capitalizes on post-earnings market inefficiencies on Polymarket using real-time verification from Polygon.io.

## Features

- ⚡ **Ultra-Fast Execution**: Sub-second verification and trade execution
- 📊 **Real-Time Earnings Tracking**: Monitors earnings calendar and releases
- 🎯 **Smart Arbitrage**: Exploits price inefficiencies post-announcement
- 🛡️ **Risk Management**: Position sizing, return thresholds, and limits
- 📈 **Performance Monitoring**: Built-in metrics and logging

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aftermath.git
cd aftermath

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required API keys:
- **Polygon.io API Key**: Get from [polygon.io](https://polygon.io)
- **Polymarket Credentials**: API key and private key
- **Ethereum Wallet**: Private key for trade execution

### 3. Run the Bot

```bash
# Start the bot
python -m src.main

# Run in background (production)
nohup python -m src.main > logs/bot.log 2>&1 &
```

## Architecture

```
┌─────────────────┐
│ Earnings Events │
│   (Polygon.io)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Verification   │
│     Engine      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Polymarket    │
│  Market Scanner │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Trade Execution │
│     Engine      │
└─────────────────┘
```

## Configuration

### Trading Parameters

- `TRADE_ALLOCATION_PERCENTAGE`: 10% (percent of wallet per trade)
- `MIN_RETURN_THRESHOLD`: 5.0% (minimum expected return)
- `MAX_CONCURRENT_TRADES`: 3 (maximum simultaneous positions)

### Risk Controls

- Maximum position size per trade
- Daily trade limits
- Return threshold validation
- Post-verification execution only

## Strategy

1. **Track**: Monitor earnings calendar for tracked companies
2. **Verify**: Use Polygon.io to verify beat/miss immediately after release
3. **Scan**: Find corresponding Polymarket markets
4. **Calculate**: Determine potential returns
5. **Execute**: Buy Yes (beat) or No (miss) if return > threshold

## Monitoring

View real-time metrics at `http://localhost:8080/metrics`

Key metrics:
- Trades executed
- Average execution time
- Win rate
- Total P&L

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Safety & Legal

⚠️ **Important Disclaimers**:
- This bot trades real money. Use at your own risk.
- Test thoroughly with small amounts first
- Ensure compliance with local regulations
- Not financial advice

## Performance Tips

1. **Low Latency**: Deploy close to exchanges (AWS us-east-1)
2. **Fast Network**: Use dedicated network connection
3. **Monitoring**: Set up alerts for errors
4. **Backtesting**: Test strategy with historical data first

## Troubleshooting

### Common Issues

**"API key invalid"**
- Verify your API keys in .env file
- Check key permissions on Polygon.io dashboard

**"No markets found"**
- Polymarket may not have markets for all earnings
- Check market naming conventions

**"Execution too slow"**
- Optimize network latency
- Consider using WebSocket connections
- Deploy closer to exchanges

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file

## Support

For issues and questions:
- Open a GitHub issue
- Check documentation
- Review logs in `logs/` directory

---

**Disclaimer**: This software is for educational purposes. Trading involves risk. Past performance does not guarantee future results.