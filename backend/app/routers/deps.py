from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User

# Використовуємо HTTPBearer замість OAuth2PasswordBearer
security_scheme = HTTPBearer()

def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(security_scheme), 
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося валідувати авторизацію",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = auth.credentials  # Отримуємо токен з заголовка Bearer
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user