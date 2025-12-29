from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from . import auth
from . import crud
from .database import get_db
from sqlalchemy.orm import Session

security = HTTPBearer()

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    if credentials is None:
        return None
    
    token_data = auth.verify_token(credentials.credentials)
    user = crud.get_user(db, user_id=token_data.user_id)
    
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    return user

def check_permissions(
    user_id: Optional[int] = None,
    advertisement_id: Optional[int] = None,
    required_group: str = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # If no authentication required for the endpoint
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication required",
        )
    
    # Admin has all permissions
    if current_user.group.value == "admin":
        return current_user
    
    # Check if user is trying to access their own data
    if user_id and user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Check if user is trying to access their own advertisement
    if advertisement_id:
        advertisement = crud.get_advertisement(db, advertisement_id)
        if advertisement and advertisement.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
    
    # Check required group
    if required_group and current_user.group.value != required_group:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return current_user

def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        if credentials is None:
            return None
        return get_current_user(credentials, db)
    except HTTPException:
        return None
