from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Index, Text, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScreeningRun(Base):
    """Screening Runs Audit Trail Model"""
    __tablename__ = 'screening_runs'
    __table_args__ = (
        Index('idx_screening_runs_status', 'status'),
        Index('idx_screening_runs_created_at', 'created_at'),
    )
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_start_time = Column(DateTime, nullable=False)
    run_end_time = Column(DateTime)
    total_stocks = Column(Integer)
    stocks_passed = Column(Integer)
    execution_time_seconds = Column(Integer)
    status = Column(String(20), default='running')  # running, completed, failed
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ScreeningRun {self.id} Status: {self.status}>'
