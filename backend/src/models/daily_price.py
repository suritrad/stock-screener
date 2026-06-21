from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DailyPrice(Base):
    """Daily Stock Price Model"""
    __tablename__ = 'daily_price'
    __table_args__ = (
        UniqueConstraint('symbol', 'trade_date', name='uq_symbol_trade_date'),
        Index('idx_daily_price_symbol_date', 'symbol', 'trade_date'),
        Index('idx_daily_price_trade_date', 'trade_date'),
    )
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey('stocks.symbol', ondelete='CASCADE'), nullable=False)
    trade_date = Column(Date, nullable=False)
    open_price = Column(Numeric(10, 4))
    high_price = Column(Numeric(10, 4))
    low_price = Column(Numeric(10, 4))
    close_price = Column(Numeric(10, 4))
    previous_close = Column(Numeric(10, 4))
    change = Column(Numeric(10, 4))
    change_percent = Column(Numeric(10, 4))
    volume = Column(BigInteger)
    trading_value = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DailyPrice {self.symbol} {self.trade_date} Close: {self.close_price}>'
