from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.routers.deps import get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])

# Отримання профілю поточного користувача
@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Оновлення даних профілю / KYC
@router.put("/me", response_model=UserOut)
def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.phone_number is not None:
        current_user.phone_number = user_update.phone_number
    if user_update.kyc_status is not None:
        current_user.kyc_status = user_update.kyc_status

    db.commit()
    db.refresh(current_user)
    return current_user