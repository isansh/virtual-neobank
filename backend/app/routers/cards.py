from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.models.card import Card
from app.schemas.card import (
    CardCreate, CardOut, CardLimitsUpdate, CardPinSet, TopUp, BalanceSummary
)
from app.routers.deps import get_current_user
from app.services.card_utils import generate_card_number, generate_iban

router = APIRouter(prefix="/api/cards", tags=["Cards"])

MAX_CARDS_PER_USER = 5


def get_user_card_or_404(card_id: int, user: User, db: Session) -> Card:
    card = db.query(Card).filter(Card.id == card_id, Card.user_id == user.id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Картку не знайдено")
    return card


@router.post("/create", response_model=CardOut, status_code=status.HTTP_201_CREATED)
def create_card(
    card_data: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.kyc_status == "rejected":
        raise HTTPException(status_code=403, detail="KYC відхилено, випуск карток недоступний")

    cards_count = db.query(Card).filter(Card.user_id == current_user.id).count()
    if cards_count >= MAX_CARDS_PER_USER:
        raise HTTPException(status_code=400, detail=f"Максимум {MAX_CARDS_PER_USER} карток на користувача")

    card_number = generate_card_number(card_data.card_type)
    while db.query(Card).filter(Card.card_number == card_number).first():
        card_number = generate_card_number(card_data.card_type)
    iban = generate_iban()
    while db.query(Card).filter(Card.iban == iban).first():
        iban = generate_iban()

    new_card = Card(
        user_id=current_user.id,
        card_number=card_number,
        iban=iban,
        card_type=card_data.card_type,
        currency=card_data.currency,
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card


@router.get("/my-cards", response_model=List[CardOut])
def get_my_cards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Card).filter(Card.user_id == current_user.id).all()


@router.get("/summary", response_model=BalanceSummary)
def get_balance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cards = db.query(Card).filter(
        Card.user_id == current_user.id, Card.status == "active"
    ).all()
    balances: dict[str, float] = {}
    for c in cards:
        balances[c.currency] = round(balances.get(c.currency, 0.0) + c.balance, 2)
    return {"cards_count": len(cards), "balances": balances}


@router.get("/{card_id}", response_model=CardOut)
def get_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_card_or_404(card_id, current_user, db)


@router.post("/{card_id}/block", response_model=CardOut)
def block_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = get_user_card_or_404(card_id, current_user, db)
    card.status = "blocked"
    db.commit()
    db.refresh(card)
    return card


@router.post("/{card_id}/unblock", response_model=CardOut)
def unblock_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = get_user_card_or_404(card_id, current_user, db)
    card.status = "active"
    db.commit()
    db.refresh(card)
    return card


@router.put("/{card_id}/limits", response_model=CardOut)
def update_limits(
    card_id: int,
    limits: CardLimitsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = get_user_card_or_404(card_id, current_user, db)
    if limits.daily_limit is not None:
        card.daily_limit = limits.daily_limit
    if limits.monthly_limit is not None:
        card.monthly_limit = limits.monthly_limit
    if card.daily_limit > card.monthly_limit:
        raise HTTPException(status_code=400, detail="Денний ліміт не може перевищувати місячний")
    db.commit()
    db.refresh(card)
    return card


@router.put("/{card_id}/pin", status_code=status.HTTP_204_NO_CONTENT)
def set_pin(
    card_id: int,
    pin_data: CardPinSet,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = get_user_card_or_404(card_id, current_user, db)
    card.pin_hash = hash_password(pin_data.pin)
    db.commit()


@router.post("/{card_id}/topup", response_model=CardOut)
def topup_card(
    card_id: int,
    data: TopUp,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = get_user_card_or_404(card_id, current_user, db)
    if card.status != "active":
        raise HTTPException(status_code=400, detail="Картка заблокована")
    card.balance += data.amount
    db.commit()
    db.refresh(card)
    return card
