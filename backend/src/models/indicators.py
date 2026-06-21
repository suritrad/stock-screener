from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Indicator(Base):
    """Technical Indicators Model"""
    __tablename__ = 'indicators'
    __table_args__ = (
        UniqueConstraint('symbol', 'trade_date', name='uq_indicator_symbol_date'),
        Index('idx_indicators_symbol_date', 'symbol', 'trade_date'),
        Index('idx_indicators_status', 'calculation_status'),
    )
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey('stocks.symbol', ondelete='CASCADE'), nullable=False)
    trade_date = Column(Date, nullable=False)
    
    # EMA Indicators
    ema5 = Column(Numeric(10, 4))
    ema10 = Column(Numeric(10, 4))
    ema25 = Column(Numeric(10, 4))
    ema50 = Column(Numeric(10, 4))
    ema200 = Column(Numeric(10, 4))
    
    # Momentum Indicators
    rsi14 = Column(Numeric(10, 4))
    macd = Column(Numeric(10, 4))
    macd_signal = Column(Numeric(10, 4))
    macd_histogram = Column(Numeric(10, 4))
    
    # Trend Indicators
    adx = Column(Numeric(10, 4))
    plus_di = Column(Numeric(10, 4))
    minus_di = Column(Numeric(10, 4))
    atr = Column(Numeric(10, 4))
    
    # Volume Indicators
    relative_volume = Column(Numeric(10, 4))
    obv = Column(BigInteger)
    
    # 20-day highs/lows
    high_20 = Column(Numeric(10, 4))
    low_20 = Column(Numeric(10, 4))
    avg_volume_20 = Column(BigInteger)
    
    # Bollinger Bands
    bollinger_upper = Column(Numeric(10, 4))
    bollinger_middle = Column(Numeric(10, 4))
    bollinger_lower = Column(Numeric(10, 4))
    
    # Status
    calculation_status = Column(String(20), default='pending', index=True)
    error_reason = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Indicator {self.symbol} {self.trade_date} Status: {self.calculation_status}>'
