from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.user import Token, LoginRequest, UserResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == login_data.username,
        User.deleted_at.is_(None)
    ).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}
    )
    
    # Audit log
    audit = AuditLog(
        user_id=user.id,
        action="LOGIN",
        entity_type="users",
        entity_id=user.id,
        ip_address=request.client.host if request.client else None,
        description=f"User {user.username} logged in"
    )
    db.add(audit)
    db.commit()
    
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.post("/logout")
def logout(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    audit = AuditLog(
        user_id=current_user.id,
        action="LOGOUT",
        entity_type="users",
        entity_id=current_user.id,
        ip_address=request.client.host if request.client else None,
        description=f"User {current_user.username} logged out"
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Logged out successfully"}
