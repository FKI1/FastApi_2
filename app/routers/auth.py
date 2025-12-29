from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from .. import crud, schemas, auth
from ..database import get_db

router = APIRouter(prefix="", tags=["authentication"])

@router.post("/login", response_model=schemas.Token)
def login(
    login_request: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, username=login_request.username)
    
    if not user or not auth.verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(hours=auth.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = auth.create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "group": user.group.value
        },
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
