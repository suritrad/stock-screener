from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScreeningResult(Base):
    """Screening Results Model"""
    __tablename__ = 'screening_results'
    __table_args__ = (
        Index('idx_screening_results_run_date', 'screening_run_id', 'trade_date'),
        Index('idx_screening_results_symbol', 'symbol'),
        Index('idx_screening_results_recommendation', 'recommendation'),
    )
    
    id = Column(Integer, primary_key=True)
    screening_run_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    trade_date = Column(Date, nullable=False)
    symbol = Column(String(10), ForeignKey('stocks.symbol', ondelete='CASCADE'), nullable=False)
    screening_type = Column(String(50))
    
    # AI Score Components
    ai_score = Column(Numeric(10, 2), nullable=False)
    recommendation = Column(String(20))
    rank = Column(Integer)
    
    # Individual Indicator Scores
    ema_alignment_score = Column(Numeric(10, 2))
    rsi_score = Column(Numeric(10, 2))
    macd_score = Column(Numeric(10, 2))
    relative_volume_score = Column(Numeric(10, 2))
    breakout_score = Column(Numeric(10, 2))
    adx_score = Column(Numeric(10, 2))
    market_cap_score = Column(Numeric(10, 2))
    risk_reward_score = Column(Numeric(10, 2))
    
    # Market Context
    market_regime = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ScreeningResult {self.symbol} Score: {self.ai_score} Recommendation: {self.recommendation}>'
