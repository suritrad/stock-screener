# 📈 Suri Trad - Stock Screener for Thai SET/mai

A web application for screening Thai stocks (SET/mai) optimized for Day Trade and Swing Trade using Technical Indicators and AI Scoring.

## 🎯 Project Overview

**Objective**: Develop an automated stock screening system that analyzes Thai stocks using technical indicators and AI scoring to identify trading opportunities.

**Key Features**:
- ✅ Automatic data collection from SET (12:50 & 17:30)
- ✅ Real-time "Run Screener Now" button
- ✅ Technical Indicators Engine (EMA, RSI, MACD, ADX, ATR, Bollinger Bands)
- ✅ Multi-strategy screening (Strong Uptrend, Breakout, Technical Reversal)
- ✅ AI Scoring Engine
- ✅ GPT-based analysis
- ✅ CSV/Excel/PDF export

## 📦 Project Structure

```
stock-screener/
├── backend/                    # Python Flask application
│   ├── app.py                 # Main Flask app
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── src/
│       ├── phase1_data_collection/      # Phase 1: Data Collection
│       ├── phase2_indicators/           # Phase 2: Technical Indicators
│       ├── phase3_screening/            # Phase 3: Stock Screening
│       ├── models/                      # SQLAlchemy models
│       ├── api/                         # REST API endpoints
│       └── utils/                       # Utility functions
├── database/
│   ├── init.sql               # Database initialization
│   └── schema/                # Table definitions
├── frontend/                  # Frontend application
│   ├── index.html
│   ├── css/
│   └── js/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/                     # Unit tests
├── docs/                      # Documentation
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/suritrad/stock-screener.git
cd stock-screener
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Set up environment variables**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

5. **Initialize database**
```bash
psql -U postgres -f database/init.sql
```

6. **Run the application**
```bash
cd backend
python app.py
```

The application will be available at `http://localhost:5000`

## 📋 Development Phases

### ✅ Phase 1: Data Collection
- Fetch all stocks from SET/mai
- Validate data
- Store in PostgreSQL
- Auto-run at 12:50 & 17:30
- Manual "Run Now" button

### ✅ Phase 2: Technical Indicator Engine
- Calculate EMA (5, 10, 25, 50, 200)
- Calculate Momentum (RSI, MACD, ADX)
- Calculate Volume Indicators (OBV, Relative Volume)
- Calculate Volatility (ATR, Bollinger Bands)

### ✅ Phase 3: Stock Screening
- Strong Uptrend screening
- Breakout detection
- Technical Reversal patterns
- Ranking and filtering

### 📅 Phase 4: AI Scoring Engine
- Dynamic scoring algorithm
- Weighted indicator scoring

### 📅 Phase 5: GPT Analysis Engine
- ChatGPT integration for stock analysis

### 📅 Phase 6: Result Page
- Display screened stocks
- Export to CSV/Excel/PDF

## 🔧 Technology Stack

- **Backend**: Python 3.9+, Flask
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy
- **Task Scheduler**: APScheduler
- **Data Processing**: Pandas, NumPy, TA-Lib
- **Frontend**: HTML5, JavaScript, Bootstrap 5
- **API**: RESTful with JSON
- **Containerization**: Docker & Docker Compose

## 📚 Documentation

- [SRS Volume 1 - Foundation](./docs/SRS_VOLUME_1.md)
- [Database Schema](./docs/DATABASE_SCHEMA.md)
- [API Specification](./docs/API_SPEC.md)
- [Screening Rules](./docs/SCREENING_RULES.md)

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stocks` | List all stocks |
| GET | `/api/stocks/:symbol` | Get stock details |
| POST | `/api/screener/run` | Run screener manually |
| GET | `/api/screener/results` | Get latest screening results |
| GET | `/api/indicators/:symbol` | Get indicators for a stock |
| POST | `/api/export` | Export results |

## 🧪 Testing

```bash
python -m pytest tests/
```

## 🐳 Docker Setup

```bash
docker-compose up -d
```

## 📝 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/stock_screener
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Scheduler
SCHEDULER_API_ENABLED=True

# SET Data API (if available)
SET_API_URL=https://api.set.or.th/
SET_API_KEY=your-api-key
```

## 👥 Contributing

1. Create a feature branch (`git checkout -b feature/phase-x`)
2. Make your changes
3. Write tests
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Last Updated**: June 2026
**Status**: Phase 1-3 Development
**Version**: 1.0.0-alpha
