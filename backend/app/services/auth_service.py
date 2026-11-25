from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, TokenBlacklist
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    @staticmethod
    def register(db: Session, dto: UserCreate) -> User:
        if db.query(User).filter(User.email == dto.email).first():
            raise HTTPException(status_code=400, detail="Email вже зареєстровано")
        
        new_user = User(
            email=dto.email,
            hashed_password=hash_password(dto.password),
            full_name=dto.full_name,
            phone_number=dto.phone_number,
            role="client"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def login(db: Session, dto: UserLogin) -> dict:
        user = db.query(User).filter(User.email == dto.email).first()
        if not user or not verify_password(dto.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний email або пароль"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Обліковий запис заблоковано адміністратором"
            )
        
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def logout(db: Session, token: str) -> dict:
        if not db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first():
            db.add(TokenBlacklist(token=token))
            db.commit()
        return {"message": "Вихід виконано безпечно. Токен анульовано."}