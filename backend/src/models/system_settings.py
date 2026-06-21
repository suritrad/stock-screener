from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SystemSettings(Base):
    """System Configuration Settings Model"""
    __tablename__ = 'system_settings'
    __table_args__ = (
        Index('idx_system_settings_key', 'setting_key'),
    )
    
    id = Column(Integer, primary_key=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text, nullable=False)
    setting_type = Column(String(20))  # numeric, string, boolean, json
    description = Column(String(255))
    is_editable = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemSettings {self.setting_key} = {self.setting_value}>'
