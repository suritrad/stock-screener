from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    """Stock Master Data Model"""
    __tablename__ = 'stocks'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False, index=True)
    company_name = Column(String(255), nullable=False)
    sector = Column(String(100), index=True)
    industry = Column(String(100))
    market_cap = Column(BigInteger)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Stock {self.symbol} - {self.company_name}>'
