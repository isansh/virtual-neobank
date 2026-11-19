from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.models.user import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    card_number = Column(String(16), unique=True, index=True, nullable=False)
    iban = Column(String(29), unique=True, nullable=False)
    card_type = Column(String, default="visa")
    currency = Column(String(3), default="UAH")
    balance = Column(Float, default=0.0)
    status = Column(String, default="active")
    daily_limit = Column(Float, default=50000.0)
    monthly_limit = Column(Float, default=200000.0)
    pin_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
