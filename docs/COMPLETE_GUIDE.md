# Stock Screener - Complete Project Documentation

## Project Structure

```
stock-screener/
├── backend/
│   ├── app.py                          # Flask app entry point
│   ├── config.py                       # Configuration management
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment template
│   └── src/
│       ├── models/                     # SQLAlchemy models
│       │   ├── stocks.py              # Stock master data
│       │   ├── daily_price.py         # Daily OHLCV data
│       │   ├── indicators.py          # Technical indicators
│       │   ├── screening_results.py   # Screening results
│       │   ├── gpt_analysis.py        # GPT analysis data
│       │   ├── system_settings.py     # Configuration settings
│       │   └── screening_runs.py      # Audit trail
│       ├── services/                   # Business logic
│       │   ├── config_service.py      # Config management
│       │   ├── scoring_service.py     # AI scoring engine
│       │   ├── indicator_calculator.py # Indicator calculations
│       │   ├── gpt_analysis_service.py # GPT integration
│       │   └── export_service.py      # Export functionality
│       └── api/                        # REST API routes
│           ├── screener_routes.py     # Screener endpoints
│           ├── stocks_routes.py       # Stock endpoints
│           └── export_routes.py       # Export endpoints
├── database/
│   ├── init.sql                       # Database initialization
│   └── schema/                         # Table definitions
│       ├── 01_stocks.sql
│       ├── 02_daily_price.sql
│       ├── 03_indicators.sql
│       ├── 04_screening_results.sql
│       ├── 05_gpt_analysis.sql
│       ├── 06_system_settings.sql
│       └── 07_screening_runs.sql
├── frontend/
│   ├── index.html                    # Main page
│   ├── css/
│   │   └── style.css                 # Styling
│   └── js/
│       └── app.js                    # Frontend app logic
├── docs/
│   ├── SRS_VOLUME_1.md              # Foundation & Phases 1-3
│   ├── SRS_VOLUME_2.md              # AI Scoring & API
│   ├── SRS_VOLUME_3.md              # GPT & Result App
│   ├── DATABASE_SCHEMA.md           # DB documentation
│   ├── API_SPEC.md                  # API documentation
│   ├── SCREENING_RULES.md           # Screening logic
│   └── PHASE_5_6_GUIDE.md           # Phase 5-6 guide
└── README.md                        # Project overview
```

## Development Phases

### Phase 1: Data Collection
- **Status**: ✅ Implemented
- Fetch stocks from SET API
- Validate data
- Store in PostgreSQL
- Automatic scheduling (12:50 & 17:30)
- Manual run capability

### Phase 2: Technical Indicators
- **Status**: ✅ Implemented
- EMA (5, 10, 25, 50, 200)
- RSI, MACD, ADX, ATR
- Bollinger Bands, OBV
- Volume calculations

### Phase 3: Stock Screening
- **Status**: ✅ Implemented
- Strong Uptrend screening
- Breakout detection
- Technical Reversal patterns
- Exclusion rules
- Ranking algorithm

### Phase 4: AI Scoring Engine
- **Status**: ✅ Implemented
- Dynamic weight system
- Market regime detection
- Individual indicator scoring
- Weighted scoring algorithm
- Recommendation generation

### Phase 5: GPT Analysis Engine
- **Status**: ✅ Implemented
- Executive summaries
- Technical analysis
- Entry/exit strategies
- Risk assessment
- Trading style recommendation
- Confidence scoring

### Phase 6: Result Application
- **Status**: ✅ Implemented
- Stock recommendation cards
- Trading plan display
- Indicator confirmation
- Risk warnings
- Search and filter
- Export functionality (CSV, Excel, PDF)

## Key Features

### Screening Engine
- 1000+ stocks support
- Multiple screening strategies
- Configurable rules
- Fast execution (<10 seconds)

### AI Scoring
- Dynamic weight adjustment
- Market regime detection
- Individual indicator scoring
- Customizable thresholds

### User Interface
- No login required
- Responsive design (Desktop, Tablet, Mobile)
- Real-time updates
- Advanced filtering
- Multi-format export

### Data Management
- PostgreSQL database
- 7 core tables
- Audit trail tracking
- Configuration management

## Technology Stack

**Backend:**
- Python 3.9+
- Flask web framework
- SQLAlchemy ORM
- PostgreSQL database
- APScheduler for task scheduling
- Pandas for data processing
- NumPy for calculations
- TA-Lib for technical indicators

**Frontend:**
- HTML5
- CSS3
- JavaScript (vanilla)
- Bootstrap 5
- Bootstrap Icons

**DevOps:**
- Docker & Docker Compose
- Environment-based configuration
- Logging and monitoring

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- pip (Python package manager)

### Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/suritrad/stock-screener.git
   cd stock-screener
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Setup environment**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

5. **Initialize database**
   ```bash
   psql -U postgres -f database/init.sql
   ```

6. **Run application**
   ```bash
   cd backend
   python app.py
   ```

7. **Access application**
   - Frontend: http://localhost:5000
   - API: http://localhost:5000/api

### Docker Setup

```bash
docker-compose up -d
```

## API Documentation

### Core Endpoints

**Screener:**
- `POST /api/screener/run` - Run screening
- `GET /api/screener/latest` - Get latest results
- `GET /api/screener/config` - Get configuration
- `PUT /api/screener/config` - Update configuration

**Stocks:**
- `GET /api/stocks` - List all stocks
- `GET /api/stocks/:symbol` - Get stock details
- `GET /api/stocks/top-picks` - Get top recommendations

**Export:**
- `POST /api/export/csv` - Export as CSV
- `POST /api/export/excel` - Export as Excel
- `POST /api/export/pdf` - Export as PDF

**Health:**
- `GET /api/health` - Health check

## Configuration

### Environment Variables

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/stock_screener

# Scheduler
SCHEDULER_ENABLED=True
SCHEDULER_TIMEZONE=Asia/Bangkok

# Data Collection
RETRY_ATTEMPTS=3
RETRY_DELAY=5
```

### Scoring Configuration

Edit `src/config/scoring_config.json` to customize:
- Indicator weights
- Market regime multipliers
- Threshold values
- Recommendation levels

## Performance Metrics

- **Screening Time**: < 10 seconds for 1000+ stocks
- **Page Load**: < 3 seconds
- **API Response**: < 1 second
- **Database Query**: < 500ms
- **Export Generation**: < 5 seconds

## Testing

```bash
# Run tests
python -m pytest tests/

# With coverage
python -m pytest --cov=src tests/
```

## Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `DATABASE_URL` for production
- [ ] Enable HTTPS
- [ ] Setup log rotation
- [ ] Configure backup strategy
- [ ] Setup monitoring and alerts

### Deployment Options

1. **Docker Compose** (Recommended for small deployments)
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Traditional Server**
   - Install dependencies
   - Run with Gunicorn
   - Setup Nginx reverse proxy
   - Enable SSL/TLS

3. **Cloud Platforms**
   - AWS ECS
   - Google Cloud Run
   - Heroku

## Troubleshooting

### Common Issues

**Issue**: Database connection failed
- Check `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- Verify credentials

**Issue**: Screener takes too long
- Check SET API availability
- Verify network connectivity
- Check system resources (CPU, memory)

**Issue**: Missing indicators
- Check historical data availability
- Verify TA-Lib installation
- Check calculation errors in logs

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/your-feature`
5. Create Pull Request

## Roadmap

### Q3 2026
- [ ] Real-time data streaming
- [ ] Backtesting engine
- [ ] Portfolio tracking
- [ ] Email notifications

### Q4 2026
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Machine learning models
- [ ] Discord/Telegram integration

## License

MIT License - See LICENSE file

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@suritrad.com

---

**Last Updated**: June 2026
**Version**: 1.0.0-alpha
**Status**: Actively Developed
