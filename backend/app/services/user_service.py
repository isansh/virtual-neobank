from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserUpdate, PasswordChange
from app.core.security import verify_password, hash_password

class UserService:
    @staticmethod
    def update_profile_and_kyc(db: Session, user: User, dto: UserUpdate) -> User:
        if dto.full_name is not None:
            user.full_name = dto.full_name
        if dto.phone_number is not None:
            user.phone_number = dto.phone_number
        if dto.passport_number is not None:
            user.passport_number = dto.passport_number
        if dto.tax_id is not None:
            user.tax_id = dto.tax_id

        if user.passport_number and user.tax_id:
            user.kyc_status = "verified"

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user: User, dto: PasswordChange) -> dict:
        if not verify_password(dto.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Поточний пароль введено невірно")
        user.hashed_password = hash_password(dto.new_password)
        db.commit()
        return {"message": "Пароль успішно змінено"}

    @staticmethod
    def set_user_active_status(db: Session, target_user_id: int, is_active: bool) -> User:
        user = db.query(User).filter(User.id == target_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def search_clients(db: Session, query: Optional[str] = None) -> List[User]:
        q = db.query(User).filter(User.role == "client")
        if query:
            q = q.filter(
                or_(
                    User.full_name.ilike(f"%{query}%"),
                    User.email.ilike(f"%{query}%")
                )
            )
        return q.all()