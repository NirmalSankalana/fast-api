from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session


from ..schemas import user_schema
from .. import models
from ..database import get_db
from ..utils import hash_password

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut)
def create_users(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password.hash_password(user.password)
    # ** - unpacked the dictionary to the base class
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{id}', response_model=user_schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} is not found")
    return user
