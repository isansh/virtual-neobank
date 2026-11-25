from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, PasswordChange
from app.services.user_service import UserService
from app.routers.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserService.update_profile_and_kyc(db, current_user, user_update)

@router.post("/change-password")
def change_password(
    passwords: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserService.change_password(db, current_user, passwords)

@router.post("/deactivate")
def deactivate_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    UserService.set_user_active_status(db, current_user.id, False)
    return {"message": "Акаунт заблоковано"}

@router.get("/admin/clients", response_model=List[UserOut])
def search_clients(
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    return UserService.search_clients(db, q)

@router.patch("/admin/clients/{user_id}/status", response_model=UserOut)
def toggle_client_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    return UserService.set_user_active_status(db, user_id, is_active)