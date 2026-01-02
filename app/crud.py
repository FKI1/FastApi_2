from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas, auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username, models.User.is_active == True).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email, models.User.is_active == True).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):

    db_user_by_username = get_user_by_username(db, user.username)
    if db_user_by_username:
        raise ValueError("Username already registered")
    

    db_user_by_email = get_user_by_email(db, user.email)
    if db_user_by_email:
        raise ValueError("Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        group=user.group
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = auth.get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    

    db_user.is_active = False
    db.commit()
    return db_user

def get_advertisement(db: Session, advertisement_id: int):
    return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()

def get_advertisements(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Advertisement)
    
    if search:
        search_filter = or_(
            models.Advertisement.title.ilike(f"%{search}%"),
            models.Advertisement.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    return query.offset(skip).limit(limit).all()

def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate, owner_id: int):
    db_advertisement = models.Advertisement(
        **advertisement.model_dump(),
        owner_id=owner_id
    )
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement

def update_advertisement(db: Session, advertisement_id: int, advertisement_update: schemas.AdvertisementUpdate):
    db_advertisement = get_advertisement(db, advertisement_id)
    if not db_advertisement:
        return None
    
    update_data = advertisement_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_advertisement, field, value)
    
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement

def delete_advertisement(db: Session, advertisement_id: int):
    db_advertisement = get_advertisement(db, advertisement_id)
    if not db_advertisement:
        return None
    
    db.delete(db_advertisement)
    db.commit()
    return db_advertisement
