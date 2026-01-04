from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi import status 
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas, dependencies
from ..database import get_db

router = APIRouter(prefix="/advertisement", tags=["advertisements"])

@router.get("/{advertisement_id}", response_model=schemas.AdvertisementResponse)
def read_advertisement(
    advertisement_id: int,
    db: Session = Depends(get_db)
):
    db_advertisement = crud.get_advertisement(db, advertisement_id=advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement

@router.get("/", response_model=List[schemas.AdvertisementResponse])
def read_advertisements(
    search: Optional[str] = Query(None, description="Search in title and description"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    advertisements = crud.get_advertisements(db, skip=skip, limit=limit, search=search)
    return advertisements

@router.post("/", response_model=schemas.AdvertisementResponse, status_code=status.HTTP_201_CREATED)
def create_advertisement(
    advertisement: schemas.AdvertisementCreate,
    current_user = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication required",
        )
    
    return crud.create_advertisement(
        db=db, 
        advertisement=advertisement, 
        owner_id=current_user.id
    )

@router.patch("/{advertisement_id}", response_model=schemas.AdvertisementResponse)
def update_advertisement(
    advertisement_id: int,
    advertisement_update: schemas.AdvertisementUpdate,
    current_user = Depends(
        lambda: dependencies.check_permissions(advertisement_id=advertisement_id)
    ),
    db: Session = Depends(get_db)
):
    db_advertisement = crud.update_advertisement(
        db=db, 
        advertisement_id=advertisement_id, 
        advertisement_update=advertisement_update
    )
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement

@router.delete(
    "/{advertisement_id}",
    status_code=status.HTTP_204_NO_CONTENT 
)
def delete_advertisement(
    advertisement_id: int,
    current_user = Depends(
        lambda: dependencies.check_permissions(advertisement_id=advertisement_id)
    ),
    db: Session = Depends(get_db)
):
    db_advertisement = crud.delete_advertisement(db=db, advertisement_id=advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return None 
