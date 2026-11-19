from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class CardCreate(BaseModel):
    card_type: Literal["visa", "mastercard"] = "visa"
    currency: Literal["UAH", "USD", "EUR"] = "UAH"


class CardLimitsUpdate(BaseModel):
    daily_limit: Optional[float] = Field(default=None, gt=0)
    monthly_limit: Optional[float] = Field(default=None, gt=0)


class CardPinSet(BaseModel):
    pin: str = Field(pattern=r"^\d{4}$")


class TopUp(BaseModel):
    amount: float = Field(gt=0)


class CardOut(BaseModel):
    id: int
    card_number: str
    iban: str
    card_type: str
    currency: str
    balance: float
    status: str
    daily_limit: float
    monthly_limit: float
    created_at: datetime

    class Config:
        from_attributes = True


class BalanceSummary(BaseModel):
    cards_count: int
    balances: dict[str, float]
