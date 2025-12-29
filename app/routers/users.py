from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas, dependencies
from ..database import get_db

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Everyone can read user data (including non-authorized users)
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(dependencies.check_permissions),
    db: Session = Depends(get_db)
):
    # Only authorized users can list all users
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user = Depends(lambda: dependencies.check_permissions(user_id=user_id)),
    db: Session = Depends(get_db)
):
    db_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=schemas.UserResponse)
def delete_user(
    user_id: int,
    current_user = Depends(lambda: dependencies.check_permissions(user_id=user_id)),
    db: Session = Depends(get_db)
):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
