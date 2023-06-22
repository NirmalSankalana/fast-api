from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from ..schemas import user_schema
from ..models import User
from ..utils.hash_password import verify_password

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: user_schema.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid user credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user credentials")

    return {"token": "Your Token"}