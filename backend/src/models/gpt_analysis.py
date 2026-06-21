from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, ForeignKey, UniqueConstraint, Index, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GPTAnalysis(Base):
    """GPT Analysis Results Model"""
    __tablename__ = 'gpt_analysis'
    __table_args__ = (
        UniqueConstraint('symbol', 'trade_date', name='uq_gpt_symbol_date'),
        Index('idx_gpt_analysis_symbol_date', 'symbol', 'trade_date'),
    )
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey('stocks.symbol', ondelete='CASCADE'), nullable=False)
    trade_date = Column(Date, nullable=False)
    summary = Column(Text)
    support = Column(Numeric(10, 4))
    resistance = Column(Numeric(10, 4))
    stop_loss = Column(Numeric(10, 4))
    target_1 = Column(Numeric(10, 4))
    target_2 = Column(Numeric(10, 4))
    target_3 = Column(Numeric(10, 4))
    risk_reward_ratio = Column(Numeric(10, 4))
    trading_style = Column(String(50))
    confidence_level = Column(String(20))
    gpt_analysis = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<GPTAnalysis {self.symbol} {self.trade_date}>'
